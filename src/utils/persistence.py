"""Persistence utilities for config directory handling."""

import sys
import os


def get_config_dir() -> str:
    """
    Get configuration directory path.

    Handles both script execution and PyInstaller frozen executable.

    Returns:
        Path to config directory
    """
    if getattr(sys, 'frozen', False):
        # Running as compiled executable
        base_dir = os.path.dirname(sys.executable)
    else:
        # Running as script - go up from src/utils to project root
        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

    config_dir = os.path.join(base_dir, 'configs')
    os.makedirs(config_dir, exist_ok=True)
    return config_dir


def get_assets_dir() -> str:
    """
    Get assets directory path.

    Handles both script execution and PyInstaller frozen executable.

    Returns:
        Path to assets directory
    """
    if getattr(sys, 'frozen', False):
        # Running as compiled executable - assets bundled with exe
        base_dir = sys._MEIPASS  # PyInstaller temp directory
    else:
        # Running as script
        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

    assets_dir = os.path.join(base_dir, 'assets')
    return assets_dir
