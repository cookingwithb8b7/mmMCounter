"""Timer row widget for displaying individual timers."""

import tkinter as tk
from typing import Callable, Optional
from src.core.timer import Timer
from src.config.defaults import TimerState
from src.utils.tooltip import add_tooltip


class TimerRow(tk.Frame):
    """
    Individual timer display row.

    Shows: Label | Time Display | Start/Pause | Reset | Config | Delete
    """

    def __init__(
        self,
        parent,
        timer: Timer,
        theme,
        on_config_click: Optional[Callable] = None,
        on_delete_click: Optional[Callable] = None
    ):
        """
        Initialize timer row.

        Args:
            parent: Parent widget
            timer: Timer instance
            theme: Theme instance
            on_config_click: Callback for config button (receives timer_id)
            on_delete_click: Callback for delete button (receives timer_id)
        """
        super().__init__(parent)
        self.timer = timer
        self.theme = theme
        self.on_config_click = on_config_click
        self.on_delete_click = on_delete_click

        # Apply theme
        self.configure(bg=theme.bg_color)

        # Create widgets
        self._create_widgets()

        # Update display
        self.update_display()

    def _create_widgets(self):
        """Create all widgets for the timer row."""
        # Label (15 characters wide)
        self.label_widget = tk.Label(
            self,
            text=self.timer.label,
            width=15,
            anchor='w',
            font=('Arial', 10)
        )
        self.theme.apply_to_widget(self.label_widget, "label")
        self.label_widget.grid(row=0, column=0, padx=5, pady=2, sticky='w')

        # Time display (MM:SS format, large font)
        self.time_display = tk.Label(
            self,
            text="00:00",
            width=8,
            font=('Arial', 16, 'bold')
        )
        self.theme.apply_to_widget(self.time_display, "label")
        self.time_display.grid(row=0, column=1, padx=5, pady=2)

        # Start/Pause button
        self.start_button = tk.Button(
            self,
            text="Start",
            width=8,
            command=self._on_start_pause_click
        )
        self.theme.apply_to_widget(self.start_button, "button")
        self.start_button.grid(row=0, column=2, padx=2, pady=2)
        add_tooltip(
            self.start_button,
            "Start/pause the timer (hotkey if configured)"
        )

        # Reset button
        self.reset_button = tk.Button(
            self,
            text="Reset",
            width=8,
            command=self._on_reset_click
        )
        self.theme.apply_to_widget(self.reset_button, "button")
        self.reset_button.grid(row=0, column=3, padx=2, pady=2)
        add_tooltip(self.reset_button, "Reset timer to initial duration")

        # Config button (gear icon as text)
        self.config_button = tk.Button(
            self,
            text="Config",
            width=6,
            command=self._on_config_button_click
        )
        self.theme.apply_to_widget(self.config_button, "button")
        self.config_button.grid(row=0, column=4, padx=2, pady=2)
        add_tooltip(
            self.config_button,
            "Configure timer settings (label, duration, hotkey, alerts)"
        )

        # Delete button
        self.delete_button = tk.Button(
            self,
            text="X",
            width=3,
            command=self._on_delete_button_click
        )
        self.theme.apply_to_widget(self.delete_button, "button")
        self.delete_button.grid(row=0, column=5, padx=2, pady=2)
        add_tooltip(self.delete_button, "Delete this timer")

    def _on_start_pause_click(self):
        """Handle start/pause button click."""
        if self.timer.state == TimerState.STOPPED:
            self.timer.start()
        elif self.timer.state == TimerState.RUNNING:
            self.timer.pause()
        elif self.timer.state == TimerState.PAUSED:
            self.timer.resume()
        elif self.timer.state == TimerState.COMPLETED:
            self.timer.reset()
            self.timer.start()

        self.update_display()

    def _on_reset_click(self):
        """Handle reset button click."""
        self.timer.reset()
        self.update_display()

    def _on_config_button_click(self):
        """Handle config button click."""
        if self.on_config_click:
            self.on_config_click(self.timer.id)

    def _on_delete_button_click(self):
        """Handle delete button click."""
        if self.on_delete_click:
            self.on_delete_click(self.timer.id)

    def update_display(self):
        """Update the display based on timer state."""
        # Update time display
        self.time_display.configure(text=self.timer.get_display_time())

        # Update start/pause button text
        if self.timer.state == TimerState.STOPPED:
            self.start_button.configure(text="Start")
        elif self.timer.state == TimerState.RUNNING:
            self.start_button.configure(text="Pause")
        elif self.timer.state == TimerState.PAUSED:
            self.start_button.configure(text="Resume")
        elif self.timer.state == TimerState.COMPLETED:
            self.start_button.configure(text="Restart")

        # Change time color if completed
        if self.timer.state == TimerState.COMPLETED:
            self.time_display.configure(fg=self.theme.alert_flash_color)
        else:
            self.time_display.configure(fg=self.theme.fg_color)

    def flash_alert(self):
        """Flash the timer display for visual alert."""
        # Toggle between alert color and normal color
        current_fg = self.time_display.cget('fg')
        if current_fg == self.theme.alert_flash_color:
            self.time_display.configure(fg=self.theme.alert_normal_color)
        else:
            self.time_display.configure(fg=self.theme.alert_flash_color)
