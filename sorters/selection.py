from typing import List

from .base import Sorter

class SelectionSort(Sorter):
    """Classic selection sort."""

    name = "selection"

    def sort(self, data: List[int]) -> List[int]:
        arr = data[:]
        n = len(arr)

        for i in range(n):
            min_inx = i  #minimum index
            for j in range(i + 1, n):
                if arr[j] < arr[min_inx]:
                    min_inx = j

            if min_inx != i:
                arr[i], arr[min_inx] = arr[min_inx], arr[i]
        return arr
