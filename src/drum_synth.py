import random
import time
import pygame
import pygame.midi
from primitives import DrumSound, PlayableTrack, drum_sounds


class DrumSynth:
    def __init__(self):
        # Initialize pygame mixer
        pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=512)

        # Initialize MIDI
        pygame.midi.init()

        # Load all drum sounds into memory
        self.sounds = {}
        for drum_sound in drum_sounds.values():
            if isinstance(drum_sound, DrumSound) and drum_sound.sample_path.exists():
                self.sounds[drum_sound.midi_value] = pygame.mixer.Sound(
                    str(drum_sound.sample_path)
                )

    def play_drum(self, midi_value: int, velocity: int = 127):
        """
        Play a drum sound for the given MIDI note
        velocity: 0-127 (will affect volume)
        """
        if midi_value in self.sounds:
            # Convert MIDI velocity (0-127) to pygame volume (0.0-1.0)
            # add small random variation to velocity
            volume = velocity / 127.0 + random.uniform(-0.05, 0.05)
            self.sounds[midi_value].set_volume(volume)
            self.sounds[midi_value].play()

    def play_track(self, track: PlayableTrack):
        for beat in track.beats:
            seconds_per_beat = (
                60.0 / track.bpm
            )  # one beat (quarter note) duration in seconds

            for hit in beat.hits:
                if isinstance(hit, DrumSound):
                    self.play_drum(hit.midi_value)

            duration = 1 / beat.length.value
            if beat.length.is_dotted:
                duration = duration + (duration / 2)

            # Convert duration to seconds based on BPM
            duration = (
                duration * 4 * seconds_per_beat
            )  # scale by 4 since duration is 1/note_value

            time.sleep(duration)

        self.cleanup()

    def cleanup(self):
        """Clean up resources"""
        time.sleep(1)
        pygame.midi.quit()
        pygame.mixer.quit()
