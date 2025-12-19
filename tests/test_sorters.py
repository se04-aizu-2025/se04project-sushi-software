from __future__ import annotations

import importlib
import inspect
import pkgutil
from typing import List

import pytest

import sorters
from sorters.base import Sorter


def _discover_sorter_classes() -> List[type[Sorter]]:
    """Import all sorter modules and collect concrete Sorter subclasses."""
    classes: List[type[Sorter]] = []
    for module_info in pkgutil.iter_modules(sorters.__path__):
        if module_info.name.startswith("_") or module_info.name == "base":
            continue
        module = importlib.import_module(f"{sorters.__name__}.{module_info.name}")
        for _, obj in inspect.getmembers(module, inspect.isclass):
            if issubclass(obj, Sorter) and obj is not Sorter and not inspect.isabstract(obj):
                classes.append(obj)
    if not classes:
        raise RuntimeError("No Sorter implementations found")
    return classes


@pytest.fixture(scope="module")
def sorter_instances() -> List[Sorter]:
    """Instantiate all available sorter implementations."""
    return [cls() for cls in _discover_sorter_classes()]


@pytest.mark.parametrize(
    "data",
    [
        [],
        [1],
        [2, 1],
        [5, 5, 1, 1],
        [3, -1, 2, 0],
        [10, 9, 8, 7, 6],
        [1, 2, 3, 4, 5],
    ],
    ids=[
        "empty",
        "single",
        "two_unsorted",
        "duplicates",
        "mixed_sign",
        "reverse",
        "already_sorted",
    ],
)
def test_sort_matches_builtin(sorter_instances: List[Sorter], data: List[int]) -> None:
    for sorter in sorter_instances:
        original = list(data)
        result = sorter.sort(original)
        assert result == sorted(data)
        assert original == data  # input must not be mutated
        assert result is not original


def test_name_is_non_empty(sorter_instances: List[Sorter]) -> None:
    for sorter in sorter_instances:
        assert isinstance(sorter.name, str) and sorter.name.strip()
