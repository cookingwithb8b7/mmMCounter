"""Unit tests for Timer class."""

import unittest
import time
from src.core.timer import Timer
from src.config.defaults import TimerState


class TestTimer(unittest.TestCase):
    """Test cases for Timer functionality."""

    def test_timer_initialization(self):
        """Test timer creates with correct initial values."""
        timer = Timer(
            label="Test Timer",
            duration=120,
            timer_id="test-1"
        )

        self.assertEqual(timer.id, "test-1")
        self.assertEqual(timer.label, "Test Timer")
        self.assertEqual(timer.duration, 120)
        self.assertEqual(timer.remaining, 120)
        self.assertEqual(timer.state, TimerState.STOPPED)

    def test_timer_start(self):
        """Test starting a timer."""
        timer = Timer("Test", 60)
        timer.start()

        self.assertEqual(timer.state, TimerState.RUNNING)
        self.assertIsNotNone(timer._last_update)

    def test_timer_pause(self):
        """Test pausing a running timer."""
        timer = Timer("Test", 60)
        timer.start()

        # Let it run for a moment
        time.sleep(0.1)
        timer.update(time.time())
        timer.pause()

        self.assertEqual(timer.state, TimerState.PAUSED)
        self.assertLess(timer.remaining, 60)
        self.assertGreater(timer.remaining, 59)

    def test_timer_resume(self):
        """Test resuming a paused timer."""
        timer = Timer("Test", 60)
        timer.start()
        time.sleep(0.1)
        timer.update(time.time())
        timer.pause()

        remaining = timer.remaining
        timer.resume()

        self.assertEqual(timer.state, TimerState.RUNNING)
        self.assertAlmostEqual(timer.remaining, remaining, delta=0.1)

    def test_timer_reset(self):
        """Test resetting a timer."""
        timer = Timer("Test", 60)
        timer.start()
        time.sleep(0.1)
        timer.update(time.time())
        timer.reset()

        self.assertEqual(timer.state, TimerState.STOPPED)
        self.assertEqual(timer.remaining, 60)
        self.assertIsNone(timer._last_update)

    def test_timer_completion(self):
        """Test timer completes when time expires."""
        timer = Timer("Test", 1)
        timer.start()

        # Wait for timer to complete
        time.sleep(1.2)
        current_time = time.time()
        timer.update(current_time)

        self.assertEqual(timer.state, TimerState.COMPLETED)
        self.assertEqual(timer.remaining, 0)

    def test_timer_display_time(self):
        """Test timer display formatting."""
        timer = Timer("Test", 125)  # 2:05

        display = timer.get_display_time()
        self.assertEqual(display, "02:05")

        timer2 = Timer("Test", 3661)  # 61:01
        display = timer2.get_display_time()
        self.assertEqual(display, "61:01")

    def test_timer_toggle_stopped_to_running(self):
        """Test toggle from stopped to running."""
        timer = Timer("Test", 60)
        timer.toggle()

        self.assertEqual(timer.state, TimerState.RUNNING)

    def test_timer_toggle_running_to_paused(self):
        """Test toggle from running to paused."""
        timer = Timer("Test", 60)
        timer.start()
        timer.toggle()

        self.assertEqual(timer.state, TimerState.PAUSED)

    def test_timer_toggle_paused_to_running(self):
        """Test toggle from paused to running."""
        timer = Timer("Test", 60)
        timer.start()
        timer.pause()
        timer.toggle()

        self.assertEqual(timer.state, TimerState.RUNNING)

    def test_timer_to_dict(self):
        """Test timer serialization to dictionary."""
        timer = Timer(
            label="Test Timer",
            duration=120,
            timer_id="test-1",
            hotkey="ctrl+shift+1"
        )

        data = timer.to_dict()

        self.assertEqual(data['id'], "test-1")
        self.assertEqual(data['label'], "Test Timer")
        self.assertEqual(data['duration_seconds'], 120)
        self.assertEqual(data['hotkey'], "ctrl+shift+1")
        self.assertIn('state', data)

    def test_timer_from_dict(self):
        """Test timer deserialization from dictionary."""
        data = {
            'id': 'test-1',
            'label': 'Test Timer',
            'duration_seconds': 120,
            'hotkey': 'ctrl+1',
            'state': {
                'current_state': 'stopped',
                'remaining_seconds': 120
            }
        }

        timer = Timer.from_dict(data)

        self.assertEqual(timer.id, "test-1")
        self.assertEqual(timer.label, "Test Timer")
        self.assertEqual(timer.duration, 120)
        self.assertEqual(timer.hotkey, "ctrl+1")
        self.assertEqual(timer.state, TimerState.STOPPED)


if __name__ == '__main__':
    unittest.main()
