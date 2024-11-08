from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Optional
from notes import NoteLength, note_lengths

SAMPLES_DIR = Path("./data/samples")


@dataclass
class DrumSound:
    midi_value: int
    name: str
    sample_path: Path
    drum_lang_code: str


drum_sounds = {
    "bass_drum_2": DrumSound(
        35, "Bass Drum 2", SAMPLES_DIR / "kick/kick_02_t1.wav", "b"
    ),
    "bass_drum_1": DrumSound(
        36, "Bass Drum 1", SAMPLES_DIR / "kick/kick_01_t1.wav", "B"
    ),
    "side_stick": DrumSound(37, "Side Stick", SAMPLES_DIR / "rim/rim_01_t1.wav", "s"),
    "snare": DrumSound(38, "Snare", SAMPLES_DIR / "snare/snare_01_t1.wav", "S"),
    "hand_clap": DrumSound(39, "Hand Clap", SAMPLES_DIR / "clap/clap_tape.wav", "C"),
    "snare_alt": DrumSound(
        40, "Snare (Alt)", SAMPLES_DIR / "snare/snare_02_t1.wav", "z"
    ),
    "low_tom": DrumSound(41, "Low Tom", SAMPLES_DIR / "tom/tom_01_t1.wav", "l"),
    "hi_hat_closed": DrumSound(
        42, "Hi-Hat Closed", SAMPLES_DIR / "hihat_closed/closedhat_01_t1.wav", "h"
    ),
    "high_floor_tom": DrumSound(
        43, "High Floor Tom", SAMPLES_DIR / "tom/tom_02_t1.wav", "H"
    ),
    "hi_hat_pedal": DrumSound(
        44, "Hi-Hat Pedal", SAMPLES_DIR / "hihat_closed/closedhat_02_t1.wav", "p"
    ),
    "low_tom_2": DrumSound(45, "Low Tom", SAMPLES_DIR / "tom/tom_03_t1.wav", "m"),
    "hi_hat_open": DrumSound(
        46, "Hi-Hat Open", SAMPLES_DIR / "hihat_open/openhat_01_t1.wav", "o"
    ),
    "low_mid_tom": DrumSound(47, "Low-Mid Tom", SAMPLES_DIR / "tom/tom_04_t1.wav", "M"),
    "crash_1": DrumSound(49, "Crash 1", SAMPLES_DIR / "crash/crash_01_t1.wav", "c"),
    "high_tom": DrumSound(50, "High Tom", SAMPLES_DIR / "tom/tom_06_t1.wav", "O"),
    "ride_1": DrumSound(51, "Ride 1", SAMPLES_DIR / "ride/ride_01_t1.wav", "R"),
    "chinese_cymbal": DrumSound(
        52, "Chinese Cymbal", SAMPLES_DIR / "ride/ride_02_t2.wav", "I"
    ),
    "tambourine": DrumSound(54, "Tambourine", SAMPLES_DIR / "perc/perc_tambo.wav", "T"),
    "splash": DrumSound(55, "Splash", SAMPLES_DIR / "ride/ride_02_t2.wav", "L"),
    "cowbell": DrumSound(56, "Cowbell", SAMPLES_DIR / "cowbell/cowbell_01_t1.wav", "w"),
    "crash_2": DrumSound(57, "Crash 2", SAMPLES_DIR / "crash/crash_acoustic.wav", "r"),
    "ride_2": DrumSound(59, "Ride 2", SAMPLES_DIR / "ride/ride_02_t1.wav", "a"),
    "cabasa": DrumSound(69, "Cabasa", SAMPLES_DIR / "cabasa/cabasa_01_t1.wav", "A"),
}

# Verify drum lang codes are unique
drum_lang_codes = [sound.drum_lang_code for sound in drum_sounds.values()]
if len(drum_lang_codes) != len(set(drum_lang_codes)):
    duplicate_codes = [
        code for code in drum_lang_codes if drum_lang_codes.count(code) > 1
    ]
    raise ValueError(f"Duplicate drum language codes found: {duplicate_codes}")


class DrumKit:

    DRUM_LANG_SOUND_MAP: Dict[str, DrumSound] = {
        sound.drum_lang_code: sound for sound in drum_sounds.values()
    }
    MIDI_DRUM_MAP: Dict[int, DrumSound] = {
        sound.midi_value: sound for sound in drum_sounds.values()
    }
    DRUM_LANG_NOTE_LENGTHS: Dict[str, NoteLength] = {
        length.drum_lang_code: length for length in note_lengths.values()
    }
    GP_NOTE_LENGTHS: Dict[str, NoteLength] = {
        str(length.value) + str(length.is_dotted): length
        for length in note_lengths.values()
    }

    @classmethod
    def get_gp_note_length(cls, gp_value: int, is_dotted: bool = False) -> NoteLength:
        """Get note length object by Guitar Pro value"""
        note_length = cls.GP_NOTE_LENGTHS.get(str(gp_value) + str(is_dotted))
        return note_length

    @classmethod
    def get_drum_lang_note_length(cls, value: int) -> NoteLength:
        """Get note length object by Drum Lang value"""
        return cls.DRUM_LANG_NOTE_LENGTHS.get(value)

    @classmethod
    def get_drum_sound_by_midi(cls, midi_value: int) -> Optional[DrumSound]:
        """Get drum sound object by MIDI value"""
        return cls.MIDI_DRUM_MAP.get(midi_value)

    @classmethod
    def get_sample_path(cls, midi_value: int) -> Optional[Path]:
        """Get sample file path for a given MIDI value"""
        drum_sound = cls.get_drum_sound_by_midi(midi_value)
        return drum_sound.sample_path if drum_sound else None

    @classmethod
    def get_name(cls, midi_value: int) -> str:
        """Get drum name for a given MIDI value"""
        drum_sound = cls.get_drum_sound_by_midi(midi_value)
        return drum_sound.name if drum_sound else f"Unknown ({midi_value})"

    @classmethod
    def get_short_name(cls, midi_value: int) -> str:
        """Get short drum name for a given MIDI value"""
        drum_sound = cls.get_drum_sound_by_midi(midi_value)
        return drum_sound.drum_lang_code if drum_sound else f"U{midi_value}"
