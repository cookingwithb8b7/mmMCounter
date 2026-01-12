"""Settings dialog for global application preferences."""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from typing import Optional, Dict, Any
from src.ui.themes import Theme


class SettingsDialog:
    """
    Modal dialog for global application settings.

    Settings include:
    - Theme selection (dark/light)
    - Always-on-top preference
    - Default alert configuration
    - Default timer settings
    """

    def __init__(self, parent: tk.Tk, current_settings: Dict[str, Any], theme: Theme):
        """
        Initialize settings dialog.

        Args:
            parent: Parent window
            current_settings: Current global settings dictionary
            theme: Current theme
        """
        self.parent = parent
        self.current_settings = current_settings.copy()
        self.theme = theme
        self.result = None

        # Create dialog window
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Settings")
        self.dialog.configure(bg=theme.bg_color)
        self.dialog.resizable(False, False)

        # Make modal
        self.dialog.transient(parent)
        self.dialog.grab_set()

        # Build UI
        self._build_ui()

        # Center on parent
        self._center_on_parent()

    def _build_ui(self):
        """Build the settings dialog UI."""
        # Main container
        main_frame = tk.Frame(self.dialog, bg=self.theme.bg_color)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)

        # Appearance Section
        self._create_appearance_section(main_frame)

        # Separator
        ttk.Separator(main_frame, orient='horizontal').pack(fill=tk.X, pady=10)

        # Default Alert Section
        self._create_default_alert_section(main_frame)

        # Separator
        ttk.Separator(main_frame, orient='horizontal').pack(fill=tk.X, pady=10)

        # Buttons
        self._create_buttons(main_frame)

    def _create_appearance_section(self, parent):
        """Create appearance settings section."""
        section = tk.LabelFrame(
            parent,
            text="Appearance",
            bg=self.theme.bg_color,
            fg=self.theme.fg_color,
            font=("Segoe UI", 10, "bold")
        )
        section.pack(fill=tk.X, pady=5)

        # Theme selection
        theme_frame = tk.Frame(section, bg=self.theme.bg_color)
        theme_frame.pack(fill=tk.X, padx=10, pady=5)

        tk.Label(
            theme_frame,
            text="Theme:",
            bg=self.theme.bg_color,
            fg=self.theme.fg_color,
            font=("Segoe UI", 9)
        ).pack(side=tk.LEFT, padx=5)

        self.theme_var = tk.StringVar(value=self.current_settings.get("theme", "dark"))
        theme_combo = ttk.Combobox(
            theme_frame,
            textvariable=self.theme_var,
            values=["dark", "light", "high_contrast"],
            state="readonly",
            width=15
        )
        theme_combo.pack(side=tk.LEFT, padx=5)

        # Always on top
        self.always_on_top_var = tk.BooleanVar(
            value=self.current_settings.get("always_on_top", True)
        )
        always_on_top_check = tk.Checkbutton(
            section,
            text="Always on top",
            variable=self.always_on_top_var,
            bg=self.theme.bg_color,
            fg=self.theme.fg_color,
            selectcolor=self.theme.bg_color,
            activebackground=self.theme.bg_color,
            activeforeground=self.theme.fg_color,
            font=("Segoe UI", 9)
        )
        always_on_top_check.pack(anchor=tk.W, padx=10, pady=5)

    def _create_default_alert_section(self, parent):
        """Create default alert settings section."""
        section = tk.LabelFrame(
            parent,
            text="Default Alert Settings",
            bg=self.theme.bg_color,
            fg=self.theme.fg_color,
            font=("Segoe UI", 10, "bold")
        )
        section.pack(fill=tk.X, pady=5)

        default_alert = self.current_settings.get("default_alert", {})
        visual = default_alert.get("visual", {})
        audio = default_alert.get("audio", {})

        # Visual alerts
        visual_frame = tk.LabelFrame(
            section,
            text="Visual Alerts",
            bg=self.theme.bg_color,
            fg=self.theme.fg_color,
            font=("Segoe UI", 9)
        )
        visual_frame.pack(fill=tk.X, padx=10, pady=5)

        self.flash_numbers_var = tk.BooleanVar(value=visual.get("flash_numbers", True))
        self.flash_background_var = tk.BooleanVar(value=visual.get("flash_background", False))
        self.flash_taskbar_var = tk.BooleanVar(value=visual.get("flash_taskbar", True))

        tk.Checkbutton(
            visual_frame,
            text="Flash numbers",
            variable=self.flash_numbers_var,
            bg=self.theme.bg_color,
            fg=self.theme.fg_color,
            selectcolor=self.theme.bg_color,
            font=("Segoe UI", 9)
        ).pack(anchor=tk.W, padx=5, pady=2)

        tk.Checkbutton(
            visual_frame,
            text="Flash background",
            variable=self.flash_background_var,
            bg=self.theme.bg_color,
            fg=self.theme.fg_color,
            selectcolor=self.theme.bg_color,
            font=("Segoe UI", 9)
        ).pack(anchor=tk.W, padx=5, pady=2)

        tk.Checkbutton(
            visual_frame,
            text="Flash taskbar",
            variable=self.flash_taskbar_var,
            bg=self.theme.bg_color,
            fg=self.theme.fg_color,
            selectcolor=self.theme.bg_color,
            font=("Segoe UI", 9)
        ).pack(anchor=tk.W, padx=5, pady=2)

        # Audio alert
        audio_frame = tk.LabelFrame(
            section,
            text="Audio Alert",
            bg=self.theme.bg_color,
            fg=self.theme.fg_color,
            font=("Segoe UI", 9)
        )
        audio_frame.pack(fill=tk.X, padx=10, pady=5)

        self.audio_enabled_var = tk.BooleanVar(value=audio.get("enabled", False))
        audio_check = tk.Checkbutton(
            audio_frame,
            text="Enable sound",
            variable=self.audio_enabled_var,
            bg=self.theme.bg_color,
            fg=self.theme.fg_color,
            selectcolor=self.theme.bg_color,
            font=("Segoe UI", 9),
            command=self._toggle_audio_settings
        )
        audio_check.pack(anchor=tk.W, padx=5, pady=2)

        # Sound file selection
        sound_frame = tk.Frame(audio_frame, bg=self.theme.bg_color)
        sound_frame.pack(fill=tk.X, padx=5, pady=2)

        tk.Label(
            sound_frame,
            text="Sound file:",
            bg=self.theme.bg_color,
            fg=self.theme.fg_color,
            font=("Segoe UI", 9)
        ).pack(side=tk.LEFT, padx=5)

        self.sound_file_var = tk.StringVar(value=audio.get("file", ""))
        self.sound_file_entry = tk.Entry(
            sound_frame,
            textvariable=self.sound_file_var,
            width=25,
            state="readonly" if not self.audio_enabled_var.get() else "normal"
        )
        self.sound_file_entry.pack(side=tk.LEFT, padx=5)

        self.browse_button = tk.Button(
            sound_frame,
            text="Browse...",
            command=self._browse_sound_file,
            state="disabled" if not self.audio_enabled_var.get() else "normal"
        )
        self.theme.apply_to_widget(self.browse_button, "button")
        self.browse_button.pack(side=tk.LEFT, padx=5)

        # Volume
        volume_frame = tk.Frame(audio_frame, bg=self.theme.bg_color)
        volume_frame.pack(fill=tk.X, padx=5, pady=2)

        tk.Label(
            volume_frame,
            text="Volume:",
            bg=self.theme.bg_color,
            fg=self.theme.fg_color,
            font=("Segoe UI", 9)
        ).pack(side=tk.LEFT, padx=5)

        self.volume_var = tk.IntVar(value=audio.get("volume", 80))
        self.volume_slider = tk.Scale(
            volume_frame,
            from_=0,
            to=100,
            orient=tk.HORIZONTAL,
            variable=self.volume_var,
            bg=self.theme.bg_color,
            fg=self.theme.fg_color,
            highlightthickness=0,
            state="disabled" if not self.audio_enabled_var.get() else "normal"
        )
        self.volume_slider.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)

        self.volume_label = tk.Label(
            volume_frame,
            text=f"{self.volume_var.get()}%",
            bg=self.theme.bg_color,
            fg=self.theme.fg_color,
            font=("Segoe UI", 9),
            width=5
        )
        self.volume_label.pack(side=tk.LEFT, padx=5)

        # Update volume label when slider changes
        self.volume_var.trace_add("write", lambda *args: self.volume_label.config(
            text=f"{self.volume_var.get()}%"
        ))

    def _toggle_audio_settings(self):
        """Enable/disable audio settings based on checkbox."""
        enabled = self.audio_enabled_var.get()
        state = "normal" if enabled else "disabled"

        self.sound_file_entry.config(state="readonly" if enabled else state)
        self.browse_button.config(state=state)
        self.volume_slider.config(state=state)

    def _browse_sound_file(self):
        """Open file browser for sound file selection."""
        filename = filedialog.askopenfilename(
            parent=self.dialog,
            title="Select sound file",
            filetypes=[
                ("Audio files", "*.wav *.mp3"),
                ("WAV files", "*.wav"),
                ("MP3 files", "*.mp3"),
                ("All files", "*.*")
            ]
        )

        if filename:
            self.sound_file_var.set(filename)

    def _create_buttons(self, parent):
        """Create dialog buttons."""
        button_frame = tk.Frame(parent, bg=self.theme.bg_color)
        button_frame.pack(fill=tk.X, pady=10)

        # Cancel button
        cancel_btn = tk.Button(
            button_frame,
            text="Cancel",
            command=self._on_cancel,
            width=10
        )
        self.theme.apply_to_widget(cancel_btn, "button")
        cancel_btn.pack(side=tk.RIGHT, padx=5)

        # OK button
        ok_btn = tk.Button(
            button_frame,
            text="OK",
            command=self._on_ok,
            width=10
        )
        self.theme.apply_to_widget(ok_btn, "button")
        ok_btn.pack(side=tk.RIGHT, padx=5)

    def _on_ok(self):
        """Handle OK button click."""
        # Build settings dictionary
        self.result = {
            "theme": self.theme_var.get(),
            "always_on_top": self.always_on_top_var.get(),
            "default_alert": {
                "visual": {
                    "flash_numbers": self.flash_numbers_var.get(),
                    "flash_background": self.flash_background_var.get(),
                    "flash_taskbar": self.flash_taskbar_var.get(),
                    "flash_duration_ms": 3000,
                    "flash_interval_ms": 500
                },
                "audio": {
                    "enabled": self.audio_enabled_var.get(),
                    "file": self.sound_file_var.get(),
                    "volume": self.volume_var.get()
                }
            }
        }

        self.dialog.destroy()

    def _on_cancel(self):
        """Handle Cancel button click."""
        self.result = None
        self.dialog.destroy()

    def _center_on_parent(self):
        """Center dialog on parent window with screen bounds checking."""
        self.dialog.update_idletasks()

        # Get parent position and size
        parent_x = self.parent.winfo_x()
        parent_y = self.parent.winfo_y()
        parent_width = self.parent.winfo_width()
        parent_height = self.parent.winfo_height()

        # Get dialog size
        dialog_width = self.dialog.winfo_width()
        dialog_height = self.dialog.winfo_height()

        # Calculate center position
        x = parent_x + (parent_width - dialog_width) // 2
        y = parent_y + (parent_height - dialog_height) // 2

        # Get screen dimensions
        screen_width = self.dialog.winfo_screenwidth()
        screen_height = self.dialog.winfo_screenheight()

        # Clamp to screen bounds
        x = max(0, min(x, screen_width - dialog_width))
        y = max(0, min(y, screen_height - dialog_height))

        self.dialog.geometry(f"+{x}+{y}")

    def show(self) -> Optional[Dict[str, Any]]:
        """
        Show the dialog and wait for result.

        Returns:
            Updated settings dictionary if OK clicked, None if cancelled
        """
        self.dialog.wait_window()
        return self.result
