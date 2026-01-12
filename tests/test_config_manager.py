"""Unit tests for ConfigManager."""

import unittest
import os
import tempfile
import shutil
import json
from src.config.config_manager import ConfigManager
from src.config.defaults import DEFAULT_PROFILE


class TestConfigManager(unittest.TestCase):
    """Test cases for ConfigManager functionality."""

    def setUp(self):
        """Set up test fixtures."""
        # Create temporary directory for test configs
        self.test_dir = tempfile.mkdtemp()
        self.config_manager = ConfigManager(self.test_dir)

    def tearDown(self):
        """Clean up test fixtures."""
        # Remove temporary directory
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)

    def test_initialization(self):
        """Test ConfigManager creates necessary directories."""
        self.assertTrue(os.path.exists(self.config_manager.profiles_dir))
        self.assertTrue(os.path.isdir(self.config_manager.profiles_dir))

    def test_save_and_load_profile(self):
        """Test saving and loading a profile."""
        test_profile = DEFAULT_PROFILE.copy()
        test_profile['profile_name'] = 'test_profile'

        # Save profile
        success = self.config_manager.save_profile('test_profile', test_profile)
        self.assertTrue(success)

        # Load profile
        loaded = self.config_manager.load_profile('test_profile')
        self.assertIsNotNone(loaded)
        self.assertEqual(loaded['profile_name'], 'test_profile')

    def test_load_nonexistent_profile(self):
        """Test loading a profile that doesn't exist."""
        loaded = self.config_manager.load_profile('nonexistent')
        self.assertIsNone(loaded)

    def test_delete_profile(self):
        """Test deleting a profile."""
        # Create a profile first
        test_profile = DEFAULT_PROFILE.copy()
        self.config_manager.save_profile('test_delete', test_profile)

        # Delete it
        success = self.config_manager.delete_profile('test_delete')
        self.assertTrue(success)

        # Verify it's gone
        loaded = self.config_manager.load_profile('test_delete')
        self.assertIsNone(loaded)

    def test_delete_nonexistent_profile(self):
        """Test deleting a profile that doesn't exist."""
        success = self.config_manager.delete_profile('nonexistent')
        self.assertFalse(success)

    def test_list_profiles(self):
        """Test listing all profiles."""
        # Create multiple profiles
        for i in range(3):
            profile = DEFAULT_PROFILE.copy()
            profile['profile_name'] = f'profile_{i}'
            self.config_manager.save_profile(f'profile_{i}', profile)

        # List profiles
        profiles = self.config_manager.list_profiles()
        self.assertEqual(len(profiles), 3)
        self.assertIn('profile_0', profiles)
        self.assertIn('profile_1', profiles)
        self.assertIn('profile_2', profiles)

    def test_list_profiles_empty(self):
        """Test listing profiles when none exist."""
        profiles = self.config_manager.list_profiles()
        self.assertEqual(profiles, [])

    def test_create_default_profile(self):
        """Test creating default profile."""
        # Create default profile
        created = self.config_manager.create_default_profile()
        self.assertTrue(created)

        # Verify it exists
        loaded = self.config_manager.load_profile('default')
        self.assertIsNotNone(loaded)
        self.assertEqual(loaded['profile_name'], 'default')

    def test_create_default_profile_already_exists(self):
        """Test creating default profile when it already exists."""
        # Create it once
        self.config_manager.create_default_profile()

        # Try to create again
        created = self.config_manager.create_default_profile()
        self.assertFalse(created)

    def test_export_profile(self):
        """Test exporting a profile to file."""
        # Create a profile
        test_profile = DEFAULT_PROFILE.copy()
        test_profile['profile_name'] = 'export_test'
        self.config_manager.save_profile('export_test', test_profile)

        # Export it
        export_path = os.path.join(self.test_dir, 'exported.json')
        success = self.config_manager.export_profile('export_test', export_path)
        self.assertTrue(success)

        # Verify file exists and contains correct data
        self.assertTrue(os.path.exists(export_path))
        with open(export_path, 'r', encoding='utf-8') as f:
            exported_data = json.load(f)
        self.assertEqual(exported_data['profile_name'], 'export_test')

    def test_import_profile(self):
        """Test importing a profile from file."""
        # Create a test profile file
        test_profile = DEFAULT_PROFILE.copy()
        test_profile['profile_name'] = 'imported'
        import_path = os.path.join(self.test_dir, 'import_test.json')

        with open(import_path, 'w', encoding='utf-8') as f:
            json.dump(test_profile, f)

        # Import it
        success = self.config_manager.import_profile(import_path, 'imported')
        self.assertTrue(success)

        # Verify it was imported
        loaded = self.config_manager.load_profile('imported')
        self.assertIsNotNone(loaded)
        self.assertEqual(loaded['profile_name'], 'imported')

    def test_save_and_load_app_state(self):
        """Test saving and loading application state."""
        test_state = {
            'last_active_profile': 'test_profile',
            'recent_profiles': ['test_profile', 'default'],
            'window_state': {
                'position': {'x': 200, 'y': 100},
                'size': {'width': 500, 'height': 400}
            }
        }

        # Save state
        success = self.config_manager.save_app_state(test_state)
        self.assertTrue(success)

        # Load state
        loaded_state = self.config_manager.load_app_state()
        self.assertEqual(loaded_state['last_active_profile'], 'test_profile')
        self.assertEqual(loaded_state['window_state']['position']['x'], 200)

    def test_profile_validation(self):
        """Test profile validation fills in missing values."""
        # Create incomplete profile
        incomplete_profile = {
            'profile_name': 'incomplete',
            'timers': []
        }

        # Save and load (should be validated)
        self.config_manager.save_profile('incomplete', incomplete_profile)
        loaded = self.config_manager.load_profile('incomplete')

        # Check that defaults were filled in
        self.assertIn('version', loaded)
        self.assertIn('global_settings', loaded)
        self.assertIn('theme', loaded['global_settings'])


if __name__ == '__main__':
    unittest.main()
