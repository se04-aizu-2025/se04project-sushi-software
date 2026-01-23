from typing import List
from .base import Sorter


class MergeSort(Sorter):
    """Classic merge sort (divide and conquer)."""

    name = "merge"

    def sort(self, data: List[int]) -> List[int]:
        arr = data[:]
        return self._merge_sort(arr)

    def _merge_sort(self, arr: List[int]) -> List[int]:
        if len(arr) <= 1:
            return arr

        mid = len(arr) // 2
        left = self._merge_sort(arr[:mid])
        right = self._merge_sort(arr[mid:])

        return self._merge(left, right)

    def _merge(self, left: List[int], right: List[int]) -> List[int]:
        merged = []
        i = j = 0

        while i < len(left) and j < len(right):
            if left[i] <= right[j]:
                merged.append(left[i])
                i += 1
            else:
                merged.append(right[j])
                j += 1

        merged.extend(left[i:])
        merged.extend(right[j:])
        return merged
