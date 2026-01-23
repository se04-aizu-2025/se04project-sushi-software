from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Iterator, List

from common.step import SortStep


class Sorter(ABC):
    """Abstract interface for all sorting algorithm implementations."""

    #: Human-friendly name used for selection/labels (e.g. "bubble", "merge").
    name: str

    @abstractmethod
    def sort_steps(self, data: List[int]) -> Iterator[SortStep]:
        """Yield visualization steps while sorting the data.

        Args:
            data: List of integers to sort. Will not be mutated.

        Yields:
            SortStep objects representing each step of the algorithm.
        """
        raise NotImplementedError

    def sort(self, data: List[int]) -> List[int]:
        """Return a new list sorted in ascending order without mutating the input.

        Default implementation consumes sort_steps and returns the final array.
        """
        final_step = None
        for step in self.sort_steps(data):
            final_step = step
        return list(final_step.array) if final_step else data[:]
