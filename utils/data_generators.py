"""Data generators for sorting algorithm visualization."""

from __future__ import annotations

import random
from typing import List


def generate_random(size: int, min_val: int = -1000, max_val: int = 1000) -> List[int]:
    """Generate a list of random integers."""
    return [random.randint(min_val, max_val) for _ in range(size)]