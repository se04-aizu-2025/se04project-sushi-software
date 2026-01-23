from typing import Iterator, List

from common.step import SortStep, StepType
from .base import Sorter


class QuickSort(Sorter):
    """Quick sort with visualization using Lomuto partition scheme."""

    name = "quick"

    def sort_steps(self, data: List[int]) -> Iterator[SortStep]:
        arr = data[:]

        yield SortStep.create(arr, StepType.INITIAL, [], "Initial array")

        yield from self._quick_sort(arr, 0, len(arr) - 1)

        yield SortStep.create(
            arr, StepType.SORTED, list(range(len(arr))), "Array is fully sorted"
        )

    def _quick_sort(
        self, arr: List[int], low: int, high: int
    ) -> Iterator[SortStep]:
        if low < high:
            pivot_index = yield from self._partition(arr, low, high)
            yield from self._quick_sort(arr, low, pivot_index - 1)
            yield from self._quick_sort(arr, pivot_index + 1, high)

    def _partition(
        self, arr: List[int], low: int, high: int
    ) -> Iterator[int]:
        pivot = arr[high]
        i = low - 1

        for j in range(low, high):
            yield SortStep.create(
                arr,
                StepType.COMPARE,
                [j, high],
                f"Comparing {arr[j]} with pivot {pivot}",
            )

            if arr[j] <= pivot:
                i += 1
                arr[i], arr[j] = arr[j], arr[i]
                yield SortStep.create(
                    arr,
                    StepType.SWAP,
                    [i, j],
                    f"Swapping {arr[i]} and {arr[j]}",
                )

        arr[i + 1], arr[high] = arr[high], arr[i + 1]
        yield SortStep.create(
            arr,
            StepType.SWAP,
            [i + 1, high],
            f"Placing pivot in correct position",
        )

        return i + 1
