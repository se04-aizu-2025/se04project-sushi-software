from __future__ import annotations

from abc import ABC, abstractmethod
from typing import List


class Sorter(ABC):
    """Abstract interface for all sorting algorithm implementations."""

    #: Human-friendly name used for selection/labels (e.g. "bubble", "merge").
    name: str

    @abstractmethod
    def sort(self, data: List[int]) -> List[int]:
        """Return a new list sorted in ascending order without mutating the input."""
        raise NotImplementedError
