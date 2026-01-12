"""Input validation utilities for mmMCounter."""

import re
from typing import Optional, Tuple


class ValidationError(Exception):
    """Raised when validation fails."""
    pass


def validate_profile_name(name: str) -> Tuple[bool, str]:
    """
    Validate a profile name.

    Args:
        name: Profile name to validate

    Returns:
        Tuple of (is_valid, error_message)
    """
    if not name:
        return False, "Profile name cannot be empty"

    if len(name) > 50:
        return False, "Profile name too long (max 50 characters)"

    # Disallow filesystem-unsafe characters
    if re.search(r'[<>:"/\\|?*]', name):
        return False, "Profile name contains invalid characters"

    # Reserved names
    reserved = ["CON", "PRN", "AUX", "NUL", "COM1", "COM2", "COM3", "COM4",
                "COM5", "COM6", "COM7", "COM8", "COM9", "LPT1", "LPT2",
                "LPT3", "LPT4", "LPT5", "LPT6", "LPT7", "LPT8", "LPT9"]

    if name.upper() in reserved:
        return False, f"'{name}' is a reserved name"

    return True, ""


def validate_timer_label(label: str) -> Tuple[bool, str]:
    """
    Validate a timer label.

    Args:
        label: Timer label to validate

    Returns:
        Tuple of (is_valid, error_message)
    """
    if not label:
        return False, "Timer label cannot be empty"

    if len(label) > 30:
        return False, "Timer label too long (max 30 characters)"

    return True, ""


def validate_duration(duration: int) -> Tuple[bool, str]:
    """
    Validate a timer duration.

    Args:
        duration: Duration in seconds

    Returns:
        Tuple of (is_valid, error_message)
    """
    if duration <= 0:
        return False, "Duration must be positive"

    if duration > 86400:  # 24 hours
        return False, "Duration too long (max 24 hours)"

    return True, ""


def parse_duration_string(duration_str: str) -> Optional[int]:
    """
    Parse a duration string into seconds.

    Supports formats:
    - "MM:SS" (e.g., "04:30" = 270 seconds)
    - "HH:MM:SS" (e.g., "01:30:15" = 5415 seconds)
    - Seconds as integer (e.g., "240")

    Args:
        duration_str: Duration string to parse

    Returns:
        Duration in seconds, or None if invalid
    """
    duration_str = duration_str.strip()

    # Try parsing as plain integer (seconds)
    try:
        seconds = int(duration_str)
        if seconds > 0:
            return seconds
    except ValueError:
        pass

    # Try parsing as time format
    parts = duration_str.split(':')

    try:
        if len(parts) == 2:
            # MM:SS format
            minutes, seconds = map(int, parts)
            total = minutes * 60 + seconds
            return total if total > 0 else None

        elif len(parts) == 3:
            # HH:MM:SS format
            hours, minutes, seconds = map(int, parts)
            total = hours * 3600 + minutes * 60 + seconds
            return total if total > 0 else None

    except ValueError:
        pass

    return None


def validate_hotkey_string(hotkey: str) -> Tuple[bool, str]:
    """
    Validate a hotkey string format.

    Args:
        hotkey: Hotkey string (e.g., "ctrl+shift+1")

    Returns:
        Tuple of (is_valid, error_message)
    """
    if not hotkey:
        return True, ""  # Empty hotkey is allowed (disabled)

    # Check for valid format
    parts = [p.strip().lower() for p in hotkey.split('+')]

    if len(parts) < 1:
        return False, "Invalid hotkey format"

    # Valid modifiers
    valid_modifiers = {'ctrl', 'shift', 'alt', 'win', 'cmd'}

    # Check each part
    modifiers = []
    regular_keys = []

    for part in parts:
        if part in valid_modifiers:
            modifiers.append(part)
        else:
            regular_keys.append(part)

    # Must have at least one regular key
    if not regular_keys:
        return False, "Hotkey must include at least one regular key"

    # Should not have multiple regular keys
    if len(regular_keys) > 1:
        return False, "Hotkey can only have one regular key"

    # Warn about potentially conflicting keys
    single_key = regular_keys[0]
    if len(modifiers) == 0 and len(single_key) == 1:
        # Single letter/number with no modifiers might conflict with Minecraft
        return True, f"Warning: '{hotkey}' might conflict with Minecraft controls"

    return True, ""


def validate_volume(volume: int) -> Tuple[bool, str]:
    """
    Validate audio volume level.

    Args:
        volume: Volume percentage (0-100)

    Returns:
        Tuple of (is_valid, error_message)
    """
    if volume < 0 or volume > 100:
        return False, "Volume must be between 0 and 100"

    return True, ""


def sanitize_filename(filename: str) -> str:
    """
    Sanitize a filename by removing/replacing unsafe characters.

    Args:
        filename: Original filename

    Returns:
        Sanitized filename
    """
    # Replace unsafe characters with underscore
    sanitized = re.sub(r'[<>:"/\\|?*]', '_', filename)

    # Remove leading/trailing whitespace and dots
    sanitized = sanitized.strip(' .')

    # Ensure not empty
    if not sanitized:
        sanitized = "unnamed"

    return sanitized
