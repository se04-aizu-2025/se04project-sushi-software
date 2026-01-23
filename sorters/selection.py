from typing import Iterator, List

from common.step import SortStep, StepType

from .base import Sorter


class SelectionSort(Sorter):
    """Classic selection sort."""

    name = "selection"

    def sort_steps(self, data: List[int]) -> Iterator[SortStep]:
        """Yield visualization steps for selection sort."""
        arr = data[:]
        n = len(arr)

        # Initial state
        yield SortStep.create(arr, StepType.INITIAL, [], "Initial array")

        if n <= 1:
            if n == 1:
                yield SortStep.create(arr, StepType.SORTED, [0], "Single element")
            return

        for i in range(n):
            min_idx = i

            # Search for minimum in unsorted portion
            for j in range(i + 1, n):
                yield SortStep.create(
                    arr,
                    StepType.COMPARE,
                    [min_idx, j],
                    f"Comparing current minimum {arr[min_idx]} with {arr[j]}",
                )

                if arr[j] < arr[min_idx]:
                    min_idx = j
                    yield SortStep.create(
                        arr,
                        StepType.COMPARE,
                        [min_idx],
                        f"New minimum found: {arr[min_idx]}",
                    )

            # Swap minimum with current position if needed
            if min_idx != i:
                arr[i], arr[min_idx] = arr[min_idx], arr[i]
                yield SortStep.create(
                    arr,
                    StepType.SWAP,
                    [i, min_idx],
                    f"Swapped {arr[min_idx]} and {arr[i]}",
                )

            # Mark position as sorted
            yield SortStep.create(
                arr,
                StepType.SORTED,
                [i],
                f"Element {arr[i]} is now in its sorted position",
            )
