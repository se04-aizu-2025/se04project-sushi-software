"""Canvas renderer for bar chart visualization of sorting algorithms."""

from __future__ import annotations

import tkinter as tk
from typing import Set, Tuple

from common.step import SortStep, StepType


class CanvasRenderer:
    """Renders the sorting array as a bar chart on a tkinter Canvas."""

    # Color scheme
    COLOR_NORMAL = "#4A90D9"  # Blue - normal elements
    COLOR_COMPARE = "#F5A623"  # Orange - comparing
    COLOR_SWAP = "#D0021B"  # Red - swapping
    COLOR_SORTED = "#7ED321"  # Green - sorted
    COLOR_INSERT = "#9013FE"  # Purple - inserting
    COLOR_BAR_OUTLINE = "#2C3E50"  # Dark outline

    def __init__(self, canvas: tk.Canvas, padding: int = 20):
        """Initialize the renderer.

        Args:
            canvas: The tkinter Canvas to draw on.
            padding: Padding around the chart area.
        """
        self.canvas = canvas
        self.padding = padding
        self._bar_ids: list[int] = []
        self._text_ids: list[int] = []

    def render(
        self,
        step: SortStep,
        sorted_indices: Set[int] | None = None,
    ) -> None:
        """Render the current sorting step.

        Args:
            step: The SortStep to visualize.
            sorted_indices: Set of indices that are in their final sorted position.
        """
        self.canvas.delete("all")
        self._bar_ids.clear()
        self._text_ids.clear()

        if not step.array:
            return

        sorted_indices = sorted_indices or set()

        # Calculate dimensions
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()

        if canvas_width <= 1 or canvas_height <= 1:
            # Canvas not yet rendered, use requested size
            canvas_width = int(self.canvas.cget("width"))
            canvas_height = int(self.canvas.cget("height"))

        chart_width = canvas_width - 2 * self.padding
        chart_height = canvas_height - 2 * self.padding - 30  # Space for values

        n = len(step.array)
        bar_width = chart_width / n
        max_val = max(step.array) if step.array else 1

        # Draw bars
        for i, value in enumerate(step.array):
            x1 = self.padding + i * bar_width + 2
            x2 = self.padding + (i + 1) * bar_width - 2
            bar_height = (value / max_val) * chart_height
            y1 = canvas_height - self.padding - 25 - bar_height
            y2 = canvas_height - self.padding - 25

            # Determine color
            color = self._get_color(i, step, sorted_indices)

            # Draw bar
            bar_id = self.canvas.create_rectangle(
                x1,
                y1,
                x2,
                y2,
                fill=color,
                outline=self.COLOR_BAR_OUTLINE,
                width=1,
            )
            self._bar_ids.append(bar_id)

            # Draw value below bar
            text_x = (x1 + x2) / 2
            text_y = canvas_height - self.padding - 10
            text_id = self.canvas.create_text(
                text_x,
                text_y,
                text=str(value),
                font=("Helvetica", 9),
                fill="#333333",
            )
            self._text_ids.append(text_id)

    def _get_color(
        self,
        index: int,
        step: SortStep,
        sorted_indices: Set[int],
    ) -> str:
        """Determine the color for a bar based on its state."""
        # Check if this index is highlighted in the current step
        is_highlighted = index in step.indices

        if is_highlighted:
            if step.step_type == StepType.COMPARE:
                return self.COLOR_COMPARE
            elif step.step_type == StepType.SWAP:
                return self.COLOR_SWAP
            elif step.step_type == StepType.INSERT:
                return self.COLOR_INSERT
            elif step.step_type == StepType.SORTED:
                return self.COLOR_SORTED

        # Check if already sorted
        if index in sorted_indices:
            return self.COLOR_SORTED

        return self.COLOR_NORMAL

    def get_dimensions(self) -> Tuple[int, int]:
        """Get current canvas dimensions."""
        return (self.canvas.winfo_width(), self.canvas.winfo_height())
