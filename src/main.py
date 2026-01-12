"""mmMCounter - Main entry point."""

import os
import sys
import traceback

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.core.timer_manager import TimerManager
from src.config.config_manager import ConfigManager
from src.ui.main_window import MainWindow
from src.utils.persistence import get_config_dir
from src.utils.logger import setup_logger, get_logger, log_exception, log_startup_validation


def main():
    """Main application entry point."""
    logger = None

    try:
        # Set up logging (beta testing mode - verbose)
        logger = setup_logger(enable_console=True)

        # Install custom exception handler
        sys.excepthook = log_exception

        logger.info('Starting mmMCounter...')

        # Run startup validation
        validation_issues = log_startup_validation()

        if validation_issues:
            logger.warning(f'Starting with {len(validation_issues)} validation warnings')

        # Initialize config manager
        logger.info('Initializing configuration manager...')
        config_dir = get_config_dir()
        logger.info(f'Config directory: {config_dir}')
        config_manager = ConfigManager(config_dir)

        # Create default profile if it doesn't exist
        logger.info('Checking for default profile...')
        config_manager.create_default_profile()
        logger.info('✓ Configuration ready')

        # Initialize timer manager
        logger.info('Initializing timer manager...')
        timer_manager = TimerManager()
        logger.info('✓ Timer manager ready')

        # Create and run main window
        logger.info('Creating main window...')
        app = MainWindow(config_manager, timer_manager)
        logger.info('✓ Main window created')
        logger.info('Starting main event loop...')
        logger.info('=' * 80)

        app.mainloop()

        logger.info('Application closed normally')

    except Exception as e:
        error_msg = f'CRITICAL ERROR during startup: {str(e)}\n{traceback.format_exc()}'

        if logger:
            logger.critical(error_msg)
        else:
            # Logger not set up yet, print to stderr
            print(error_msg, file=sys.stderr)

        # Show error dialog if possible
        try:
            import tkinter as tk
            from tkinter import messagebox
            root = tk.Tk()
            root.withdraw()
            messagebox.showerror(
                'mmMCounter - Critical Error',
                f'Failed to start mmMCounter:\n\n{str(e)}\n\n'
                f'Check logs directory for details.'
            )
        except:
            pass

        sys.exit(1)


if __name__ == "__main__":
    main()
