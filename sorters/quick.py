from typing import List
from .base import Sorter

class QuickSort(Sorter):
    """Quick sort using divide-and-conquer with a middle pivot."""

    name = "quick"

    def sort(self, data: List[int]) -> List[int]:
        arr = data[:]
        return self._quick_sort(arr)

    def _quick_sort(self, arr: List[int]) -> List[int]:
        if len(arr) <= 1:
            return arr

        pivot = arr[len(arr) // 2]
        left = [x for x in arr if x < pivot]
        middle = [x for x in arr if x == pivot]
        right = [x for x in arr if x > pivot]

        return self._quick_sort(left) + middle + self._quick_sort(right)
