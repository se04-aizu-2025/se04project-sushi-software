from typing import List
from .base import Sorter

class InsertionSort(Sorter):
    """Insertion sort builds the final sorted array one item at a time."""

    name = "insertion"

    def sort(self, data: List[int]) -> List[int]:
        arr = data[:]

        for i in range(1, len(arr)):
            key = arr[i]
            j = i - 1

            while j >= 0 and arr[j] > key:
                arr[j + 1] = arr[j]
                j -= 1

            arr[j + 1] = key

        return arr
