from typing import Iterator, List

from common.step import SortStep, StepType

from .base import Sorter


class BubbleSort(Sorter):
    """Classic bubble sort with early exit when already sorted."""

    name = "bubble"

    def sort_steps(self, data: List[int]) -> Iterator[SortStep]:
        """Yield visualization steps for bubble sort."""
        arr = data[:]
        n = len(arr)

        # Initial state
        yield SortStep.create(arr, StepType.INITIAL, [], "Initial array")

        if n <= 1:
            if n == 1:
                yield SortStep.create(arr, StepType.SORTED, [0], "Single element")
            return

        for i in range(n):
            swapped = False
            for j in range(0, n - i - 1):
                # Compare step
                yield SortStep.create(
                    arr,
                    StepType.COMPARE,
                    [j, j + 1],
                    f"Comparing {arr[j]} and {arr[j + 1]}",
                )

                if arr[j] > arr[j + 1]:
                    # Swap step
                    arr[j], arr[j + 1] = arr[j + 1], arr[j]
                    yield SortStep.create(
                        arr,
                        StepType.SWAP,
                        [j, j + 1],
                        f"Swapped {arr[j + 1]} and {arr[j]}",
                    )
                    swapped = True

            # Mark last element of this pass as sorted
            sorted_idx = n - i - 1
            yield SortStep.create(
                arr,
                StepType.SORTED,
                [sorted_idx],
                f"Element {arr[sorted_idx]} is now in its sorted position",
            )

            if not swapped:
                # All remaining elements are sorted
                remaining = list(range(sorted_idx))
                if remaining:
                    yield SortStep.create(
                        arr,
                        StepType.SORTED,
                        remaining,
                        "No swaps needed - array is sorted",
                    )
                break
