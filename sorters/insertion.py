from typing import Iterator, List

from common.step import SortStep, StepType
from .base import Sorter


class InsertionSort(Sorter):
    """Insertion sort with visualization steps."""

    name = "insertion"

    def sort_steps(self, data: List[int]) -> Iterator[SortStep]:
        arr = data[:]
        n = len(arr)

        yield SortStep.create(arr, StepType.INITIAL, [], "Initial array")

        for i in range(1, n):
            key = arr[i]
            j = i - 1

            while j >= 0:
                yield SortStep.create(
                    arr,
                    StepType.COMPARE,
                    [j, j + 1],
                    f"Comparing {arr[j]} and {key}",
                )

                if arr[j] > key:
                    arr[j + 1] = arr[j]
                    yield SortStep.create(
                        arr,
                        StepType.SWAP,
                        [j, j + 1],
                        f"Shifting {arr[j]} to the right",
                    )
                    j -= 1
                else:
                    break

            arr[j + 1] = key
            yield SortStep.create(
                arr,
                StepType.INSERT,
                [j + 1],
                f"Inserting {key} at position {j + 1}",
            )

        yield SortStep.create(
            arr, StepType.SORTED, list(range(n)), "Array is fully sorted"
        )

