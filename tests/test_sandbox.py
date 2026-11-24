"""Tests du bac à sable qui exécute pytest sur du code généré."""

from chain.sandbox import run_pytest

TESTS_ADD = """
from solution import add


def test_add():
    assert add(2, 3) == 5
"""


def test_code_correct_passe():
    resultat = run_pytest("def add(a, b):\n    return a + b\n", TESTS_ADD)

    assert resultat.passed
    assert resultat.exit_code == 0
    assert not resultat.timed_out


def test_code_faux_echoue():
    resultat = run_pytest("def add(a, b):\n    return a - b\n", TESTS_ADD)

    assert not resultat.passed
    assert resultat.exit_code == 1
    assert "assert -1 == 5" in resultat.output  # le reviewer aura besoin de ce détail


def test_erreur_de_syntaxe_echoue():
    resultat = run_pytest("def add(a, b)\n    return a + b\n", TESTS_ADD)  # il manque « : »

    assert not resultat.passed
    assert resultat.exit_code == 2
    assert "SyntaxError" in resultat.output


def test_boucle_infinie_interrompue_par_le_timeout():
    resultat = run_pytest("def add(a, b):\n    while True:\n        pass\n", TESTS_ADD, timeout=1)

    assert not resultat.passed
    assert resultat.timed_out
    assert resultat.exit_code is None
