"""Timer manager for orchestrating multiple timers."""

import time
import threading
from typing import List, Optional, Callable, Dict
from src.core.timer import Timer
from src.config.defaults import TimerState


class TimerManager:
    """
    Manages multiple timers with a single update thread.

    Handles timer lifecycle, update loop, and event coordination.
    """

    def __init__(self, update_interval_ms: int = 100):
        """
        Initialize the timer manager.

        Args:
            update_interval_ms: Update tick interval in milliseconds (default: 100ms)
        """
        self.timers: List[Timer] = []
        self.update_interval = update_interval_ms / 1000.0  # Convert to seconds
        self._running = False
        self._update_thread: Optional[threading.Thread] = None
        self._lock = threading.Lock()

        # Callbacks for UI integration
        self._on_timer_complete: Optional[Callable] = None
        self._on_timer_tick: Optional[Callable] = None

    def add_timer(self, timer: Timer):
        """
        Add a timer to the manager.

        Args:
            timer: Timer instance to add
        """
        with self._lock:
            self.timers.append(timer)

            # Set completion callback
            timer.set_on_complete(self._handle_timer_complete)
            timer.set_on_tick(self._handle_timer_tick)

    def remove_timer(self, timer_id: str) -> bool:
        """
        Remove a timer by ID.

        Args:
            timer_id: UUID of timer to remove

        Returns:
            True if timer was removed, False if not found
        """
        with self._lock:
            for i, timer in enumerate(self.timers):
                if timer.id == timer_id:
                    del self.timers[i]
                    return True
        return False

    def get_timer(self, timer_id: str) -> Optional[Timer]:
        """
        Get a timer by ID.

        Args:
            timer_id: UUID of timer

        Returns:
            Timer instance or None if not found
        """
        with self._lock:
            for timer in self.timers:
                if timer.id == timer_id:
                    return timer
        return None

    def get_all_timers(self) -> List[Timer]:
        """Get a copy of all timers."""
        with self._lock:
            return list(self.timers)

    def start(self):
        """Start the update loop thread."""
        if not self._running:
            self._running = True
            self._update_thread = threading.Thread(target=self._update_loop, daemon=True)
            self._update_thread.start()

    def stop(self):
        """Stop the update loop thread."""
        self._running = False
        if self._update_thread:
            self._update_thread.join(timeout=1.0)
            self._update_thread = None

    def _update_loop(self):
        """Background thread that updates all timers."""
        while self._running:
            try:
                current_time = time.time()

                # Update all running timers
                with self._lock:
                    for timer in self.timers:
                        if timer.state == TimerState.RUNNING:
                            timer.update(current_time)

                # Sleep for update interval
                time.sleep(self.update_interval)

            except Exception as e:
                print(f"Error in timer update loop: {e}")

    def _handle_timer_complete(self, timer: Timer):
        """
        Handle timer completion event.

        Args:
            timer: Timer that completed
        """
        if self._on_timer_complete:
            self._on_timer_complete(timer)

    def _handle_timer_tick(self, timer: Timer):
        """
        Handle timer tick event.

        Args:
            timer: Timer that ticked
        """
        if self._on_timer_tick:
            self._on_timer_tick(timer)

    def set_on_timer_complete(self, callback: Callable):
        """
        Set callback for timer completion events.

        Callback signature: callback(timer: Timer) -> None
        """
        self._on_timer_complete = callback

    def set_on_timer_tick(self, callback: Callable):
        """
        Set callback for timer tick events.

        Callback signature: callback(timer: Timer) -> None
        """
        self._on_timer_tick = callback

    def execute_timer_action(self, timer_id: str, action: str):
        """
        Execute an action on a timer (used for hotkey callbacks).

        Args:
            timer_id: UUID of timer
            action: Action to perform ('start', 'pause', 'reset', 'toggle')
        """
        timer = self.get_timer(timer_id)
        if timer:
            if action == 'start':
                timer.start()
            elif action == 'pause':
                timer.pause()
            elif action == 'reset':
                timer.reset()
            elif action == 'toggle':
                timer.toggle()

    def to_dict_list(self) -> List[Dict]:
        """Serialize all timers to list of dictionaries."""
        with self._lock:
            return [timer.to_dict() for timer in self.timers]

    def clear(self):
        """Remove all timers."""
        with self._lock:
            self.timers.clear()

    def load_from_dict_list(self, timer_data_list: List[Dict]):
        """
        Load timers from a list of dictionaries.

        Args:
            timer_data_list: List of timer configuration dictionaries
        """
        self.clear()
        for timer_data in timer_data_list:
            timer = Timer.from_dict(timer_data)
            self.add_timer(timer)

    def __len__(self) -> int:
        """Get number of timers."""
        return len(self.timers)

    def __repr__(self) -> str:
        """String representation for debugging."""
        return f"TimerManager(timers={len(self.timers)}, running={self._running})"
