"""
Logging utility for mmMCounter
Provides file-based logging for debugging and beta testing
"""

import logging
import os
import sys
from datetime import datetime
from pathlib import Path


def setup_logger(log_level=logging.DEBUG, enable_console=True):
    """
    Set up application-wide logger for beta testing

    Args:
        log_level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        enable_console: Whether to also print logs to console

    Returns:
        Logger instance
    """
    # Create logger
    logger = logging.getLogger('mmMCounter')
    logger.setLevel(log_level)

    # Remove existing handlers to avoid duplicates
    logger.handlers = []

    # Create logs directory if it doesn't exist
    if getattr(sys, 'frozen', False):
        # Running as executable - logs next to exe
        log_dir = Path(sys.executable).parent / 'logs'
    else:
        # Running as script - logs in project root
        log_dir = Path(__file__).parent.parent.parent / 'logs'

    log_dir.mkdir(exist_ok=True)

    # Create file handler with timestamp
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    log_file = log_dir / f'mmMCounter_{timestamp}.log'
    file_handler = logging.FileHandler(log_file, encoding='utf-8')
    file_handler.setLevel(log_level)

    # Create console handler (optional)
    if enable_console or not getattr(sys, 'frozen', False):
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(logging.INFO)

        # Console format (simpler)
        console_format = logging.Formatter(
            '%(levelname)s: %(message)s'
        )
        console_handler.setFormatter(console_format)
        logger.addHandler(console_handler)

    # File format (detailed)
    file_format = logging.Formatter(
        '%(asctime)s | %(levelname)-8s | %(name)s | %(funcName)s:%(lineno)d | %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    file_handler.setFormatter(file_format)
    logger.addHandler(file_handler)

    # Log startup info
    logger.info('=' * 80)
    logger.info('mmMCounter - Beta Logging Started')
    logger.info(f'Log file: {log_file}')
    logger.info(f'Python version: {sys.version}')
    logger.info(f'Running as executable: {getattr(sys, "frozen", False)}')
    logger.info(f'Working directory: {os.getcwd()}')
    logger.info('=' * 80)

    return logger


def get_logger():
    """Get the application logger instance"""
    return logging.getLogger('mmMCounter')


def log_exception(exc_type, exc_value, exc_traceback):
    """
    Custom exception handler that logs unhandled exceptions

    Usage:
        import sys
        sys.excepthook = log_exception
    """
    if issubclass(exc_type, KeyboardInterrupt):
        # Don't log keyboard interrupts
        sys.__excepthook__(exc_type, exc_value, exc_traceback)
        return

    logger = get_logger()
    logger.critical(
        'Unhandled exception:',
        exc_info=(exc_type, exc_value, exc_traceback)
    )


def log_startup_validation():
    """
    Log validation checks for application startup
    Helps identify missing files, config issues, etc.
    """
    logger = get_logger()
    logger.info('Running startup validation...')

    issues = []

    # Check sound files
    if getattr(sys, 'frozen', False):
        base_path = Path(sys._MEIPASS)  # PyInstaller temp directory
    else:
        base_path = Path(__file__).parent.parent.parent

    sounds_dir = base_path / 'assets' / 'sounds'
    expected_sounds = [
        'beepbeep.wav',
        'sonar.wav',
        'sweetalertsound1.wav',
        'alertshort.wav',
        'phoneoffhooktone.wav',
        'CREDITS.txt'
    ]

    if sounds_dir.exists():
        logger.info(f'[OK] Sounds directory found: {sounds_dir}')
        for sound in expected_sounds:
            sound_path = sounds_dir / sound
            if sound_path.exists():
                logger.info(f'  [OK] {sound} ({sound_path.stat().st_size} bytes)')
            else:
                logger.warning(f'  [X] MISSING: {sound}')
                issues.append(f'Missing sound file: {sound}')
    else:
        logger.error(f'[X] Sounds directory NOT FOUND: {sounds_dir}')
        issues.append('Sounds directory missing')

    # Check fonts directory
    fonts_dir = base_path / 'assets' / 'fonts'
    if fonts_dir.exists():
        logger.info(f'[OK] Fonts directory found: {fonts_dir}')
    else:
        logger.warning(f'[X] Fonts directory NOT FOUND: {fonts_dir}')
        issues.append('Fonts directory missing (non-critical)')

    # Check config directory
    if getattr(sys, 'frozen', False):
        config_dir = Path(sys.executable).parent / 'configs'
    else:
        config_dir = base_path / 'configs'

    if config_dir.exists():
        logger.info(f'[OK] Config directory found: {config_dir}')
    else:
        logger.info(f'[i] Config directory will be created: {config_dir}')

    # Check default profile
    default_profile = base_path / 'configs' / 'profiles' / 'default.json'
    if default_profile.exists():
        logger.info(f'[OK] Default profile found: {default_profile}')
    else:
        logger.warning(f'[X] Default profile NOT FOUND: {default_profile}')
        issues.append('Default profile missing')

    # Summary
    if issues:
        logger.warning(f'Startup validation found {len(issues)} issue(s):')
        for issue in issues:
            logger.warning(f'  - {issue}')
    else:
        logger.info('[OK] All startup validation checks passed')

    logger.info('Startup validation complete.')
    logger.info('-' * 80)

    return issues
