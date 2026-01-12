"""Generate default alert sound for mmMCounter."""

import wave
import struct
import math


def generate_beep(frequency=800, duration_ms=200, sample_rate=44100):
    """
    Generate a simple beep tone as WAV file.

    Args:
        frequency: Frequency in Hz
        duration_ms: Duration in milliseconds
        sample_rate: Sample rate in Hz
    """
    num_samples = int(sample_rate * duration_ms / 1000)

    # Generate samples for a sine wave
    samples = []
    for i in range(num_samples):
        # Sine wave with envelope (fade in/out to avoid clicks)
        t = i / sample_rate
        envelope = 1.0

        # Fade in first 10ms
        fade_in_samples = int(sample_rate * 0.01)
        if i < fade_in_samples:
            envelope = i / fade_in_samples

        # Fade out last 10ms
        fade_out_samples = int(sample_rate * 0.01)
        if i > num_samples - fade_out_samples:
            envelope = (num_samples - i) / fade_out_samples

        # Generate sine wave
        value = envelope * math.sin(2 * math.pi * frequency * t)

        # Convert to 16-bit integer (-32768 to 32767)
        samples.append(int(value * 32767 * 0.3))  # 30% volume

    return samples


def save_wav(filename, samples, sample_rate=44100):
    """
    Save samples to WAV file.

    Args:
        filename: Output filename
        samples: List of sample values
        sample_rate: Sample rate in Hz
    """
    with wave.open(filename, 'w') as wav_file:
        # Set WAV file parameters
        # nchannels, sampwidth, framerate, nframes, comptype, compname
        wav_file.setparams((1, 2, sample_rate, len(samples), 'NONE', 'not compressed'))

        # Write samples
        for sample in samples:
            wav_file.writeframes(struct.pack('<h', sample))


if __name__ == "__main__":
    print("Generating default alert sound...")

    # Generate a pleasant two-tone beep
    beep1 = generate_beep(frequency=800, duration_ms=150)
    silence = [0] * int(44100 * 0.05)  # 50ms silence
    beep2 = generate_beep(frequency=1000, duration_ms=150)

    # Combine
    samples = beep1 + silence + beep2

    # Save
    output_path = "assets/sounds/default_alert.wav"
    save_wav(output_path, samples)

    print(f"Generated {output_path}")
    print(f"Duration: ~350ms, Two-tone beep (800Hz + 1000Hz)")
