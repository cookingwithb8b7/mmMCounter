"""Core timer logic with state management and countdown functionality."""

import time
import uuid
from typing import Optional, Callable, Dict, Any
from src.config.defaults import TimerState


class Timer:
    """
    Manages individual timer state and countdown logic.

    Attributes:
        id: Unique identifier (UUID)
        label: Display label for the timer
        duration: Total duration in seconds
        remaining: Remaining time in seconds
        state: Current state (STOPPED/RUNNING/PAUSED/COMPLETED)
        hotkey: Global hotkey string (e.g., "ctrl+shift+1")
        alert_config: Alert settings (visual/audio)
        font_config: Font settings
    """

    def __init__(
        self,
        label: str,
        duration: int,
        timer_id: Optional[str] = None,
        hotkey: Optional[str] = None,
        alert_config: Optional[Dict] = None,
        font_config: Optional[Dict] = None
    ):
        """
        Initialize a new timer.

        Args:
            label: Display label
            duration: Total duration in seconds
            timer_id: Optional UUID (generates if None)
            hotkey: Optional global hotkey string
            alert_config: Optional alert configuration
            font_config: Optional font configuration
        """
        self.id = timer_id or str(uuid.uuid4())
        self.label = label
        self.duration = duration
        self.remaining = duration
        self.state = TimerState.STOPPED
        self.hotkey = hotkey
        self.alert_config = alert_config
        self.font_config = font_config

        # Internal state for countdown
        self._last_update = None
        self._on_complete_callback: Optional[Callable] = None
        self._on_tick_callback: Optional[Callable] = None

    def start(self):
        """Start or resume the timer."""
        if self.state == TimerState.STOPPED:
            self.remaining = self.duration  # Reset to full duration

        self.state = TimerState.RUNNING
        self._last_update = time.time()

    def pause(self):
        """Pause the timer."""
        if self.state == TimerState.RUNNING:
            self.state = TimerState.PAUSED
            self._last_update = None

    def resume(self):
        """Resume a paused timer."""
        if self.state == TimerState.PAUSED:
            self.state = TimerState.RUNNING
            self._last_update = time.time()

    def reset(self):
        """Reset timer to initial duration and stop."""
        self.state = TimerState.STOPPED
        self.remaining = self.duration
        self._last_update = None

    def stop(self):
        """Stop the timer (same as reset for now)."""
        self.reset()

    def toggle(self):
        """Toggle between running and paused/stopped."""
        if self.state == TimerState.RUNNING:
            self.pause()
        elif self.state in (TimerState.STOPPED, TimerState.PAUSED):
            if self.state == TimerState.STOPPED:
                self.start()
            else:
                self.resume()

    def update(self, current_time: float):
        """
        Update timer countdown (called by TimerManager).

        Args:
            current_time: Current time from time.time()
        """
        if self.state != TimerState.RUNNING or self._last_update is None:
            return

        # Calculate elapsed time since last update
        elapsed = current_time - self._last_update
        self._last_update = current_time

        # Update remaining time
        self.remaining -= elapsed

        # Check for completion
        if self.remaining <= 0:
            self.remaining = 0
            self.state = TimerState.COMPLETED

            # Trigger completion callback
            if self._on_complete_callback:
                self._on_complete_callback(self)

        # Trigger tick callback
        if self._on_tick_callback:
            self._on_tick_callback(self)

    def is_complete(self) -> bool:
        """Check if timer has completed."""
        return self.state == TimerState.COMPLETED

    def set_on_complete(self, callback: Callable):
        """Set callback function to call when timer completes."""
        self._on_complete_callback = callback

    def set_on_tick(self, callback: Callable):
        """Set callback function to call on each update tick."""
        self._on_tick_callback = callback

    def get_display_time(self) -> str:
        """
        Get formatted time string for display (MM:SS).

        Returns:
            Formatted time string
        """
        total_seconds = max(0, int(self.remaining))
        minutes = total_seconds // 60
        seconds = total_seconds % 60
        return f"{minutes:02d}:{seconds:02d}"

    def to_dict(self) -> Dict[str, Any]:
        """
        Serialize timer to dictionary for persistence.

        Returns:
            Dictionary representation
        """
        return {
            "id": self.id,
            "label": self.label,
            "duration_seconds": self.duration,
            "hotkey": self.hotkey,
            "state": {
                "current_state": self.state,
                "remaining_seconds": int(self.remaining)
            },
            "alert": self.alert_config,
            "font": self.font_config
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Timer':
        """
        Deserialize timer from dictionary.

        Args:
            data: Dictionary with timer configuration

        Returns:
            Timer instance
        """
        timer = cls(
            label=data["label"],
            duration=data["duration_seconds"],
            timer_id=data.get("id"),
            hotkey=data.get("hotkey"),
            alert_config=data.get("alert"),
            font_config=data.get("font")
        )

        # Restore state
        if "state" in data:
            state_data = data["state"]
            timer.state = state_data.get("current_state", TimerState.STOPPED)
            timer.remaining = state_data.get("remaining_seconds", timer.duration)

        return timer

    def __repr__(self) -> str:
        """String representation for debugging."""
        return (
            f"Timer(id={self.id[:8]}..., label='{self.label}', "
            f"duration={self.duration}s, remaining={self.remaining:.1f}s, "
            f"state={self.state})"
        )
