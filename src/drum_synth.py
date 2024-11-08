from dataclasses import dataclass
import time
from typing import List, Union
import pygame
import pygame.midi
from drum_kit import DrumKit, NoteLength


@dataclass
class DrumHit:
    def __init__(
        self,
        midi_value: int,
        note_length: NoteLength,
        velocity: int = 127,
    ):
        self.midi_value = midi_value
        self.note_length = note_length
        self.velocity = velocity

    def __repr__(self):
        return f"DrumHit(midi_value={DrumKit.get_name(self.midi_value)}, note_length={self.note_length.name}, velocity={self.velocity})"


@dataclass
class Rest:
    note_length: NoteLength


class DrumSynth:
    def __init__(self):
        # Initialize pygame mixer
        pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=512)

        # Initialize MIDI
        pygame.midi.init()

        # Load all drum sounds into memory
        self.sounds = {}
        for midi_value in DrumKit.MIDI_DRUM_MAP.keys():
            sample_path = DrumKit.get_sample_path(midi_value)
            if sample_path and sample_path.exists():
                self.sounds[midi_value] = pygame.mixer.Sound(str(sample_path))

    def play_drum(self, midi_value: int, velocity: int = 127):
        """
        Play a drum sound for the given MIDI note
        velocity: 0-127 (will affect volume)
        """
        if midi_value in self.sounds:
            # Convert MIDI velocity (0-127) to pygame volume (0.0-1.0)
            volume = velocity / 127.0
            self.sounds[midi_value].set_volume(volume)
            self.sounds[midi_value].play()

    def play_track(self, track: List[List[Union[DrumHit, Rest]]], bpm: int = 120):
        for measure in track:
            for hit in measure:
                seconds_per_beat = (
                    60.0 / bpm
                )  # one beat (quarter note) duration in seconds
                if isinstance(hit, DrumHit):
                    self.play_drum(hit.midi_value, hit.velocity)

            duration = (
                1 / measure[0].note_length.value
            )  # 1/4 = 0.25, 1/8 = 0.125, 1/16 = 0.0625

            # Handle dotted notes
            if hit.note_length.is_dotted:
                duration = duration + (duration / 2)

            # Convert duration to seconds based on BPM
            duration = (
                duration * 4 * seconds_per_beat
            )  # scale by 4 since duration is 1/note_value

            time.sleep(duration)

    def cleanup(self):
        """Clean up resources"""
        pygame.midi.quit()
        pygame.mixer.quit()
