import pprint
import guitarpro
from typing import List
from drum_synth import DrumHit, Rest
from drum_kit import DrumKit


def parse_guitar_pro(file_path) -> List[DrumHit]:
    song = guitarpro.parse(file_path)

    drums_tracks = [
        track
        for track in song.tracks
        if "Drum" in track.name
        or track.channel.instrument == 0  # Standard drum kit
        or track.channel.isPercussionChannel  # MIDI channel 9/10 is for drums
    ]

    drums = drums_tracks[0]

    if not drums:
        print("No drum track found!")
        return []

    drum_hits = []

    if not drums.measures:
        print("No measures found in drum track!")
        return []

    # Process all measures in the drum track
    for i, measure in enumerate(drums.measures):
        voice_one = measure.voices[0]
        # Only process first measure
        for beat in voice_one.beats:
            if beat.notes:
                hits = []
                print(
                    f"BEAT {beat.duration.value} {beat.duration.isDotted} {beat.duration.time}"
                )
                for note in beat.notes:
                    note_length = DrumKit.get_gp_note_length(
                        beat.duration.value, beat.duration.isDotted
                    )
                    hits.append(
                        DrumHit(
                            midi_value=note.value,
                            note_length=note_length,
                            velocity=note.velocity,
                        )
                    )
                drum_hits.append(hits)
            else:
                note_length = DrumKit.get_gp_note_length(
                    beat.duration.value, beat.duration.isDotted
                )
                rest = Rest(note_length)
                drum_hits.append([rest])

    print("---")
    pprint.pprint(drum_hits)
    print("---")
    return drum_hits
