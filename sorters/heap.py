from typing import Iterator, List

from common.step import SortStep, StepType

from .base import Sorter


class HeapSort(Sorter):
    """Heap sort using a max-heap."""

    name = "heap"

    def sort_steps(self, data: List[int]) -> Iterator[SortStep]:
        """Yield visualization steps for heap sort."""
        arr = data[:]
        n = len(arr)

        # Initial state
        yield SortStep.create(arr, StepType.INITIAL, [], "Initial array")

        if n <= 1:
            if n == 1:
                yield SortStep.create(arr, StepType.SORTED, [0], "Single element")
            return

        # Build max heap
        yield SortStep.create(arr, StepType.COMPARE, [], "Building max heap")

        for i in range(n // 2 - 1, -1, -1):
            yield from self._heapify_steps(arr, n, i)

        yield SortStep.create(arr, StepType.COMPARE, [], "Max heap built")

        # Extract elements one by one
        for i in range(n - 1, 0, -1):
            # Swap root (max) with last unsorted element
            yield SortStep.create(
                arr,
                StepType.COMPARE,
                [0, i],
                f"Moving max {arr[0]} to sorted position",
            )

            arr[0], arr[i] = arr[i], arr[0]

            yield SortStep.create(
                arr,
                StepType.SWAP,
                [0, i],
                f"Swapped {arr[0]} and {arr[i]}",
            )

            # Mark as sorted
            yield SortStep.create(
                arr,
                StepType.SORTED,
                [i],
                f"Element {arr[i]} is now in its sorted position",
            )

            # Restore heap property
            yield from self._heapify_steps(arr, i, 0)

        # Mark first element as sorted
        yield SortStep.create(
            arr,
            StepType.SORTED,
            [0],
            f"Element {arr[0]} is now in its sorted position",
        )

    def _heapify_steps(
        self, arr: List[int], heap_size: int, root: int
    ) -> Iterator[SortStep]:
        """Heapify subtree rooted at index root, yielding steps."""
        largest = root
        left = 2 * root + 1
        right = 2 * root + 2

        # Compare with left child
        if left < heap_size:
            yield SortStep.create(
                arr,
                StepType.COMPARE,
                [largest, left],
                f"Comparing {arr[largest]} with left child {arr[left]}",
            )
            if arr[left] > arr[largest]:
                largest = left

        # Compare with right child
        if right < heap_size:
            yield SortStep.create(
                arr,
                StepType.COMPARE,
                [largest, right],
                f"Comparing {arr[largest]} with right child {arr[right]}",
            )
            if arr[right] > arr[largest]:
                largest = right

        # Swap if needed and continue heapifying
        if largest != root:
            arr[root], arr[largest] = arr[largest], arr[root]
            yield SortStep.create(
                arr,
                StepType.SWAP,
                [root, largest],
                f"Swapped {arr[largest]} and {arr[root]} to maintain heap property",
            )
            yield from self._heapify_steps(arr, heap_size, largest)
