"""Default configuration values for mmMCounter."""

# Default profile configuration
DEFAULT_PROFILE = {
    "profile_name": "Default",
    "version": "1.0",
    "global_settings": {
        "theme": "dark",
        "always_on_top": True,
        "window_position": {"x": 100, "y": 100},
        "window_size": {"width": 400, "height": 300},
        "default_font": {
            "family": "Arial",  # Will try OpenDyslexic if available
            "size": 12,
            "bold": False
        },
        "default_alert": {
            "visual": {
                "flash_numbers": True,
                "flash_background": True,
                "flash_window": False,
                "flash_taskbar": True,
                "flash_duration_ms": 3000,
                "flash_interval_ms": 500
            },
            "audio": {
                "enabled": True,
                "file": "assets/sounds/beepbeep.wav",
                "volume": 80
            }
        }
    },
    "timers": []
}

# Default timer configuration
DEFAULT_TIMER = {
    "id": None,  # Will be generated as UUID
    "label": "New Timer",
    "duration_seconds": 240,  # 4 minutes default
    "hotkey": None,  # No hotkey by default
    "state": {
        "current_state": "stopped",
        "remaining_seconds": 240
    },
    "alert": None,  # None means use global defaults
    "font": None  # None means use global defaults
}

# Timer states
class TimerState:
    """Timer state constants."""
    STOPPED = "stopped"
    RUNNING = "running"
    PAUSED = "paused"
    COMPLETED = "completed"

# Theme definitions (moved here from themes.py for now)
DARK_THEME = {
    "bg_color": "#2b2b2b",
    "fg_color": "#ffffff",
    "button_bg": "#3c3f41",
    "button_fg": "#ffffff",
    "button_active_bg": "#4b6eaf",
    "entry_bg": "#3c3f41",
    "entry_fg": "#ffffff",
    "alert_flash_color": "#ff4444",
    "alert_normal_color": "#ffffff"
}

LIGHT_THEME = {
    "bg_color": "#f0f0f0",
    "fg_color": "#000000",
    "button_bg": "#e0e0e0",
    "button_fg": "#000000",
    "button_active_bg": "#4b9ef0",
    "entry_bg": "#ffffff",
    "entry_fg": "#000000",
    "alert_flash_color": "#ff0000",
    "alert_normal_color": "#000000"
}

HIGH_CONTRAST_THEME = {
    "bg_color": "#000000",
    "fg_color": "#ffffff",
    "button_bg": "#000000",
    "button_fg": "#ffff00",  # Yellow text
    "button_active_bg": "#ffff00",
    "entry_bg": "#000000",
    "entry_fg": "#ffffff",
    "alert_flash_color": "#ff00ff",  # Magenta for alerts
    "alert_normal_color": "#00ff00"   # Green for normal
}

THEMES = {
    "dark": DARK_THEME,
    "light": LIGHT_THEME,
    "high_contrast": HIGH_CONTRAST_THEME
}
