from typing import List, Union
from drum_synth import DrumSynth
from primitives import (
    Beat,
    DrumSound,
    InfillTrack,
    NoteLength,
    Hole,
    PlayableTrack,
)


def parse_primitives_from_drum_lang(
    sequence: str,
) -> InfillTrack:
    """Different from parse_track_from_drum_lang in that it returns a list of primitives.
    This supports ? occlusions.
    """
    primitives: List[Union[DrumSound, NoteLength, Hole]] = []

    i = 0
    while i < len(sequence):
        if sequence[i] == "?":
            primitives.append(Hole())
        elif NoteLength.from_drum_lang_code(sequence[i]):
            primitives.append(NoteLength.from_drum_lang_code(sequence[i]))
        elif DrumSound.from_drum_lang_code(sequence[i]):
            primitives.append(DrumSound.from_drum_lang_code(sequence[i]))
        else:
            raise ValueError(f"Invalid drum lang code: {sequence[i]}")
        i += 1

    return primitives


def primitives_to_track(
    primitives: List[Union[DrumSound, NoteLength, Hole]],
    bpm: int = 120,
) -> PlayableTrack:
    # Check for occlusions
    if any(isinstance(p, Hole) for p in primitives):
        raise ValueError("Occlusions not supported in primitives_to_track")

    beats: List[Beat] = []
    hits: List[DrumSound] = []

    for primitive in primitives:
        if isinstance(primitive, DrumSound):
            hits.append(primitive)
        elif isinstance(primitive, NoteLength):
            if not hits:
                raise ValueError("No hits to create a beat")
            elif len(hits) > 4:
                raise ValueError("Too many hits to create a beat (max 4)")
            beats.append(Beat(hits=hits, length=primitive))
            hits = []

    return PlayableTrack(beats=beats, bpm=bpm)


def parse_track_from_drum_lang(sequence: str) -> PlayableTrack:
    """Parse a drum language sequence into a playable track."""
    if "?" in sequence:
        raise ValueError("Occlusions not supported in parse_track_from_drum_lang")

    if not sequence or not sequence.strip():
        return PlayableTrack(beats=[])

    sequence = sequence.strip().replace(" ", "")
    beats: List[Beat] = []
    i = 0

    while i < len(sequence):
        simultaneous_hits: List[DrumSound] = []

        while i < len(sequence):
            drum_sound = DrumSound.from_drum_lang_code(sequence[i])
            if not simultaneous_hits and drum_sound is None:
                raise ValueError(f"Invalid or missing drum sound")
            elif drum_sound is None:
                break
            else:
                simultaneous_hits.append(drum_sound)
                i += 1

        # Check for note length
        if i < len(sequence) and NoteLength.from_drum_lang_code(sequence[i]):
            note_length = NoteLength.from_drum_lang_code(sequence[i])
            i += 1
        elif isinstance(simultaneous_hits[-1], Hole):
            pass
        else:
            raise ValueError(f"Invalid or missing note length")

        beats.append(
            Beat(
                hits=simultaneous_hits,
                length=note_length,
            )
        )
    return PlayableTrack(beats=beats)


if __name__ == "__main__":
    sequence = "B2B2S2R2"  # Boom boom clap
    track = parse_track_from_drum_lang(sequence)
    track.bpm = 81
    print(track.beats[-1])
    synth = DrumSynth()
    synth.play_track(track)
