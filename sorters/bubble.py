from typing import List

from .base import Sorter


class BubbleSort(Sorter):
    """Classic bubble sort with early exit when already sorted."""

    name = "bubble"

    def sort(self, data: List[int]) -> List[int]:
        arr = data[:]
        n = len(arr)
        for i in range(n):
            swapped = False
            for j in range(0, n - i - 1):
                if arr[j] > arr[j + 1]:
                    arr[j], arr[j + 1] = arr[j + 1], arr[j]
                    swapped = True
            if not swapped:  # finished early if no swaps occurred
                break
        return arr
