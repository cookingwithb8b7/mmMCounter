"""mmMCounter - Main entry point."""

import os
import sys

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.core.timer_manager import TimerManager
from src.config.config_manager import ConfigManager
from src.ui.main_window import MainWindow
from src.utils.persistence import get_config_dir


def main():
    """Main application entry point."""
    # Initialize config manager
    config_dir = get_config_dir()
    config_manager = ConfigManager(config_dir)

    # Create default profile if it doesn't exist
    config_manager.create_default_profile()

    # Initialize timer manager
    timer_manager = TimerManager()

    # Create and run main window
    app = MainWindow(config_manager, timer_manager)
    app.mainloop()


if __name__ == "__main__":
    main()
