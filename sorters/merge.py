from typing import Iterator, List

from common.step import SortStep, StepType

from .base import Sorter


class MergeSort(Sorter):
    """Classic merge sort (divide and conquer) with bottom-up approach for visualization."""

    name = "merge"

    def sort_steps(self, data: List[int]) -> Iterator[SortStep]:
        """Yield visualization steps for merge sort."""
        arr = data[:]
        n = len(arr)

        # Initial state
        yield SortStep.create(arr, StepType.INITIAL, [], "Initial array")

        if n <= 1:
            if n == 1:
                yield SortStep.create(
                    arr, StepType.SORTED, [0], "Single element is already sorted"
                )
            return

        # Bottom-up merge sort for clearer visualization
        size = 1
        while size < n:
            for start in range(0, n, 2 * size):
                mid = min(start + size, n)
                end = min(start + 2 * size, n)

                if mid < end:
                    # Show the subarrays being merged
                    left_indices = list(range(start, mid))
                    right_indices = list(range(mid, end))

                    yield SortStep.create(
                        arr,
                        StepType.COMPARE,
                        left_indices + right_indices,
                        f"Merging subarrays [{start}:{mid}] and [{mid}:{end}]",
                    )

                    # Perform merge and yield steps
                    yield from self._merge(arr, start, mid, end)

            size *= 2

        # Mark all as sorted
        yield SortStep.create(
            arr, StepType.SORTED, list(range(n)), "Array is fully sorted"
        )

    def _merge(
        self, arr: List[int], start: int, mid: int, end: int
    ) -> Iterator[SortStep]:
        """Merge two sorted subarrays and yield steps."""
        left = arr[start:mid]
        right = arr[mid:end]
        i = j = 0
        k = start

        while i < len(left) and j < len(right):
            yield SortStep.create(
                arr,
                StepType.COMPARE,
                [start + i, mid + j] if start + i < mid else [k],
                f"Comparing {left[i]} and {right[j]}",
            )

            if left[i] <= right[j]:
                arr[k] = left[i]
                yield SortStep.create(
                    arr,
                    StepType.INSERT,
                    [k],
                    f"Inserting {left[i]} at position {k}",
                )
                i += 1
            else:
                arr[k] = right[j]
                yield SortStep.create(
                    arr,
                    StepType.INSERT,
                    [k],
                    f"Inserting {right[j]} at position {k}",
                )
                j += 1
            k += 1

        # Copy remaining elements from left
        while i < len(left):
            arr[k] = left[i]
            yield SortStep.create(
                arr,
                StepType.INSERT,
                [k],
                f"Inserting remaining {left[i]} at position {k}",
            )
            i += 1
            k += 1

        # Copy remaining elements from right
        while j < len(right):
            arr[k] = right[j]
            yield SortStep.create(
                arr,
                StepType.INSERT,
                [k],
                f"Inserting remaining {right[j]} at position {k}",
            )
            j += 1
            k += 1
