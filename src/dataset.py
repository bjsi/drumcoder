from pathlib import Path
import random
from typing import List, Optional
from drum_lang import parse_primitives_from_drum_lang, parse_track_from_drum_lang
from drum_synth import DrumSynth
from tab_parser import parse_flat_track_from_tab, parse_playable_track_from_tab
from dataclasses import dataclass
from primitives import (
    FlatTrack,
    NoteLength,
    OccludedTrack,
    Occlusion,
    PlayableTrack,
    Rest,
)


@dataclass
class OccludedTask:
    """Represents a drum track with some sounds or note lengths occluded"""

    original_track: OccludedTrack
    occluded_idxs: List[int]

    @property
    def occluded_track(self) -> FlatTrack:
        """Get the track with the occluded beats"""
        track = self.original_track.copy()
        for idx in self.occluded_idxs:
            track[idx] = Occlusion()
        return track

    def __len__(self) -> int:
        return len(self.original_track)

    def to_drum_lang(self, occluded: bool = False) -> str:
        return "".join(
            [primitive.drum_lang_code for primitive in self.occluded_track]
            if occluded
            else [primitive.drum_lang_code for primitive in self.original_track]
        )

    def to_playable_track(self, occluded: bool = False) -> PlayableTrack:
        return parse_track_from_drum_lang(self.to_drum_lang(occluded))

    def play(self, occluded: bool = False):
        track = self.to_playable_track(occluded)
        track.bpm = 120
        synth = DrumSynth()
        synth.play_track(track)


def init_drum_dataset(gp_dir: str = "./data/gp"):
    gp_dir = Path(gp_dir)
    return list(gp_dir.glob("*.gp*"))


def load_tracks(tab_files: List[Path]) -> List[PlayableTrack]:
    """Load all drum tracks from Guitar Pro files in directory"""
    tracks: List[PlayableTrack] = []
    for tab_file in tab_files:
        try:
            track = parse_playable_track_from_tab(tab_file)
            if track:  # Only add non-empty tracks
                tracks.append(track)
        except Exception as e:
            print(f"Error loading {tab_file}: {e}")
    return tracks


def create_occlusion_task(
    track: FlatTrack,
    num_occluded: Optional[int] = None,
    occlusion_probability: float = 0.2,
) -> OccludedTask:
    """Create an occlusion task from a track by hiding some beats"""
    if not track:
        raise ValueError("Cannot create occlusion task from empty track")

    # Determine number of beats to occlude
    if num_occluded is None:
        num_occluded = max(1, int(len(track) * occlusion_probability))

    # Randomly select beats to occlude
    occluded_indices = random.sample(range(len(track)), num_occluded)
    occluded_indices.sort()

    return OccludedTask(
        original_track=track,
        occluded_idxs=occluded_indices,
    )


def generate_tasks(
    tab_files: List[Path],
    max_tasks: int,
    min_beats: int = 18,
    max_beats: int = 48,
    occlusion_probability: float = 0.2,
) -> List[OccludedTask]:
    """Generate a dataset of occlusion tasks"""
    all_tracks = load_tracks(tab_files)
    print(f"all_tracks: {len(all_tracks)}")
    tasks = []
    for track in all_tracks:
        i = 0
        while i < len(track):
            # Find end of segment
            random_len = random.randint(min_beats, max_beats)
            end = min(i + random_len, len(track))
            segment = track.from_slice(i, end)
            print(f"segment: {segment.to_drum_lang_sequence()}")
            segment = parse_primitives_from_drum_lang(segment.to_drum_lang_sequence())
            if is_valid_segment(segment, min_beats=random_len):
                task = create_occlusion_task(
                    segment, occlusion_probability=occlusion_probability
                )
                tasks.append(task)

                if len(tasks) >= max_tasks:
                    break

            i = end

        if len(tasks) >= max_tasks:
            break

    print("-" * 25)
    print(f"Dataset statistics:")
    print(f"Total tracks processed: {len(all_tracks)}")
    print(f"Tasks generated: {len(tasks)}")
    print("-" * 25)

    return tasks


def is_valid_segment(segment: FlatTrack, min_beats: int = 4) -> bool:
    """Check if a segment is valid for task generation

    Args:
        segment: Track segment to validate
        min_beats: Minimum number of beats required

    Returns:
        bool: True if segment is valid
    """
    try:
        # Must end with note length
        if not isinstance(segment[-1], NoteLength):
            return False

        # Convert to drum lang and check number of beats
        drum_lang = "".join(primitive.drum_lang_code for primitive in segment)
        print(f"drum_lang: {drum_lang}")
        playable_track = parse_track_from_drum_lang(drum_lang)

        # Count total hits and rests
        total_hits = sum(len(beat.hits) for beat in playable_track.beats)
        rest_count = sum(
            sum(1 for hit in beat.hits if isinstance(hit, Rest))
            for beat in playable_track.beats
        )

        # Return False if more than 50% are rests
        if rest_count / total_hits > 0.5:
            return False

        return len(playable_track.beats) >= min_beats

    except (ValueError, IndexError):
        return False


if __name__ == "__main__":
    tab_files = init_drum_dataset()
    tasks = generate_tasks(tab_files, 50)
    random.shuffle(tasks)
    t = tasks[0]
    print(t.to_drum_lang(occluded=True))
    t.play()
