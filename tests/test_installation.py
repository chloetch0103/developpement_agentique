"""Tests de fumée : vérifient que le projet s'installe et s'importe correctement."""

from importlib.metadata import version
from importlib.util import find_spec

import pytest

import chain


def test_package_importable():
    assert chain.__name__ == "chain"


def test_package_installe_avec_version():
    assert version("chain")


@pytest.mark.parametrize("dependance", ["langgraph", "dotenv", "pytest"])
def test_dependances_installees(dependance):
    assert find_spec(dependance) is not None, f"{dependance} n'est pas installé"
