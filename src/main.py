"""mmMCounter - Main entry point."""

import os
import sys

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.core.timer import Timer
from src.core.timer_manager import TimerManager
from src.config.config_manager import ConfigManager
from src.config.defaults import DEFAULT_PROFILE

def get_config_dir():
    """Get configuration directory path."""
    if getattr(sys, 'frozen', False):
        # Running as compiled executable
        base_dir = os.path.dirname(sys.executable)
    else:
        # Running as script
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    config_dir = os.path.join(base_dir, 'configs')
    os.makedirs(config_dir, exist_ok=True)
    return config_dir


def test_timer_functionality():
    """
    Test core timer functionality (Phase 1 milestone).

    This is a temporary test function. Will be replaced with GUI in Phase 2.
    """
    print("=== mmMCounter Phase 1: Core Foundation Test ===\n")

    # Initialize config manager
    config_dir = get_config_dir()
    config_manager = ConfigManager(config_dir)

    # Create default profile if needed
    config_manager.create_default_profile()

    print(f"Config directory: {config_dir}")
    print(f"Available profiles: {config_manager.list_profiles()}\n")

    # Load default profile
    profile = config_manager.load_profile("default")
    if profile:
        print(f"Loaded profile: {profile['profile_name']}")
        print(f"Theme: {profile['global_settings']['theme']}\n")

    # Create timer manager
    timer_manager = TimerManager()

    # Create test timers
    timer1 = Timer(label="Test Timer 1", duration=5)  # 5 seconds for testing
    timer2 = Timer(label="Test Timer 2", duration=10)  # 10 seconds

    timer_manager.add_timer(timer1)
    timer_manager.add_timer(timer2)

    print(f"Created {len(timer_manager)} timers:")
    for timer in timer_manager.get_all_timers():
        print(f"  - {timer.label}: {timer.get_display_time()}")

    # Test serialization
    timer_data = timer_manager.to_dict_list()
    print(f"\nSerialized timer data:")
    print(f"  Timer count: {len(timer_data)}")

    # Test save to profile
    profile['timers'] = timer_data
    config_manager.save_profile("test_profile", profile)
    print(f"  Saved to profile: test_profile")

    # Test load from profile
    loaded_profile = config_manager.load_profile("test_profile")
    if loaded_profile:
        print(f"  Loaded profile successfully")

    print("\n[OK] Phase 1 Milestone: Core timer logic and config management working!")
    print("\nNext phase: Build UI with Tkinter (Phase 2)")


def main():
    """Main application entry point."""
    print("mmMCounter v0.1.0")
    print("Money-Making-Meta Counter for Minecraft\n")

    # For Phase 1, just run tests
    test_timer_functionality()


if __name__ == "__main__":
    main()
