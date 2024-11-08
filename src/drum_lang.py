from typing import List, Union
from dataclasses import dataclass
from typing import Dict

from drum_kit import DrumSound, note_lengths, drum_sounds, DrumKit
from notes import NoteLength
from drum_synth import DrumHit, DrumSynth


def parse_drum_sequence(sequence: str) -> List[Union[DrumHit, List[DrumHit]]]:
    """
    Parses a drum sequence string, returning a list of either:
    - Single drum hits (DrumHit)
    - Groups of simultaneous drum hits as lists of DrumHit

    Args:
        sequence: A string representing the drum sequence (e.g., "KSH5C2")

    Returns:
        List of DrumHit objects or lists of simultaneous DrumHit objects

    Raises:
        ValueError: If the sequence is empty or contains invalid codes
    """
    if not sequence or not sequence.strip():
        return []

    sequence = sequence.strip().replace(" ", "")
    parsed_sequence = []
    i = 0

    while i < len(sequence):
        simultaneous_hits = []

        # Look for drum sounds based on their codes
        while i < len(sequence) and DrumKit.DRUM_LANG_SOUND_MAP.get(sequence[i]):
            drum_sound = DrumKit.DRUM_LANG_SOUND_MAP.get(sequence[i])
            simultaneous_hits.append(drum_sound)
            i += 1

        # Check for note length
        if i < len(sequence) and DrumKit.DRUM_LANG_NOTE_LENGTHS.get(sequence[i]):
            note_length = DrumKit.get_drum_lang_note_length(sequence[i])
            i += 1
        else:
            note_length = note_lengths["quarter"]

        if not simultaneous_hits:
            continue

        # Create DrumHit objects
        if len(simultaneous_hits) > 1:
            # Multiple simultaneous hits as a list
            parsed_sequence.append(
                [
                    DrumHit(
                        midi_value=drum.midi_value,
                        note_length=note_length,
                        velocity=127,
                    )
                    for drum in simultaneous_hits
                ]
            )
        else:
            parsed_sequence.append(
                [
                    DrumHit(
                        midi_value=simultaneous_hits[0].midi_value,
                        note_length=note_length,
                        velocity=127,
                    )
                ]
            )

    return parsed_sequence


if __name__ == "__main__":
    sequence = "SH5C2"
    parsed_sequence = parse_drum_sequence(sequence)
    print(parsed_sequence)
    synth = DrumSynth()
    synth.play_track(parsed_sequence)
