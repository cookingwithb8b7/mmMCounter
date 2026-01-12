"""Theme definitions and management for UI styling."""

from typing import Dict
from src.config.defaults import THEMES, DARK_THEME, LIGHT_THEME


class Theme:
    """
    Theme manager for UI color schemes.

    Provides easy access to current theme colors.
    """

    def __init__(self, theme_name: str = "dark"):
        """
        Initialize theme.

        Args:
            theme_name: Name of theme ('dark' or 'light')
        """
        self.name = theme_name
        self._colors = THEMES.get(theme_name, DARK_THEME)

    @property
    def bg_color(self) -> str:
        """Background color."""
        return self._colors["bg_color"]

    @property
    def fg_color(self) -> str:
        """Foreground (text) color."""
        return self._colors["fg_color"]

    @property
    def button_bg(self) -> str:
        """Button background color."""
        return self._colors["button_bg"]

    @property
    def button_fg(self) -> str:
        """Button foreground color."""
        return self._colors["button_fg"]

    @property
    def button_active_bg(self) -> str:
        """Active button background color."""
        return self._colors["button_active_bg"]

    @property
    def entry_bg(self) -> str:
        """Entry field background color."""
        return self._colors["entry_bg"]

    @property
    def entry_fg(self) -> str:
        """Entry field foreground color."""
        return self._colors["entry_fg"]

    @property
    def alert_flash_color(self) -> str:
        """Alert flash color (for visual alerts)."""
        return self._colors["alert_flash_color"]

    @property
    def alert_normal_color(self) -> str:
        """Normal color when not alerting."""
        return self._colors["alert_normal_color"]

    def switch_theme(self, theme_name: str):
        """
        Switch to a different theme.

        Args:
            theme_name: Name of theme to switch to
        """
        if theme_name in THEMES:
            self.name = theme_name
            self._colors = THEMES[theme_name]

    def apply_to_widget(self, widget, widget_type: str = "frame"):
        """
        Apply theme colors to a tkinter widget.

        Args:
            widget: Tkinter widget
            widget_type: Type of widget ('frame', 'button', 'entry', 'label')
        """
        try:
            if widget_type == "frame":
                widget.configure(bg=self.bg_color)
            elif widget_type == "button":
                widget.configure(
                    bg=self.button_bg,
                    fg=self.button_fg,
                    activebackground=self.button_active_bg
                )
            elif widget_type == "entry":
                widget.configure(
                    bg=self.entry_bg,
                    fg=self.entry_fg,
                    insertbackground=self.entry_fg
                )
            elif widget_type == "label":
                widget.configure(
                    bg=self.bg_color,
                    fg=self.fg_color
                )
        except Exception as e:
            # Some widgets may not support all config options
            print(f"Warning: Could not apply theme to {widget_type}: {e}")
