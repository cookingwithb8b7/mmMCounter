"""Configuration management for loading and saving profiles."""

import json
import os
from typing import Dict, Any, Optional
from src.config.defaults import DEFAULT_PROFILE


class ConfigManager:
    """
    Handles configuration loading, saving, and validation.

    Manages profile JSON files and application state persistence.
    """

    def __init__(self, config_dir: str):
        """
        Initialize configuration manager.

        Args:
            config_dir: Path to configuration directory
        """
        self.config_dir = config_dir
        self.profiles_dir = os.path.join(config_dir, "profiles")
        self.app_state_file = os.path.join(config_dir, "app_state.json")

        # Ensure directories exist
        os.makedirs(self.profiles_dir, exist_ok=True)

    def load_profile(self, profile_name: str) -> Optional[Dict[str, Any]]:
        """
        Load a profile by name.

        Args:
            profile_name: Name of the profile

        Returns:
            Profile configuration dictionary or None if not found
        """
        profile_path = self._get_profile_path(profile_name)

        if not os.path.exists(profile_path):
            return None

        try:
            with open(profile_path, 'r', encoding='utf-8') as f:
                config = json.load(f)
            return self._validate_profile(config)
        except (json.JSONDecodeError, IOError) as e:
            print(f"Error loading profile '{profile_name}': {e}")
            return None

    def save_profile(self, profile_name: str, config: Dict[str, Any]) -> bool:
        """
        Save a profile.

        Args:
            profile_name: Name of the profile
            config: Profile configuration dictionary

        Returns:
            True if saved successfully, False otherwise
        """
        profile_path = self._get_profile_path(profile_name)

        try:
            # Update profile name in config
            config["profile_name"] = profile_name

            with open(profile_path, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=2)
            return True
        except IOError as e:
            print(f"Error saving profile '{profile_name}': {e}")
            return False

    def delete_profile(self, profile_name: str) -> bool:
        """
        Delete a profile.

        Args:
            profile_name: Name of the profile to delete

        Returns:
            True if deleted successfully, False otherwise
        """
        profile_path = self._get_profile_path(profile_name)

        try:
            if os.path.exists(profile_path):
                os.remove(profile_path)
                return True
            return False
        except IOError as e:
            print(f"Error deleting profile '{profile_name}': {e}")
            return False

    def list_profiles(self) -> list[str]:
        """
        List all available profile names.

        Returns:
            List of profile names
        """
        try:
            if not os.path.exists(self.profiles_dir):
                return []

            profiles = []
            for filename in os.listdir(self.profiles_dir):
                if filename.endswith('.json'):
                    profile_name = filename[:-5]  # Remove .json extension
                    profiles.append(profile_name)
            return sorted(profiles)
        except IOError:
            return []

    def create_default_profile(self) -> bool:
        """
        Create the default profile if it doesn't exist.

        Returns:
            True if created, False if already exists
        """
        if self.load_profile("default") is None:
            return self.save_profile("default", DEFAULT_PROFILE.copy())
        return False

    def load_app_state(self) -> Dict[str, Any]:
        """
        Load application state (last active profile, window position, etc.).

        Returns:
            Application state dictionary
        """
        if not os.path.exists(self.app_state_file):
            return {
                "last_active_profile": "default",
                "recent_profiles": ["default"],
                "window_state": {
                    "position": {"x": 100, "y": 100},
                    "size": {"width": 400, "height": 300}
                }
            }

        try:
            with open(self.app_state_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError) as e:
            print(f"Error loading app state: {e}")
            return {}

    def save_app_state(self, state: Dict[str, Any]) -> bool:
        """
        Save application state.

        Args:
            state: Application state dictionary

        Returns:
            True if saved successfully
        """
        try:
            with open(self.app_state_file, 'w', encoding='utf-8') as f:
                json.dump(state, f, indent=2)
            return True
        except IOError as e:
            print(f"Error saving app state: {e}")
            return False

    def _get_profile_path(self, profile_name: str) -> str:
        """Get full path for a profile file."""
        return os.path.join(self.profiles_dir, f"{profile_name}.json")

    def _validate_profile(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate and fill in missing profile configuration values.

        Args:
            config: Profile configuration

        Returns:
            Validated profile configuration
        """
        # Ensure required top-level keys exist
        validated = DEFAULT_PROFILE.copy()

        # Update with loaded config (deep merge for nested dicts)
        if "profile_name" in config:
            validated["profile_name"] = config["profile_name"]

        if "version" in config:
            validated["version"] = config["version"]

        if "global_settings" in config:
            validated["global_settings"].update(config["global_settings"])

        if "timers" in config:
            validated["timers"] = config["timers"]

        return validated

    def export_profile(self, profile_name: str, export_path: str) -> bool:
        """
        Export a profile to a file.

        Args:
            profile_name: Name of profile to export
            export_path: Destination file path

        Returns:
            True if exported successfully
        """
        config = self.load_profile(profile_name)
        if config is None:
            return False

        try:
            with open(export_path, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=2)
            return True
        except IOError as e:
            print(f"Error exporting profile: {e}")
            return False

    def import_profile(self, import_path: str, new_profile_name: Optional[str] = None) -> bool:
        """
        Import a profile from a file.

        Args:
            import_path: Source file path
            new_profile_name: Optional new name (uses name from file if None)

        Returns:
            True if imported successfully
        """
        try:
            with open(import_path, 'r', encoding='utf-8') as f:
                config = json.load(f)

            # Use provided name or name from config
            profile_name = new_profile_name or config.get("profile_name", "imported")

            return self.save_profile(profile_name, config)
        except (json.JSONDecodeError, IOError) as e:
            print(f"Error importing profile: {e}")
            return False
