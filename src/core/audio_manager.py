"""Audio manager for sound playback using pygame.mixer."""

import pygame
import os
from typing import Dict, Optional


class AudioManager:
    """
    Manages audio playback with volume control.

    Uses pygame.mixer for reliable audio playback with .wav and .mp3 support.
    """

    def __init__(self):
        """Initialize audio manager."""
        self.initialized = False
        self.sounds: Dict[str, pygame.mixer.Sound] = {}  # file_path -> Sound object

        try:
            pygame.mixer.init()
            self.initialized = True
        except Exception as e:
            print(f"Warning: Failed to initialize audio: {e}")

    def load_sound(self, file_path: str) -> bool:
        """
        Load a sound file.

        Args:
            file_path: Path to sound file (.wav or .mp3)

        Returns:
            True if loaded successfully
        """
        if not self.initialized:
            return False

        if not os.path.exists(file_path):
            print(f"Warning: Sound file not found: {file_path}")
            return False

        try:
            # Load sound
            sound = pygame.mixer.Sound(file_path)
            self.sounds[file_path] = sound
            return True
        except Exception as e:
            print(f"Error loading sound '{file_path}': {e}")
            return False

    def play_sound(self, file_path: str, volume: float = 1.0) -> bool:
        """
        Play a sound file.

        Args:
            file_path: Path to sound file
            volume: Volume level (0.0 to 1.0)

        Returns:
            True if played successfully
        """
        if not self.initialized:
            return False

        # Load sound if not already loaded
        if file_path not in self.sounds:
            if not self.load_sound(file_path):
                return False

        try:
            sound = self.sounds[file_path]

            # Set volume (0.0 to 1.0)
            volume = max(0.0, min(1.0, volume))
            sound.set_volume(volume)

            # Play sound
            sound.play()
            return True
        except Exception as e:
            print(f"Error playing sound '{file_path}': {e}")
            return False

    def stop_all(self):
        """Stop all playing sounds."""
        if self.initialized:
            pygame.mixer.stop()

    def unload_sound(self, file_path: str):
        """
        Unload a sound from memory.

        Args:
            file_path: Path to sound file
        """
        if file_path in self.sounds:
            del self.sounds[file_path]

    def clear_all(self):
        """Unload all sounds."""
        self.sounds.clear()

    def __repr__(self) -> str:
        """String representation for debugging."""
        return f"AudioManager(initialized={self.initialized}, loaded={len(self.sounds)})"
