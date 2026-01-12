"""Tooltip utility for adding hover tooltips to widgets."""

import tkinter as tk


class ToolTip:
    """
    Creates a tooltip for a given widget.

    Usage:
        button = tk.Button(root, text="Click me")
        ToolTip(button, "This button does something")
    """

    def __init__(self, widget, text, delay=500):
        """
        Initialize tooltip.

        Args:
            widget: Widget to attach tooltip to
            text: Tooltip text to display
            delay: Delay in milliseconds before showing tooltip
        """
        self.widget = widget
        self.text = text
        self.delay = delay
        self.tooltip_window = None
        self.schedule_id = None

        # Bind events
        self.widget.bind("<Enter>", self._on_enter)
        self.widget.bind("<Leave>", self._on_leave)
        self.widget.bind("<Button>", self._on_leave)  # Hide on click

    def _on_enter(self, event=None):
        """Mouse entered widget - schedule tooltip display."""
        self._cancel_schedule()
        self.schedule_id = self.widget.after(self.delay, self._show_tooltip)

    def _on_leave(self, event=None):
        """Mouse left widget - hide tooltip."""
        self._cancel_schedule()
        self._hide_tooltip()

    def _cancel_schedule(self):
        """Cancel scheduled tooltip display."""
        if self.schedule_id:
            self.widget.after_cancel(self.schedule_id)
            self.schedule_id = None

    def _show_tooltip(self):
        """Display the tooltip window."""
        if self.tooltip_window:
            return

        # Get widget position
        x = self.widget.winfo_rootx() + 20
        y = self.widget.winfo_rooty() + self.widget.winfo_height() + 5

        # Create tooltip window
        self.tooltip_window = tk.Toplevel(self.widget)
        self.tooltip_window.wm_overrideredirect(True)  # No window decorations
        self.tooltip_window.wm_geometry(f"+{x}+{y}")

        # Create label with tooltip text
        label = tk.Label(
            self.tooltip_window,
            text=self.text,
            background="#ffffe0",
            foreground="#000000",
            relief=tk.SOLID,
            borderwidth=1,
            font=("Segoe UI", 9),
            padx=5,
            pady=3
        )
        label.pack()

    def _hide_tooltip(self):
        """Hide the tooltip window."""
        if self.tooltip_window:
            self.tooltip_window.destroy()
            self.tooltip_window = None


def add_tooltip(widget, text, delay=500):
    """
    Convenience function to add a tooltip to a widget.

    Args:
        widget: Widget to add tooltip to
        text: Tooltip text
        delay: Delay in milliseconds before showing tooltip

    Returns:
        ToolTip instance
    """
    return ToolTip(widget, text, delay)
