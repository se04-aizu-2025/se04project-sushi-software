from typing import List
from .base import Sorter


class HeapSort(Sorter):
    """Heap sort using a max-heap."""

    name = "heap"

    def sort(self, data: List[int]) -> List[int]:
        arr=data[:]
        n=len(arr)
        for i in range(n // 2 - 1, -1, -1): # Build max heap
            self._heapify(arr, n, i)
        for i in range(n - 1, 0, -1): # Extract elements one by one
            arr[0], arr[i] = arr[i], arr[0]
            self._heapify(arr, i, 0)
        return arr


    def _heapify(self, arr: List[int], heap_size: int, root: int) -> None:
        largest = root
        left = 2* root + 1
        right = 2* root + 2

        if left < heap_size and arr[left] > arr[largest]:
            largest = left

        if right < heap_size and arr[right] > arr[largest]:
            largest = right

        if largest != root:
            arr[root], arr[largest] = arr[largest], arr[root]
            self._heapify(arr, heap_size, largest)
