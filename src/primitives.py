from dataclasses import dataclass
from enum import Enum, auto
from pathlib import Path
from typing import List, Union


class PrimitiveType(Enum):
    SOUND = auto()
    LENGTH = auto()


class Primitive:
    name: str
    cost: float
    type: PrimitiveType

    def __hash__(self) -> int:
        return hash(self.name)


@dataclass(frozen=True)
class Hole:

    name: str = "Hole"
    drum_lang_code: str = "?"


@dataclass(frozen=True)
class NoteLength(Primitive):

    value: int
    is_dotted: bool
    drum_lang_code: str
    type: PrimitiveType = PrimitiveType.LENGTH

    cost: float = 1.0

    @property
    def name(self) -> str:
        val = str(self.value) if self.value == 1 else f"1/{self.value}"
        if self.is_dotted:
            val += " dotted"
        return val

    @classmethod
    def from_drum_lang_code(cls, code: str) -> "NoteLength":
        return next(
            (
                length
                for length in note_lengths.values()
                if length.drum_lang_code == code
            ),
            None,
        )

    @classmethod
    def from_gp_value(cls, value: int, is_dotted: bool = False) -> "NoteLength":
        return next(
            (
                length
                for length in note_lengths.values()
                if length.value == value and length.is_dotted == is_dotted
            ),
            None,
        )

    def __repr__(self):
        return f"NoteLength({self.name}, {self.drum_lang_code})"


SIXTY_FOURTH = NoteLength(64, False, "+")
THIRTY_SECOND = NoteLength(32, False, "0")
SIXTEENTH = NoteLength(16, False, "1")
DOTTED_SIXTEENTH = NoteLength(16, True, "2")
EIGHTH = NoteLength(8, False, "3")
DOTTED_EIGHTH = NoteLength(8, True, "4")
QUARTER = NoteLength(4, False, "5")
DOTTED_QUARTER = NoteLength(4, True, "6")
HALF = NoteLength(2, False, "7")
DOTTED_HALF = NoteLength(2, True, "8")
WHOLE = NoteLength(1, False, "9")

note_lengths = {
    "sixty_fourth": SIXTY_FOURTH,
    "thirty_second": THIRTY_SECOND,
    "sixteenth": SIXTEENTH,
    "dotted_sixteenth": DOTTED_SIXTEENTH,
    "eighth": EIGHTH,
    "dotted_eighth": DOTTED_EIGHTH,
    "quarter": QUARTER,
    "dotted_quarter": DOTTED_QUARTER,
    "half": HALF,
    "dotted_half": DOTTED_HALF,
    "whole": WHOLE,
}


@dataclass(frozen=True)
class Rest(Primitive):
    midi_value: int = -1
    name: str = "Rest"
    drum_lang_code: str = "R"
    type: PrimitiveType = PrimitiveType.SOUND
    cost: float = 1.0

    def __repr__(self):
        return f"Rest({self.drum_lang_code})"


@dataclass(frozen=True)
class DrumSound(Primitive):
    midi_value: int
    name: str
    sample_path: Path
    drum_lang_code: str
    type: PrimitiveType = PrimitiveType.SOUND

    cost: float = 1.0

    @classmethod
    def from_drum_lang_code(cls, code: str) -> Union["DrumSound", Rest]:
        return next(
            (sound for sound in drum_sounds.values() if sound.drum_lang_code == code),
            None,
        )

    @classmethod
    def from_midi_value(cls, midi_value: int) -> Union["DrumSound", Rest]:
        sound = next(
            (sound for sound in drum_sounds.values() if sound.midi_value == midi_value),
            None,
        )
        if sound is None:
            print(f"No drum sound found for MIDI value: {midi_value}")
            return Rest()
        return sound

    def __repr__(self):
        return f"DrumSound({self.name}, {self.drum_lang_code})"


SAMPLES_DIR = Path("./data/samples")

