"""Generate addon/sounds/bonus.wav, the variable ratio reward sound.

The sound is synthesized from scratch using only the standard library, so it has
no third-party license: a quick rising bell arpeggio that lands on a ringing major
chord, with high sparkles in the tail.

Run from the repository root:

    python tools/generate_bonus_sound.py
"""

import math
import random
import struct
import wave
from pathlib import Path
from typing import List, Tuple

SAMPLE_RATE = 44100
DURATION = 1.7  # seconds
PEAK = 0.6  # a few dB louder than the regular good/easy sounds
OUTPUT = Path(__file__).resolve().parent.parent / "addon" / "sounds" / "bonus.wav"

# (relative frequency, relative amplitude) of each partial of a bell tone
PARTIALS = ((1.0, 1.0), (2.0, 0.45), (3.0, 0.22), (4.2, 0.1))

# (start time, MIDI note, gain, decay rate)
Note = Tuple[float, int, float, float]


def midi_to_freq(midi: int) -> float:
    return 440.0 * 2 ** ((midi - 69) / 12)


def notes() -> List[Note]:
    result: List[Note] = []

    # Rising arpeggio: G5 C6 E6 G6 C7
    for i, midi in enumerate((79, 84, 88, 91, 96)):
        result.append((i * 0.055, midi, 0.42, 7.0))

    # Landing chord: C5 C6 E6 G6 C7, ringing out
    chord_start = 5 * 0.055
    for midi, gain in ((72, 0.32), (84, 0.3), (88, 0.26), (91, 0.24), (96, 0.22)):
        result.append((chord_start, midi, gain, 2.0))

    # Sparkles: short, high, pentatonic pings scattered over the tail
    rng = random.Random(7)
    for _ in range(16):
        start = rng.uniform(chord_start + 0.05, DURATION - 0.35)
        midi = rng.choice((96, 98, 100, 103, 105, 108))
        result.append((start, midi, rng.uniform(0.06, 0.12), 22.0))

    return result


def render() -> List[float]:
    samples = [0.0] * int(SAMPLE_RATE * DURATION)
    for start, midi, gain, decay in notes():
        freq = midi_to_freq(midi)
        first = int(start * SAMPLE_RATE)
        # Stop once the fundamental has decayed below -80 dB
        length = min(len(samples) - first, int(9.2 / decay * SAMPLE_RATE))
        for n in range(length):
            t = n / SAMPLE_RATE
            attack = min(1.0, t / 0.003)
            value = 0.0
            for ratio, amp in PARTIALS:
                # Higher partials fade faster, like a struck bell
                envelope = math.exp(-t * decay * (1 + ratio) / 2)
                # Two slightly detuned voices for a shimmering chorus
                phase = 2 * math.pi * freq * ratio * t
                value += amp * envelope * (math.sin(phase) + math.sin(phase * 1.003))
            samples[first + n] += gain * attack * value / 2

    # Fade out the very end so it never clicks
    fade = int(0.08 * SAMPLE_RATE)
    for i in range(fade):
        samples[-1 - i] *= i / fade

    scale = PEAK / max(abs(s) for s in samples)
    return [s * scale for s in samples]


def main() -> None:
    samples = render()
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    with wave.open(str(OUTPUT), "wb") as file:
        file.setnchannels(1)
        file.setsampwidth(2)
        file.setframerate(SAMPLE_RATE)
        file.writeframes(b"".join(struct.pack("<h", round(s * 32767)) for s in samples))
    print(f"Wrote {OUTPUT}")


if __name__ == "__main__":
    main()
