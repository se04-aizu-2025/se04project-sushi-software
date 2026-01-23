"""Data classes for representing sorting visualization steps."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum, auto
from typing import Tuple


class StepType(Enum):
    """Type of operation being visualized."""

    COMPARE = auto()  # Comparing two elements
    SWAP = auto()  # Swapping two elements
    INSERT = auto()  # Inserting element at position (for merge)
    SORTED = auto()  # Element(s) in final sorted position
    INITIAL = auto()  # Initial state


@dataclass(frozen=True)
class SortStep:
    """Immutable representation of a single step in the sorting process."""

    array: Tuple[int, ...]  # Current array state
    step_type: StepType  # Type of operation
    indices: Tuple[int, ...]  # Indices to highlight
    message: str  # Description of current operation

    @classmethod
    def create(
        cls,
        array: list[int],
        step_type: StepType,
        indices: list[int] | tuple[int, ...],
        message: str,
    ) -> SortStep:
        """Factory method to create a SortStep from mutable inputs."""
        return cls(
            array=tuple(array),
            step_type=step_type,
            indices=tuple(indices),
            message=message,
        )
