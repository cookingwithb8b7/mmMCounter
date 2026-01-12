"""Global hotkey manager using pynput."""

from pynput import keyboard
from typing import Dict, Callable, Set, Optional
import threading


class HotkeyManager:
    """
    Manages global hotkey registration and handling.

    Uses pynput to capture keyboard events even when app is not focused.
    Thread-safe for use with Tkinter.
    """

    def __init__(self):
        """Initialize hotkey manager."""
        self.hotkeys: Dict[str, Dict] = {}  # hotkey_string -> {keys, callback}
        self.listener: Optional[keyboard.Listener] = None
        self.current_keys: Set = set()
        self._lock = threading.Lock()

    def register_hotkey(self, hotkey_string: str, callback: Callable) -> bool:
        """
        Register a global hotkey.

        Args:
            hotkey_string: Hotkey combination (e.g., "ctrl+shift+1")
            callback: Function to call when hotkey is pressed

        Returns:
            True if registered successfully, False if already exists
        """
        if not hotkey_string:
            return False

        with self._lock:
            # Check for conflicts
            if hotkey_string in self.hotkeys:
                print(f"Warning: Hotkey '{hotkey_string}' already registered")
                return False

            # Parse hotkey string
            keys = self._parse_hotkey(hotkey_string)
            if not keys:
                print(f"Error: Invalid hotkey string '{hotkey_string}'")
                return False

            # Register hotkey
            self.hotkeys[hotkey_string] = {
                'keys': keys,
                'callback': callback
            }

            # Restart listener if needed
            self._restart_listener()

            return True

    def unregister_hotkey(self, hotkey_string: str) -> bool:
        """
        Unregister a hotkey.

        Args:
            hotkey_string: Hotkey combination to remove

        Returns:
            True if unregistered, False if not found
        """
        with self._lock:
            if hotkey_string in self.hotkeys:
                del self.hotkeys[hotkey_string]
                return True
            return False

    def clear_all(self):
        """Remove all registered hotkeys."""
        with self._lock:
            self.hotkeys.clear()

    def stop(self):
        """Stop the hotkey listener."""
        if self.listener:
            self.listener.stop()
            self.listener = None

    def _parse_hotkey(self, hotkey_string: str) -> Optional[Set]:
        """
        Parse hotkey string into set of Key objects.

        Args:
            hotkey_string: String like "ctrl+shift+1"

        Returns:
            Set of Key/KeyCode objects or None if invalid
        """
        parts = hotkey_string.lower().strip().split('+')
        keys = set()

        for part in parts:
            part = part.strip()

            if part == 'ctrl':
                keys.add(keyboard.Key.ctrl_l)
                keys.add(keyboard.Key.ctrl_r)
            elif part == 'shift':
                keys.add(keyboard.Key.shift_l)
                keys.add(keyboard.Key.shift_r)
            elif part == 'alt':
                keys.add(keyboard.Key.alt_l)
                keys.add(keyboard.Key.alt_r)
            elif len(part) == 1:
                # Single character key
                try:
                    keys.add(keyboard.KeyCode.from_char(part))
                except:
                    print(f"Warning: Invalid key '{part}'")
                    return None
            else:
                print(f"Warning: Unsupported key '{part}'")
                return None

        return keys if keys else None

    def _restart_listener(self):
        """Restart the keyboard listener."""
        if self.listener:
            self.listener.stop()

        self.listener = keyboard.Listener(
            on_press=self._on_press,
            on_release=self._on_release
        )
        self.listener.start()

    def _on_press(self, key):
        """Handle key press event."""
        self.current_keys.add(key)
        self._check_hotkeys()

    def _on_release(self, key):
        """Handle key release event."""
        if key in self.current_keys:
            self.current_keys.discard(key)

    def _check_hotkeys(self):
        """Check if current key combination matches any registered hotkey."""
        with self._lock:
            for hotkey_string, hotkey_data in self.hotkeys.items():
                required_keys = hotkey_data['keys']

                # Check if all required keys are pressed
                if self._keys_match(required_keys, self.current_keys):
                    # Invoke callback
                    try:
                        hotkey_data['callback']()
                    except Exception as e:
                        print(f"Error in hotkey callback for '{hotkey_string}': {e}")

    def _keys_match(self, required: Set, current: Set) -> bool:
        """
        Check if required keys are pressed.

        Handles modifier key variants (left/right).

        Args:
            required: Set of required keys
            current: Set of currently pressed keys

        Returns:
            True if all required keys are pressed
        """
        # For each required key, check if it or its variant is pressed
        for req_key in required:
            # Check if this exact key is in current keys
            if req_key in current:
                continue

            # For modifier keys, check if either left or right variant is pressed
            if isinstance(req_key, keyboard.Key):
                # It's a modifier - check if any variant is pressed
                if req_key not in current:
                    # Check if we need to match left/right variants
                    key_name = str(req_key)
                    if '_l' in key_name or '_r' in key_name:
                        # Already specific, must match exactly
                        return False
                    # It's a general modifier, already checked above
                    return False
            else:
                # Regular key must match exactly
                return False

        # All required keys found
        return True

    def validate_hotkey(self, hotkey_string: str) -> Dict[str, any]:
        """
        Validate a hotkey string.

        Args:
            hotkey_string: Hotkey to validate

        Returns:
            Dict with 'valid' (bool) and optional 'warning' (str)
        """
        if not hotkey_string:
            return {"valid": False, "error": "Hotkey cannot be empty"}

        # Try to parse
        keys = self._parse_hotkey(hotkey_string)
        if not keys:
            return {"valid": False, "error": "Invalid hotkey format"}

        # Check for conflicts
        if hotkey_string in self.hotkeys:
            return {"valid": False, "error": "Hotkey already in use"}

        # Warn about common Minecraft keys
        minecraft_keys = ['e', 'q', 'w', 'a', 's', 'd', 'space', 'shift', 'ctrl']
        if any(key in hotkey_string.lower() for key in minecraft_keys):
            return {
                "valid": True,
                "warning": "This hotkey may conflict with Minecraft controls"
            }

        return {"valid": True}

    def __repr__(self) -> str:
        """String representation for debugging."""
        return f"HotkeyManager(registered={len(self.hotkeys)})"
