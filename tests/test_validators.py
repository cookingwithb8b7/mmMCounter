"""Unit tests for validation utilities."""

import unittest
from src.utils.validators import (
    validate_profile_name,
    validate_timer_label,
    validate_duration,
    parse_duration_string,
    validate_hotkey_string,
    validate_volume,
    sanitize_filename
)


class TestValidators(unittest.TestCase):
    """Test cases for input validation functions."""

    def test_validate_profile_name_valid(self):
        """Test valid profile names."""
        is_valid, msg = validate_profile_name("MyProfile")
        self.assertTrue(is_valid)
        self.assertEqual(msg, "")

        is_valid, msg = validate_profile_name("Profile_123")
        self.assertTrue(is_valid)

    def test_validate_profile_name_empty(self):
        """Test empty profile name."""
        is_valid, msg = validate_profile_name("")
        self.assertFalse(is_valid)
        self.assertIn("empty", msg.lower())

    def test_validate_profile_name_too_long(self):
        """Test profile name too long."""
        long_name = "a" * 51
        is_valid, msg = validate_profile_name(long_name)
        self.assertFalse(is_valid)
        self.assertIn("long", msg.lower())

    def test_validate_profile_name_invalid_chars(self):
        """Test profile name with invalid characters."""
        is_valid, msg = validate_profile_name("My<Profile>")
        self.assertFalse(is_valid)
        self.assertIn("invalid", msg.lower())

        is_valid, msg = validate_profile_name("Profile/Name")
        self.assertFalse(is_valid)

    def test_validate_profile_name_reserved(self):
        """Test reserved profile names."""
        is_valid, msg = validate_profile_name("CON")
        self.assertFalse(is_valid)
        self.assertIn("reserved", msg.lower())

        is_valid, msg = validate_profile_name("NUL")
        self.assertFalse(is_valid)

    def test_validate_timer_label_valid(self):
        """Test valid timer labels."""
        is_valid, msg = validate_timer_label("Pearl")
        self.assertTrue(is_valid)
        self.assertEqual(msg, "")

    def test_validate_timer_label_empty(self):
        """Test empty timer label."""
        is_valid, msg = validate_timer_label("")
        self.assertFalse(is_valid)
        self.assertIn("empty", msg.lower())

    def test_validate_timer_label_too_long(self):
        """Test timer label too long."""
        long_label = "a" * 31
        is_valid, msg = validate_timer_label(long_label)
        self.assertFalse(is_valid)
        self.assertIn("long", msg.lower())

    def test_validate_duration_valid(self):
        """Test valid durations."""
        is_valid, msg = validate_duration(60)
        self.assertTrue(is_valid)
        self.assertEqual(msg, "")

        is_valid, msg = validate_duration(3600)
        self.assertTrue(is_valid)

    def test_validate_duration_negative(self):
        """Test negative duration."""
        is_valid, msg = validate_duration(-1)
        self.assertFalse(is_valid)
        self.assertIn("positive", msg.lower())

    def test_validate_duration_too_long(self):
        """Test duration exceeding 24 hours."""
        is_valid, msg = validate_duration(86401)
        self.assertFalse(is_valid)
        self.assertIn("long", msg.lower())

    def test_parse_duration_string_seconds(self):
        """Test parsing duration as plain seconds."""
        self.assertEqual(parse_duration_string("240"), 240)
        self.assertEqual(parse_duration_string("60"), 60)

    def test_parse_duration_string_mm_ss(self):
        """Test parsing MM:SS format."""
        self.assertEqual(parse_duration_string("04:30"), 270)
        self.assertEqual(parse_duration_string("1:30"), 90)
        self.assertEqual(parse_duration_string("00:45"), 45)

    def test_parse_duration_string_hh_mm_ss(self):
        """Test parsing HH:MM:SS format."""
        self.assertEqual(parse_duration_string("01:30:15"), 5415)
        self.assertEqual(parse_duration_string("0:04:30"), 270)

    def test_parse_duration_string_invalid(self):
        """Test parsing invalid duration strings."""
        self.assertIsNone(parse_duration_string("abc"))
        self.assertIsNone(parse_duration_string(""))
        self.assertIsNone(parse_duration_string("1:2:3:4"))
        self.assertIsNone(parse_duration_string("-10"))
        self.assertIsNone(parse_duration_string("00:00"))

    def test_validate_hotkey_string_valid(self):
        """Test valid hotkey strings."""
        is_valid, msg = validate_hotkey_string("ctrl+shift+1")
        self.assertTrue(is_valid)

        is_valid, msg = validate_hotkey_string("ctrl+f13")
        self.assertTrue(is_valid)

        is_valid, msg = validate_hotkey_string("alt+page_up")
        self.assertTrue(is_valid)

    def test_validate_hotkey_string_empty(self):
        """Test empty hotkey (allowed)."""
        is_valid, msg = validate_hotkey_string("")
        self.assertTrue(is_valid)  # Empty is allowed (disabled hotkey)

    def test_validate_hotkey_string_no_regular_key(self):
        """Test hotkey with only modifiers."""
        is_valid, msg = validate_hotkey_string("ctrl+shift")
        self.assertFalse(is_valid)
        self.assertIn("regular key", msg.lower())

    def test_validate_hotkey_string_multiple_regular_keys(self):
        """Test hotkey with multiple regular keys."""
        is_valid, msg = validate_hotkey_string("ctrl+a+b")
        self.assertFalse(is_valid)
        self.assertIn("one regular key", msg.lower())

    def test_validate_hotkey_string_minecraft_warning(self):
        """Test warning for potentially conflicting hotkeys."""
        is_valid, msg = validate_hotkey_string("w")
        self.assertTrue(is_valid)
        self.assertIn("conflict", msg.lower())

    def test_validate_volume_valid(self):
        """Test valid volume levels."""
        is_valid, msg = validate_volume(50)
        self.assertTrue(is_valid)
        self.assertEqual(msg, "")

        is_valid, msg = validate_volume(0)
        self.assertTrue(is_valid)

        is_valid, msg = validate_volume(100)
        self.assertTrue(is_valid)

    def test_validate_volume_invalid(self):
        """Test invalid volume levels."""
        is_valid, msg = validate_volume(-1)
        self.assertFalse(is_valid)
        self.assertIn("0 and 100", msg)

        is_valid, msg = validate_volume(101)
        self.assertFalse(is_valid)

    def test_sanitize_filename_valid(self):
        """Test sanitizing filenames."""
        self.assertEqual(sanitize_filename("MyProfile"), "MyProfile")
        self.assertEqual(sanitize_filename("Profile 123"), "Profile 123")

    def test_sanitize_filename_invalid_chars(self):
        """Test sanitizing filenames with invalid characters."""
        self.assertEqual(sanitize_filename("My<Profile>"), "My_Profile_")
        self.assertEqual(sanitize_filename("Profile/Name"), "Profile_Name")
        self.assertEqual(sanitize_filename("File:Name"), "File_Name")

    def test_sanitize_filename_empty(self):
        """Test sanitizing empty filename."""
        self.assertEqual(sanitize_filename(""), "unnamed")
        self.assertEqual(sanitize_filename("   "), "unnamed")


if __name__ == '__main__':
    unittest.main()
