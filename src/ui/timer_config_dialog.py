"""Timer configuration dialog for per-timer settings."""

import tkinter as tk
from tkinter import messagebox
from src.core.timer import Timer


class TimerConfigDialog(tk.Toplevel):
    """
    Modal dialog for configuring individual timer settings.

    Allows editing:
    - Label
    - Duration
    - Hotkey
    - Alert settings (visual/audio)
    - Font settings (placeholder for Phase 5)
    """

    def __init__(self, parent, timer: Timer, theme, hotkey_manager=None):
        """
        Initialize timer config dialog.

        Args:
            parent: Parent window
            timer: Timer to configure
            theme: Theme instance
            hotkey_manager: HotkeyManager for validation (optional)
        """
        super().__init__(parent)

        self.timer = timer
        self.theme = theme
        self.hotkey_manager = hotkey_manager
        self.result = None  # Will be set to timer config dict if OK clicked

        # Window setup
        self.title(f"Configure Timer: {timer.label}")
        self.configure(bg=theme.bg_color)
        self.resizable(False, False)

        # Make modal
        self.transient(parent)
        self.grab_set()

        # Create UI
        self._create_widgets()

        # Center on parent with screen bounds checking
        self.update_idletasks()

        # Calculate centered position
        x = parent.winfo_x() + (parent.winfo_width() // 2) - (self.winfo_width() // 2)
        y = parent.winfo_y() + (parent.winfo_height() // 2) - (self.winfo_height() // 2)

        # Get screen dimensions
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        dialog_width = self.winfo_width()
        dialog_height = self.winfo_height()

        # Clamp X position (keep within screen bounds)
        x = max(0, min(x, screen_width - dialog_width))

        # Clamp Y position (ensure title bar is always accessible)
        # Keep at least 30 pixels from top for title bar, and keep bottom visible
        min_y = 0
        max_y = screen_height - dialog_height
        y = max(min_y, min(y, max_y))

        self.geometry(f"+{x}+{y}")

    def _create_widgets(self):
        """Create all dialog widgets."""
        # Main frame
        main_frame = tk.Frame(self, bg=self.theme.bg_color, padx=20, pady=20)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Label
        tk.Label(
            main_frame,
            text="Timer Label:",
            bg=self.theme.bg_color,
            fg=self.theme.fg_color
        ).grid(row=0, column=0, sticky='w', pady=5)

        self.label_entry = tk.Entry(main_frame, width=30)
        self.label_entry.insert(0, self.timer.label)
        self.theme.apply_to_widget(self.label_entry, "entry")
        self.label_entry.grid(row=0, column=1, pady=5)

        # Duration
        tk.Label(
            main_frame,
            text="Duration (MM:SS):",
            bg=self.theme.bg_color,
            fg=self.theme.fg_color
        ).grid(row=1, column=0, sticky='w', pady=5)

        duration_frame = tk.Frame(main_frame, bg=self.theme.bg_color)
        duration_frame.grid(row=1, column=1, sticky='w', pady=5)

        self.minutes_entry = tk.Entry(duration_frame, width=5)
        self.seconds_entry = tk.Entry(duration_frame, width=5)

        # Convert duration to MM:SS
        minutes = int(self.timer.duration) // 60
        seconds = int(self.timer.duration) % 60

        self.minutes_entry.insert(0, str(minutes))
        self.seconds_entry.insert(0, str(seconds))

        self.theme.apply_to_widget(self.minutes_entry, "entry")
        self.theme.apply_to_widget(self.seconds_entry, "entry")

        self.minutes_entry.pack(side=tk.LEFT)
        tk.Label(duration_frame, text=":", bg=self.theme.bg_color, fg=self.theme.fg_color).pack(side=tk.LEFT)
        self.seconds_entry.pack(side=tk.LEFT)

        # Hotkey
        tk.Label(
            main_frame,
            text="Hotkey:",
            bg=self.theme.bg_color,
            fg=self.theme.fg_color
        ).grid(row=2, column=0, sticky='w', pady=5)

        hotkey_frame = tk.Frame(main_frame, bg=self.theme.bg_color)
        hotkey_frame.grid(row=2, column=1, sticky='w', pady=5)

        # Current hotkey display
        self.hotkey_var = tk.StringVar(value=self.timer.hotkey or "None")
        self.hotkey_display = tk.Label(
            hotkey_frame,
            textvariable=self.hotkey_var,
            width=20,
            bg=self.theme.entry_bg,
            fg=self.theme.entry_fg,
            anchor='w',
            relief='sunken',
            padx=5,
            pady=3
        )
        self.hotkey_display.pack(side=tk.LEFT, padx=(0, 5))

        # Capture button
        self.capture_button = tk.Button(
            hotkey_frame,
            text="Press keys...",
            width=12,
            command=self._start_hotkey_capture
        )
        self.theme.apply_to_widget(self.capture_button, "button")
        self.capture_button.pack(side=tk.LEFT, padx=2)

        # Clear button
        clear_button = tk.Button(
            hotkey_frame,
            text="X",
            width=3,
            command=self._clear_hotkey
        )
        self.theme.apply_to_widget(clear_button, "button")
        clear_button.pack(side=tk.LEFT, padx=2)

        # Hotkey capture state
        self.capturing_hotkey = False
        self.captured_keys = set()
        self.hotkey_listener = None

        # Visual Alerts section
        tk.Label(
            main_frame,
            text="Visual Alerts:",
            bg=self.theme.bg_color,
            fg=self.theme.fg_color,
            font=('Arial', 10, 'bold')
        ).grid(row=3, column=0, columnspan=2, sticky='w', pady=(15, 5))

        alert_config = self.timer.alert_config or {}
        visual_config = alert_config.get('visual', {})

        self.flash_numbers_var = tk.BooleanVar(value=visual_config.get('flash_numbers', True))
        self.flash_background_var = tk.BooleanVar(value=visual_config.get('flash_background', True))
        self.flash_taskbar_var = tk.BooleanVar(value=visual_config.get('flash_taskbar', True))

        tk.Checkbutton(
            main_frame,
            text="Flash timer numbers",
            variable=self.flash_numbers_var,
            bg=self.theme.bg_color,
            fg=self.theme.fg_color,
            selectcolor=self.theme.button_bg
        ).grid(row=4, column=0, columnspan=2, sticky='w')

        tk.Checkbutton(
            main_frame,
            text="Flash timer background",
            variable=self.flash_background_var,
            bg=self.theme.bg_color,
            fg=self.theme.fg_color,
            selectcolor=self.theme.button_bg
        ).grid(row=5, column=0, columnspan=2, sticky='w')

        tk.Checkbutton(
            main_frame,
            text="Flash taskbar",
            variable=self.flash_taskbar_var,
            bg=self.theme.bg_color,
            fg=self.theme.fg_color,
            selectcolor=self.theme.button_bg
        ).grid(row=6, column=0, columnspan=2, sticky='w')

        # Audio Alerts section
        tk.Label(
            main_frame,
            text="Audio Alert:",
            bg=self.theme.bg_color,
            fg=self.theme.fg_color,
            font=('Arial', 10, 'bold')
        ).grid(row=7, column=0, columnspan=2, sticky='w', pady=(15, 5))

        audio_config = alert_config.get('audio', {})

        self.audio_enabled_var = tk.BooleanVar(value=audio_config.get('enabled', False))
        self.audio_volume_var = tk.IntVar(value=audio_config.get('volume', 80))
        self.audio_file_var = tk.StringVar(value=audio_config.get('file', ''))

        tk.Checkbutton(
            main_frame,
            text="Enable sound",
            variable=self.audio_enabled_var,
            bg=self.theme.bg_color,
            fg=self.theme.fg_color,
            selectcolor=self.theme.button_bg
        ).grid(row=8, column=0, columnspan=2, sticky='w')

        # Volume slider
        volume_frame = tk.Frame(main_frame, bg=self.theme.bg_color)
        volume_frame.grid(row=9, column=0, columnspan=2, sticky='ew', pady=5)

        tk.Label(
            volume_frame,
            text="Volume:",
            bg=self.theme.bg_color,
            fg=self.theme.fg_color
        ).pack(side=tk.LEFT)

        volume_slider = tk.Scale(
            volume_frame,
            from_=0,
            to=100,
            orient=tk.HORIZONTAL,
            variable=self.audio_volume_var,
            bg=self.theme.bg_color,
            fg=self.theme.fg_color,
            highlightthickness=0
        )
        volume_slider.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)

        # Sound file selection
        sound_frame = tk.Frame(main_frame, bg=self.theme.bg_color)
        sound_frame.grid(row=10, column=0, columnspan=2, sticky='ew', pady=5)

        # Get current sound file (or default if empty)
        current_sound = audio_config.get('file', 'assets/sounds/beepbeep.wav')
        # Extract just the filename for display
        sound_filename = current_sound.split('/')[-1] if current_sound else 'beepbeep.wav'

        tk.Label(
            sound_frame,
            text=f"Sound: {sound_filename}",
            bg=self.theme.bg_color,
            fg=self.theme.fg_color,
            font=('Arial', 9)
        ).pack(side=tk.LEFT)

        # Buttons
        button_frame = tk.Frame(main_frame, bg=self.theme.bg_color)
        button_frame.grid(row=11, column=0, columnspan=2, pady=(20, 0))

        ok_button = tk.Button(button_frame, text="OK", width=10, command=self._on_ok)
        cancel_button = tk.Button(button_frame, text="Cancel", width=10, command=self._on_cancel)

        self.theme.apply_to_widget(ok_button, "button")
        self.theme.apply_to_widget(cancel_button, "button")

        ok_button.pack(side=tk.LEFT, padx=5)
        cancel_button.pack(side=tk.LEFT, padx=5)

    def _on_ok(self):
        """Handle OK button click."""
        # Validate inputs
        label = self.label_entry.get().strip()
        if not label:
            messagebox.showerror("Error", "Timer label cannot be empty")
            return

        # Parse duration
        try:
            minutes = int(self.minutes_entry.get())
            seconds = int(self.seconds_entry.get())

            if minutes < 0 or seconds < 0:
                raise ValueError("Duration cannot be negative")

            duration = minutes * 60 + seconds

            if duration == 0:
                messagebox.showerror("Error", "Duration must be greater than 0")
                return

        except ValueError:
            messagebox.showerror("Error", "Invalid duration format")
            return

        # Get hotkey from captured value
        hotkey = self.hotkey_var.get()
        if hotkey == "None":
            hotkey = None

        if hotkey and self.hotkey_manager:
            validation = self.hotkey_manager.validate_hotkey(hotkey)
            if not validation.get('valid', False):
                messagebox.showerror("Error", f"Invalid hotkey: {validation.get('error', 'Unknown error')}")
                return
            elif 'warning' in validation:
                if not messagebox.askyesno("Warning", f"{validation['warning']}\n\nContinue anyway?"):
                    return

        # Build result config
        self.result = {
            'label': label,
            'duration': duration,
            'hotkey': hotkey,
            'alert': {
                'visual': {
                    'flash_numbers': self.flash_numbers_var.get(),
                    'flash_background': self.flash_background_var.get(),
                    'flash_window': False,
                    'flash_taskbar': self.flash_taskbar_var.get(),
                    'flash_duration_ms': 3000,
                    'flash_interval_ms': 500
                },
                'audio': {
                    'enabled': self.audio_enabled_var.get(),
                    'file': self.audio_file_var.get(),
                    'volume': self.audio_volume_var.get()
                }
            }
        }

        self.destroy()

    def _on_cancel(self):
        """Handle Cancel button click."""
        self.result = None
        self.destroy()

    def show(self):
        """
        Show dialog and wait for result.

        Returns:
            Config dict if OK clicked, None if cancelled
        """
        self.wait_window()
        return self.result

    def _start_hotkey_capture(self):
        """Start capturing hotkey input."""
        from pynput import keyboard

        # Update button text
        self.capture_button.configure(text="Listening... (Esc to cancel)")
        self.capturing_hotkey = True
        self.captured_keys = set()

        def on_press(key):
            if not self.capturing_hotkey:
                return False  # Stop listener

            # Add key to captured set
            self.captured_keys.add(key)

            # Build hotkey string
            hotkey_string = self._build_hotkey_string(self.captured_keys)

            # Update display in real-time
            self.hotkey_var.set(hotkey_string)

        def on_release(key):
            if not self.capturing_hotkey:
                return False  # Stop listener

            # Check for Escape to cancel
            if key == keyboard.Key.esc:
                self._stop_hotkey_capture()
                return False  # Stop listener

            # If we have at least one key, stop capturing
            if len(self.captured_keys) > 0:
                # Small delay to capture all keys
                self.after(100, self._stop_hotkey_capture)
                return False  # Stop listener

        # Start listener in background
        self.hotkey_listener = keyboard.Listener(on_press=on_press, on_release=on_release)
        self.hotkey_listener.start()

    def _stop_hotkey_capture(self):
        """Stop capturing hotkey input."""
        self.capturing_hotkey = False

        # Stop listener if running
        if self.hotkey_listener:
            self.hotkey_listener.stop()
            self.hotkey_listener = None

        # Reset button text
        self.capture_button.configure(text="Press keys...")

        # If no keys captured, don't change the hotkey
        if len(self.captured_keys) == 0:
            # Restore previous value or "None"
            if self.timer.hotkey:
                self.hotkey_var.set(self.timer.hotkey)
            else:
                self.hotkey_var.set("None")

    def _clear_hotkey(self):
        """Clear the current hotkey."""
        self.hotkey_var.set("None")
        self.captured_keys = set()

    def _build_hotkey_string(self, keys):
        """
        Build a hotkey string from captured keys.

        Args:
            keys: Set of pynput Key/KeyCode objects

        Returns:
            Hotkey string like "ctrl+shift+1"
        """
        from pynput import keyboard

        modifiers = []
        regular_keys = []
        has_modifiers = False

        # Map of virtual key codes to readable names (physical keys)
        vk_to_char = {
            # Number row
            48: '0', 49: '1', 50: '2', 51: '3', 52: '4',
            53: '5', 54: '6', 55: '7', 56: '8', 57: '9',
            # Letter keys (A-Z)
            65: 'a', 66: 'b', 67: 'c', 68: 'd', 69: 'e', 70: 'f',
            71: 'g', 72: 'h', 73: 'i', 74: 'j', 75: 'k', 76: 'l',
            77: 'm', 78: 'n', 79: 'o', 80: 'p', 81: 'q', 82: 'r',
            83: 's', 84: 't', 85: 'u', 86: 'v', 87: 'w', 88: 'x',
            89: 'y', 90: 'z',
            # Function keys (F1-F24)
            112: 'f1', 113: 'f2', 114: 'f3', 115: 'f4',
            116: 'f5', 117: 'f6', 118: 'f7', 119: 'f8',
            120: 'f9', 121: 'f10', 122: 'f11', 123: 'f12',
            124: 'f13', 125: 'f14', 126: 'f15', 127: 'f16',
            128: 'f17', 129: 'f18', 130: 'f19', 131: 'f20',
            132: 'f21', 133: 'f22', 134: 'f23', 135: 'f24',
            # Navigation keys
            33: 'page_up', 34: 'page_down',
            35: 'end', 36: 'home',
            45: 'insert', 46: 'delete',
            # Arrow keys
            37: 'left', 38: 'up', 39: 'right', 40: 'down',
            # Numpad
            96: 'num0', 97: 'num1', 98: 'num2', 99: 'num3',
            100: 'num4', 101: 'num5', 102: 'num6', 103: 'num7',
            104: 'num8', 105: 'num9',
            106: 'num_multiply', 107: 'num_add', 109: 'num_subtract',
            110: 'num_decimal', 111: 'num_divide',
            # Special keys
            144: 'num_lock', 145: 'scroll_lock',
            19: 'pause', 44: 'print_screen'
        }

        # First pass: collect modifiers
        for key in keys:
            if key in (keyboard.Key.ctrl_l, keyboard.Key.ctrl_r, keyboard.Key.ctrl):
                if 'ctrl' not in modifiers:
                    modifiers.append('ctrl')
                    has_modifiers = True
            elif key in (keyboard.Key.shift_l, keyboard.Key.shift_r, keyboard.Key.shift):
                if 'shift' not in modifiers:
                    modifiers.append('shift')
                    has_modifiers = True
            elif key in (keyboard.Key.alt_l, keyboard.Key.alt_r, keyboard.Key.alt):
                if 'alt' not in modifiers:
                    modifiers.append('alt')
                    has_modifiers = True

        # Second pass: collect regular keys
        # If modifiers are present, ALWAYS use VK code to get physical key
        # This prevents Shift+1 from becoming "!" instead of "1"
        for key in keys:
            # Skip modifier keys
            if key in (keyboard.Key.ctrl_l, keyboard.Key.ctrl_r, keyboard.Key.ctrl,
                      keyboard.Key.shift_l, keyboard.Key.shift_r, keyboard.Key.shift,
                      keyboard.Key.alt_l, keyboard.Key.alt_r, keyboard.Key.alt):
                continue

            # Check if it's a named special key (e.g., Key.page_up, Key.f13)
            if isinstance(key, keyboard.Key):
                key_name = key.name.lower()
                regular_keys.append(key_name)
                continue

            # Always prefer VK code for physical key
            if hasattr(key, 'vk') and key.vk is not None:
                vk = key.vk
                if vk in vk_to_char:
                    # Known physical key (letter, number, or special)
                    regular_keys.append(vk_to_char[vk])
                else:
                    # Unknown VK - try to get readable name
                    key_str = str(key).replace('Key.', '').replace('<', '').replace('>', '').replace("'", '')
                    if key_str and key_str not in modifiers:
                        regular_keys.append(key_str.lower())
            elif hasattr(key, 'char') and key.char and not has_modifiers:
                # Only use char if NO modifiers (plain key press)
                regular_keys.append(key.char.lower())

        # Sort modifiers for consistency
        modifier_order = {'ctrl': 0, 'shift': 1, 'alt': 2}
        modifiers.sort(key=lambda x: modifier_order.get(x, 99))

        # Build string
        parts = modifiers + regular_keys

        if len(parts) == 0:
            return "None"

        return '+'.join(parts)
