from pathlib import Path
import guitarpro
from typing import List, Tuple
from primitives import Beat, FlatTrack, Hits, NoteLength, Rest, PlayableTrack, DrumSound


def get_drums(file_path: Path) -> Tuple[List[guitarpro.Measure], int]:
    song = guitarpro.parse(file_path)
    bpm = song.tempo

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
        return [], bpm

    if not drums.measures:
        print("No measures found in drum track!")
        return [], bpm

    return drums.measures, bpm


def parse_flat_track_from_tab(file_path: Path) -> Tuple[FlatTrack, int]:
    measures, bpm = get_drums(file_path)
    track_flat: FlatTrack = []
    for measure in measures:
        voice_one = measure.voices[0]
        for beat in voice_one.beats:
            if beat.notes:
                for note in beat.notes:
                    track_flat.append(DrumSound.from_midi_value(note.value))
            else:
                track_flat.append(Rest())
            track_flat.append(NoteLength.from_gp_value(beat.duration.value))
    return track_flat, bpm


def parse_playable_track_from_tab(file_path: Path) -> PlayableTrack:
    measures, bpm = get_drums(file_path)
    beats: List[Beat] = []
    # Process all measures in the drum track
    for measure in measures:
        voice_one = measure.voices[0]
        for beat in voice_one.beats:
            length = NoteLength.from_gp_value(
                beat.duration.value, beat.duration.isDotted
            )
            hits: Hits = []
            if beat.notes:
                for note in beat.notes:
                    sound = DrumSound.from_midi_value(note.value)
                    hits.append(sound)
            else:
                hits.append(Rest())
            beats.append(Beat(hits=hits, length=length))
    track = PlayableTrack(beats=beats, bpm=bpm)
    return track
