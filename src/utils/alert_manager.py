"""Alert manager for coordinating visual alerts."""

import sys
from typing import Optional, Callable


class AlertManager:
    """
    Coordinates visual alerts for timer completion.

    Supports:
    - Flash timer numbers
    - Flash timer background
    - Flash window border (Windows)
    - Flash taskbar (Windows)
    """

    def __init__(self):
        """Initialize alert manager."""
        self.active_alerts = {}  # timer_id -> alert state

    def start_alert(
        self,
        timer_id: str,
        flash_numbers: bool = True,
        flash_background: bool = False,
        flash_window: bool = False,
        flash_taskbar: bool = True,
        duration_ms: int = 3000,
        interval_ms: int = 500,
        on_flash_callback: Optional[Callable] = None
    ):
        """
        Start a visual alert for a timer.

        Args:
            timer_id: ID of timer
            flash_numbers: Flash the timer numbers
            flash_background: Flash the timer row background
            flash_window: Flash the window border
            flash_taskbar: Flash the taskbar icon
            duration_ms: Total alert duration
            interval_ms: Flash interval
            on_flash_callback: Callback for each flash (receives timer_id)
        """
        self.active_alerts[timer_id] = {
            'flash_numbers': flash_numbers,
            'flash_background': flash_background,
            'flash_window': flash_window,
            'flash_taskbar': flash_taskbar,
            'duration_ms': duration_ms,
            'interval_ms': interval_ms,
            'elapsed_ms': 0,
            'flash_state': False,
            'on_flash_callback': on_flash_callback
        }

    def update_alert(self, timer_id: str, elapsed_ms: int) -> bool:
        """
        Update an alert state.

        Args:
            timer_id: ID of timer
            elapsed_ms: Milliseconds since last update

        Returns:
            True if alert should continue, False if complete
        """
        if timer_id not in self.active_alerts:
            return False

        alert = self.active_alerts[timer_id]
        alert['elapsed_ms'] += elapsed_ms

        # Check if alert duration exceeded
        if alert['elapsed_ms'] >= alert['duration_ms']:
            self.stop_alert(timer_id)
            return False

        # Check if we should toggle flash state
        if alert['elapsed_ms'] % alert['interval_ms'] < elapsed_ms:
            alert['flash_state'] = not alert['flash_state']

            # Trigger flash callback
            if alert['on_flash_callback']:
                alert['on_flash_callback'](timer_id)

        return True

    def stop_alert(self, timer_id: str):
        """
        Stop an alert.

        Args:
            timer_id: ID of timer
        """
        if timer_id in self.active_alerts:
            del self.active_alerts[timer_id]

    def is_flashing(self, timer_id: str) -> bool:
        """
        Check if timer is currently in flash state.

        Args:
            timer_id: ID of timer

        Returns:
            True if in flash state
        """
        if timer_id in self.active_alerts:
            return self.active_alerts[timer_id]['flash_state']
        return False

    def flash_taskbar_windows(self, hwnd):
        """
        Flash taskbar icon on Windows.

        Args:
            hwnd: Window handle
        """
        if sys.platform != 'win32':
            return

        try:
            import ctypes
            from ctypes import wintypes

            class FLASHWINFO(ctypes.Structure):
                _fields_ = [
                    ('cbSize', wintypes.UINT),
                    ('hwnd', wintypes.HWND),
                    ('dwFlags', wintypes.DWORD),
                    ('uCount', wintypes.UINT),
                    ('dwTimeout', wintypes.DWORD)
                ]

            FLASHW_ALL = 3  # Flash both caption and taskbar
            FLASHW_TIMERNOFG = 12  # Flash until window comes to foreground

            flash_info = FLASHWINFO(
                cbSize=ctypes.sizeof(FLASHWINFO),
                hwnd=hwnd,
                dwFlags=FLASHW_ALL | FLASHW_TIMERNOFG,
                uCount=0,  # Flash until foreground
                dwTimeout=0  # Default cursor blink rate
            )

            ctypes.windll.user32.FlashWindowEx(ctypes.byref(flash_info))

        except Exception as e:
            print(f"Warning: Could not flash taskbar: {e}")

    def __repr__(self) -> str:
        """String representation for debugging."""
        return f"AlertManager(active={len(self.active_alerts)})"