# Define individual DrumSound instances as variables
STICK_CLICK = DrumSound(31, "Stick Click", SAMPLES_DIR / "rim/rim_02_t1.wav", "k")
BASS_DRUM_2 = DrumSound(35, "Bass Drum 2", SAMPLES_DIR / "kick/kick_02_t1.wav", "b")
BASS_DRUM_1 = DrumSound(36, "Bass Drum 1", SAMPLES_DIR / "kick/kick_01_t1.wav", "B")
SIDE_STICK = DrumSound(37, "Side Stick", SAMPLES_DIR / "rim/rim_01_t1.wav", "s")
SNARE = DrumSound(38, "Snare", SAMPLES_DIR / "snare/snare_01_t1.wav", "S")
HAND_CLAP = DrumSound(39, "Hand Clap", SAMPLES_DIR / "clap/clap_tape.wav", "C")
SNARE_ALT = DrumSound(40, "Snare (Alt)", SAMPLES_DIR / "snare/snare_02_t1.wav", "z")
LOW_TOM = DrumSound(41, "Low Tom", SAMPLES_DIR / "tom/tom_01_t1.wav", "l")
HI_HAT_CLOSED = DrumSound(
    42, "Hi-Hat Closed", SAMPLES_DIR / "hihat_closed/closedhat_01_t1.wav", "h"
)
HIGH_FLOOR_TOM = DrumSound(43, "High Floor Tom", SAMPLES_DIR / "tom/tom_02_t1.wav", "H")
HI_HAT_PEDAL = DrumSound(
    44, "Hi-Hat Pedal", SAMPLES_DIR / "hihat_closed/closedhat_02_t1.wav", "p"
)
LOW_TOM_2 = DrumSound(45, "Low Tom", SAMPLES_DIR / "tom/tom_03_t1.wav", "m")
HI_HAT_OPEN = DrumSound(
    46, "Hi-Hat Open", SAMPLES_DIR / "hihat_open/openhat_01_t1.wav", "o"
)
HIGH_MID_TOM = DrumSound(48, "High-Mid Tom", SAMPLES_DIR / "tom/tom_05_t1.wav", "t")
LOW_MID_TOM = DrumSound(47, "Low-Mid Tom", SAMPLES_DIR / "tom/tom_04_t1.wav", "M")
CRASH_1 = DrumSound(49, "Crash 1", SAMPLES_DIR / "crash/crash_01_t1.wav", "c")
HIGH_TOM = DrumSound(50, "High Tom", SAMPLES_DIR / "tom/tom_06_t1.wav", "O")
RIDE_1 = DrumSound(51, "Ride 1", SAMPLES_DIR / "ride/ride_01_t1.wav", "i")
CHINESE_CYMBAL = DrumSound(
    52, "Chinese Cymbal", SAMPLES_DIR / "ride/ride_01_t1.wav", "I"
)
RIDE_CYMBAL_1 = DrumSound(53, "Ride Cymbal 1", SAMPLES_DIR / "ride/ride_03_t1.wav", "D")
TAMBOURINE = DrumSound(54, "Tambourine", SAMPLES_DIR / "perc/perc_tambo.wav", "T")
SPLASH = DrumSound(55, "Splash", SAMPLES_DIR / "ride/ride_02_t2.wav", "L")
COWBELL = DrumSound(56, "Cowbell", SAMPLES_DIR / "cowbell/cowbell_01_t1.wav", "w")
CRASH_2 = DrumSound(57, "Crash 2", SAMPLES_DIR / "crash/crash_acoustic.wav", "r")
RIDE_2 = DrumSound(59, "Ride 2", SAMPLES_DIR / "ride/ride_02_t1.wav", "a")
CABASA = DrumSound(69, "Cabasa", SAMPLES_DIR / "cabasa/cabasa_01_t1.wav", "A")
SHAKER = DrumSound(92, "Shaker", SAMPLES_DIR / "shaker/shaker_analog.wav", "K")
RIDE_BELL = DrumSound(98, "Ride Bell", SAMPLES_DIR / "ride/ride_acoustic01.wav", "e")


# Use the variables in the drum_sounds dictionary
drum_sounds = {
    "stick_click": STICK_CLICK,
    "bass_drum_2": BASS_DRUM_2,
    "bass_drum_1": BASS_DRUM_1,
    "side_stick": SIDE_STICK,
    "snare": SNARE,
    "hand_clap": HAND_CLAP,
    "snare_alt": SNARE_ALT,
    "low_tom": LOW_TOM,
    "hi_hat_closed": HI_HAT_CLOSED,
    "high_floor_tom": HIGH_FLOOR_TOM,
    "hi_hat_pedal": HI_HAT_PEDAL,
    "low_tom_2": LOW_TOM_2,
    "hi_hat_open": HI_HAT_OPEN,
    "low_mid_tom": LOW_MID_TOM,
    "high_mid_tom": HIGH_MID_TOM,
    "crash_1": CRASH_1,
    "high_tom": HIGH_TOM,
    "ride_1": RIDE_1,
    "chinese_cymbal": CHINESE_CYMBAL,
    "tambourine": TAMBOURINE,
    "splash": SPLASH,
    "cowbell": COWBELL,
    "crash_2": CRASH_2,
    "ride_2": RIDE_2,
    "cabasa": CABASA,
    "shaker": SHAKER,
    "ride_bell": RIDE_BELL,
    "ride_cymbal_1": RIDE_CYMBAL_1,
    # special cases
    "rest": Rest(),
}

# Verify drum lang codes are unique across all primitives
drum_lang_codes = [sound.drum_lang_code for sound in drum_sounds.values()] + [
    length.drum_lang_code for length in note_lengths.values()
]
if len(drum_lang_codes) != len(set(drum_lang_codes)):
    duplicate_codes = [
        code for code in drum_lang_codes if drum_lang_codes.count(code) > 1
    ]
    raise ValueError(f"Duplicate drum language codes found: {duplicate_codes}")


Hits = List[Union[DrumSound, Rest]]


@dataclass
class Beat:
    """A single beat of a track.
    A beat is a collection of hits that occur simultaneously.
    """

    hits: Hits
    length: Union[NoteLength]

    @property
    def cost(self) -> float:
        return sum(hit.cost for hit in self.hits)

    @property
    def time(self) -> float:
        return self.length.time


FlatTrack = List[Union[DrumSound, NoteLength]]
InfillTrack = List[Union[DrumSound, NoteLength, Hole]]


@dataclass
class PlayableTrack:
    beats: List[Beat]
    bpm: int = 120

    def __len__(self) -> int:
        return len(self.beats)

    def to_drum_lang_sequence(self) -> str:
        # TODO: sort simultaneous hits
        return "".join(
            "".join(hit.drum_lang_code for hit in beat.hits)
            + beat.length.drum_lang_code
            for beat in self.beats
        )

    def from_slice(self, start: int, end: int) -> "PlayableTrack":
        return PlayableTrack(self.beats[start:end], self.bpm)


drum_lang_primitives = [
    *drum_sounds.values(),
    *note_lengths.values(),
]
