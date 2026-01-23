"""Main tkinter application for sorting visualization."""

from __future__ import annotations

import random
import tkinter as tk
from tkinter import ttk
from typing import Dict, List, Type

from common.step import SortStep, StepType
from sorters import BubbleSort, MergeSort, SelectionSort
from sorters.base import Sorter

from .canvas_renderer import CanvasRenderer
from .controller import AnimationState, SortingController


class SortingVisualizerApp:
    """Main application window for sorting visualization."""

    DEFAULT_ARRAY_SIZE = 20
    MIN_ARRAY_SIZE = 5
    MAX_ARRAY_SIZE = 50
    MIN_VALUE = 1
    MAX_VALUE = 100

    def __init__(self, root: tk.Tk):
        """Initialize the application.

        Args:
            root: The tkinter root window.
        """
        self.root = root
        self.root.title("Sorting Algorithm Visualizer")
        self.root.geometry("900x600")
        self.root.minsize(700, 500)

        # Available sorters (using existing sorters directly)
        self._sorters: Dict[str, Type[Sorter]] = {
            "Bubble Sort": BubbleSort,
            "Selection Sort": SelectionSort,
            "Merge Sort": MergeSort,
        }

        # Current data
        self._data: List[int] = []
        self._array_size = self.DEFAULT_ARRAY_SIZE

        # Build UI
        self._create_widgets()

        # Initialize controller
        self.controller = SortingController(
            self.renderer,
            on_state_change=self._on_state_change,
            on_step=self._on_step,
        )

        # Generate initial data
        self._generate_array()

    def _create_widgets(self) -> None:
        """Create all UI widgets."""
        # Main container
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Top control panel
        self._create_control_panel(main_frame)

        # Canvas for visualization
        self._create_canvas(main_frame)

        # Button panel
        self._create_button_panel(main_frame)

        # Status bar
        self._create_status_bar(main_frame)

    def _create_control_panel(self, parent: ttk.Frame) -> None:
        """Create the top control panel."""
        control_frame = ttk.Frame(parent)
        control_frame.pack(fill=tk.X, pady=(0, 10))

        # Algorithm selection
        ttk.Label(control_frame, text="Algorithm:").pack(side=tk.LEFT, padx=(0, 5))
        self.algorithm_var = tk.StringVar(value="Bubble Sort")
        algorithm_combo = ttk.Combobox(
            control_frame,
            textvariable=self.algorithm_var,
            values=list(self._sorters.keys()),
            state="readonly",
            width=15,
        )
        algorithm_combo.pack(side=tk.LEFT, padx=(0, 20))

        # Array size
        ttk.Label(control_frame, text="Array Size:").pack(side=tk.LEFT, padx=(0, 5))
        self.size_var = tk.StringVar(value=str(self.DEFAULT_ARRAY_SIZE))
        size_spinbox = ttk.Spinbox(
            control_frame,
            from_=self.MIN_ARRAY_SIZE,
            to=self.MAX_ARRAY_SIZE,
            textvariable=self.size_var,
            width=5,
        )
        size_spinbox.pack(side=tk.LEFT, padx=(0, 10))

        # Generate button
        self.generate_btn = ttk.Button(
            control_frame, text="Generate", command=self._generate_array
        )
        self.generate_btn.pack(side=tk.LEFT, padx=(0, 20))

        # Speed control
        ttk.Label(control_frame, text="Speed:").pack(side=tk.LEFT, padx=(0, 5))
        self.speed_var = tk.DoubleVar(value=0.5)
        speed_scale = ttk.Scale(
            control_frame,
            from_=0.0,
            to=1.0,
            variable=self.speed_var,
            orient=tk.HORIZONTAL,
            length=150,
            command=self._on_speed_change,
        )
        speed_scale.pack(side=tk.LEFT)

    def _create_canvas(self, parent: ttk.Frame) -> None:
        """Create the visualization canvas."""
        canvas_frame = ttk.Frame(parent, relief=tk.SUNKEN, borderwidth=1)
        canvas_frame.pack(fill=tk.BOTH, expand=True, pady=10)

        self.canvas = tk.Canvas(
            canvas_frame,
            bg="white",
            width=800,
            height=400,
        )
        self.canvas.pack(fill=tk.BOTH, expand=True)

        # Create renderer
        self.renderer = CanvasRenderer(self.canvas)

        # Bind resize event
        self.canvas.bind("<Configure>", self._on_canvas_resize)

    def _create_button_panel(self, parent: ttk.Frame) -> None:
        """Create the button control panel."""
        button_frame = ttk.Frame(parent)
        button_frame.pack(fill=tk.X, pady=(0, 10))

        # Center the buttons
        inner_frame = ttk.Frame(button_frame)
        inner_frame.pack(anchor=tk.CENTER)

        self.start_btn = ttk.Button(
            inner_frame, text="Start", command=self._on_start, width=10
        )
        self.start_btn.pack(side=tk.LEFT, padx=5)

        self.pause_btn = ttk.Button(
            inner_frame, text="Pause", command=self._on_pause, width=10, state=tk.DISABLED
        )
        self.pause_btn.pack(side=tk.LEFT, padx=5)

        self.step_btn = ttk.Button(
            inner_frame, text="Step", command=self._on_step_btn, width=10
        )
        self.step_btn.pack(side=tk.LEFT, padx=5)

        self.reset_btn = ttk.Button(
            inner_frame, text="Reset", command=self._on_reset, width=10
        )
        self.reset_btn.pack(side=tk.LEFT, padx=5)

    def _create_status_bar(self, parent: ttk.Frame) -> None:
        """Create the status bar."""
        status_frame = ttk.Frame(parent)
        status_frame.pack(fill=tk.X)

        self.status_var = tk.StringVar(value="Ready")
        status_label = ttk.Label(
            status_frame,
            textvariable=self.status_var,
            relief=tk.SUNKEN,
            anchor=tk.W,
            padding=(5, 2),
        )
        status_label.pack(fill=tk.X)

    def _generate_array(self) -> None:
        """Generate a new random array."""
        try:
            size = int(self.size_var.get())
            size = max(self.MIN_ARRAY_SIZE, min(self.MAX_ARRAY_SIZE, size))
        except ValueError:
            size = self.DEFAULT_ARRAY_SIZE

        self._array_size = size
        self.size_var.set(str(size))

        self._data = [random.randint(self.MIN_VALUE, self.MAX_VALUE) for _ in range(size)]

        # Reset and show initial state
        self._setup_sorter()
        self.status_var.set(f"Generated array with {size} elements")

    def _setup_sorter(self) -> None:
        """Setup the sorter with current data."""
        sorter_class = self._sorters.get(self.algorithm_var.get(), BubbleSort)
        sorter = sorter_class()
        self.controller.setup(sorter, self._data.copy(), self.root)
        self.controller.set_speed(self.speed_var.get())

        # Show initial state
        initial_step = SortStep.create(self._data, StepType.INITIAL, [], "Ready to sort")
        self.renderer.render(initial_step, set())

    def _on_start(self) -> None:
        """Handle Start button click."""
        if self.controller.state == AnimationState.IDLE:
            self._setup_sorter()
        self.controller.start()

    def _on_pause(self) -> None:
        """Handle Pause button click."""
        self.controller.pause()

    def _on_step_btn(self) -> None:
        """Handle Step button click."""
        if self.controller.state == AnimationState.IDLE:
            self._setup_sorter()
        self.controller.step()

    def _on_reset(self) -> None:
        """Handle Reset button click."""
        self.controller.reset()
        self._setup_sorter()
        self.status_var.set("Reset - Ready to sort")

    def _on_speed_change(self, value: str) -> None:
        """Handle speed slider change."""
        self.controller.set_speed(float(value))

    def _on_canvas_resize(self, event: tk.Event) -> None:
        """Handle canvas resize event."""
        # Re-render current state if available
        if self.controller._current_step:
            self.renderer.render(
                self.controller._current_step,
                self.controller._sorted_indices,
            )

    def _on_state_change(self, state: AnimationState) -> None:
        """Handle animation state changes."""
        if state == AnimationState.IDLE:
            self.start_btn.config(state=tk.NORMAL)
            self.pause_btn.config(state=tk.DISABLED)
            self.step_btn.config(state=tk.NORMAL)
            self.generate_btn.config(state=tk.NORMAL)
        elif state == AnimationState.RUNNING:
            self.start_btn.config(state=tk.DISABLED)
            self.pause_btn.config(state=tk.NORMAL)
            self.step_btn.config(state=tk.DISABLED)
            self.generate_btn.config(state=tk.DISABLED)
            self.status_var.set("Sorting...")
        elif state == AnimationState.PAUSED:
            self.start_btn.config(state=tk.NORMAL)
            self.pause_btn.config(state=tk.DISABLED)
            self.step_btn.config(state=tk.NORMAL)
            self.generate_btn.config(state=tk.DISABLED)
            self.status_var.set("Paused")
        elif state == AnimationState.FINISHED:
            self.start_btn.config(state=tk.DISABLED)
            self.pause_btn.config(state=tk.DISABLED)
            self.step_btn.config(state=tk.DISABLED)
            self.generate_btn.config(state=tk.NORMAL)
            self.status_var.set("Sorting complete!")

    def _on_step(self, step: SortStep) -> None:
        """Handle step updates."""
        self.status_var.set(step.message)


def main() -> None:
    """Run the sorting visualizer application."""
    root = tk.Tk()
    app = SortingVisualizerApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
