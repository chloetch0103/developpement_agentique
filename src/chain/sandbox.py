import subprocess
import sys
import tempfile
from dataclasses import dataclass
from pathlib import Path


@dataclass
class PytestResult:
    passed: bool
    exit_code: int | None  # None en cas de timeout
    output: str  # stdout + stderr de pytest
    timed_out: bool = False


def run_pytest(code: str, tests: str, timeout: float = 10.0) -> PytestResult:
    with tempfile.TemporaryDirectory() as dossier:
        (Path(dossier) / "solution.py").write_text(code, encoding="utf-8")
        (Path(dossier) / "test_solution.py").write_text(tests, encoding="utf-8")
        try:
            result = subprocess.run(
                [sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider", "test_solution.py"],
                check=False, capture_output=True, cwd=dossier,
                text=True,
                timeout=timeout,
            )
            return PytestResult(
                passed=result.returncode == 0,
                exit_code=result.returncode,
                output=result.stdout + result.stderr,
                timed_out=False,
            )
        except subprocess.TimeoutExpired:
            return PytestResult(timed_out=True, passed=False, exit_code=None, output="Le test a pris trop de temps")
