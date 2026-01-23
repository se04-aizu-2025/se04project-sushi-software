"""Animation controller for sorting visualization."""

from __future__ import annotations

from enum import Enum, auto
from typing import Callable, Iterator, List, Optional, Set

from common.step import SortStep, StepType
from sorters.base import Sorter

from .canvas_renderer import CanvasRenderer


class AnimationState(Enum):
    """State of the animation."""

    IDLE = auto()  # No animation running
    RUNNING = auto()  # Animation playing
    PAUSED = auto()  # Animation paused
    FINISHED = auto()  # Animation completed


class SortingController:
    """Controls the sorting animation state and timing."""

    MIN_DELAY = 10  # Minimum delay in ms
    MAX_DELAY = 1000  # Maximum delay in ms
    DEFAULT_DELAY = 100  # Default delay in ms

    def __init__(
        self,
        renderer: CanvasRenderer,
        on_state_change: Optional[Callable[[AnimationState], None]] = None,
        on_step: Optional[Callable[[SortStep], None]] = None,
    ):
        """Initialize the controller.

        Args:
            renderer: The CanvasRenderer to use for drawing.
            on_state_change: Callback when animation state changes.
            on_step: Callback when a new step is rendered.
        """
        self.renderer = renderer
        self._on_state_change = on_state_change
        self._on_step = on_step

        self._state = AnimationState.IDLE
        self._delay = self.DEFAULT_DELAY
        self._steps_iterator: Optional[Iterator[SortStep]] = None
        self._current_step: Optional[SortStep] = None
        self._sorted_indices: Set[int] = set()
        self._after_id: Optional[str] = None
        self._root: Optional[object] = None

    @property
    def state(self) -> AnimationState:
        """Get current animation state."""
        return self._state

    @property
    def delay(self) -> int:
        """Get current animation delay in milliseconds."""
        return self._delay

    @delay.setter
    def delay(self, value: int) -> None:
        """Set animation delay (clamped to valid range)."""
        self._delay = max(self.MIN_DELAY, min(self.MAX_DELAY, value))

    def set_speed(self, speed: float) -> None:
        """Set animation speed (0.0 = slowest, 1.0 = fastest)."""
        # Map speed to delay: high speed = low delay
        self._delay = int(
            self.MAX_DELAY - speed * (self.MAX_DELAY - self.MIN_DELAY)
        )

    def setup(self, sorter: Sorter, data: List[int], root: object) -> None:
        """Prepare a new sorting animation.

        Args:
            sorter: The Sorter to use.
            data: The array to sort.
            root: The tkinter root window (for after() scheduling).
        """
        self.reset()
        self._root = root
        self._steps_iterator = sorter.sort_steps(data)
        self._sorted_indices.clear()
        self._set_state(AnimationState.IDLE)

    def start(self) -> None:
        """Start or resume the animation."""
        if self._steps_iterator is None:
            return

        if self._state in (AnimationState.IDLE, AnimationState.PAUSED):
            self._set_state(AnimationState.RUNNING)
            self._schedule_next_step()

    def pause(self) -> None:
        """Pause the animation."""
        if self._state == AnimationState.RUNNING:
            self._cancel_scheduled()
            self._set_state(AnimationState.PAUSED)

    def step(self) -> None:
        """Execute a single step (for manual stepping)."""
        if self._steps_iterator is None:
            return

        if self._state in (AnimationState.IDLE, AnimationState.PAUSED):
            self._execute_step()

    def reset(self) -> None:
        """Reset the animation to initial state."""
        self._cancel_scheduled()
        self._steps_iterator = None
        self._current_step = None
        self._sorted_indices.clear()
        self._set_state(AnimationState.IDLE)

    def _set_state(self, new_state: AnimationState) -> None:
        """Update state and notify listeners."""
        if self._state != new_state:
            self._state = new_state
            if self._on_state_change:
                self._on_state_change(new_state)

    def _schedule_next_step(self) -> None:
        """Schedule the next animation step."""
        if self._root is not None and self._state == AnimationState.RUNNING:
            self._after_id = self._root.after(self._delay, self._animation_tick)

    def _cancel_scheduled(self) -> None:
        """Cancel any scheduled animation."""
        if self._after_id is not None and self._root is not None:
            self._root.after_cancel(self._after_id)
            self._after_id = None

    def _animation_tick(self) -> None:
        """Handle one animation frame."""
        if self._state != AnimationState.RUNNING:
            return

        if self._execute_step():
            self._schedule_next_step()

    def _execute_step(self) -> bool:
        """Execute a single step. Returns True if more steps available."""
        if self._steps_iterator is None:
            return False

        try:
            step = next(self._steps_iterator)
            self._current_step = step

            # Track sorted indices
            if step.step_type == StepType.SORTED:
                self._sorted_indices.update(step.indices)

            # Render the step
            self.renderer.render(step, self._sorted_indices)

            # Notify listeners
            if self._on_step:
                self._on_step(step)

            return True

        except StopIteration:
            self._set_state(AnimationState.FINISHED)
            return False
