from pathlib import Path
import random
from typing import List
from drum_lang import parse_primitives_from_drum_lang, parse_track_from_drum_lang
from drum_synth import DrumSynth
from tab_parser import parse_playable_track_from_tab
from dataclasses import dataclass
from primitives import (
    DrumSound,
    FlatTrack,
    NoteLength,
    InfillTrack,
    Hole,
    PlayableTrack,
    PrimitiveType,
    Rest,
)


@dataclass(frozen=True)
class InfillTask:
    """Represents a drum track with a single hole"""

    original_track: InfillTrack
    hole_start: int  # Start index of hole
    hole_length: int  # Number of consecutive primitives to hole

    @property
    def hole_indices(self) -> List[int]:
        """Get the indices that are holes"""
        return list(
            range(
                self.hole_start,
                min(
                    self.hole_start + self.hole_length,
                    len(self.original_track),
                ),
            )
        )

    @property
    def track_with_hole(self) -> FlatTrack:
        """Get the track with the hole"""
        track = self.original_track.copy()
        for idx in self.hole_indices:
            track[idx] = Hole()
        return track

    def __len__(self) -> int:
        return len(self.original_track)

    def to_drum_lang_string(self, with_hole: bool = False) -> str:
        return "".join(
            [primitive.drum_lang_code for primitive in self.track_with_hole]
            if with_hole
            else [primitive.drum_lang_code for primitive in self.original_track]
        )

    def to_playable_track(self, with_hole: bool = False) -> PlayableTrack:
        return parse_track_from_drum_lang(self.to_drum_lang_string(with_hole))

    def play(self, with_hole: bool = False):
        track = self.to_playable_track(with_hole)
        track.bpm = 120
        synth = DrumSynth()
        synth.play_track(track)

    @property
    def task_signature(self) -> str:
        """Get a unique signature for this task based on its content and hole position"""
        return (
            f"{self.to_drum_lang_string(with_hole=False)}"
            f"_hole{self.hole_start}-{self.hole_start + self.hole_length}"
        )

    @property
    def hole_type(self) -> PrimitiveType:
        """Get the type of the infill primitive"""
        return self.original_track[self.hole_start].type


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


def create_infill_task(
    track: FlatTrack,
    hole_length: int,
) -> InfillTask:
    """Create an infill task from a track by hiding a sequence of primitives

    Args:
        track: The track to create a task from
        hole_length: Number of consecutive primitives to hole

    Returns:
        InfillTask with a single hole of specified length
    """
    if not track:
        raise ValueError("Cannot create infill task from empty track")

    if hole_length >= len(track):
        raise ValueError("Hole length cannot be longer than track")

    # Randomly select start position for hole
    # Ensure there's room for the full hole length
    max_start = len(track) - hole_length
    hole_start = random.randint(0, max_start)

    return InfillTask(
        original_track=track,
        hole_start=hole_start,
        hole_length=hole_length,
    )


def generate_tasks(
    tab_files: List[Path],
    max_tasks: int,
    min_beats: int = 12,
    max_beats: int = 24,
    hole_length: int = 1,
) -> List[InfillTask]:
    """Generate a dataset of infill tasks

    Args:
        tab_files: List of Guitar Pro files to process
        max_tasks: Maximum number of tasks to generate
        min_beats: Minimum number of beats in a segment
        max_beats: Maximum number of beats in a segment
        hole_length: Number of consecutive primitives to hole in each task
    """
    all_tracks = load_tracks(tab_files)
    print(f"all_tracks: {len(all_tracks)}")
    tasks = []
    seen_signatures = set()

    for track in all_tracks:
        i = 0
        while i < len(track):
            # Find end of segment
            random_len = random.randint(min_beats, max_beats)
            end = min(i + random_len, len(track))
            segment = track.from_slice(i, end)
            segment = parse_primitives_from_drum_lang(segment.to_drum_lang_sequence())

            if is_valid_segment(segment, min_beats=random_len):
                for _ in range(5):
                    task = create_infill_task(segment, hole_length=hole_length)
                    if task.task_signature not in seen_signatures:
                        seen_signatures.add(task.task_signature)
                        tasks.append(task)
                        if len(tasks) >= max_tasks:
                            break
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
    print(f"question: {t.to_drum_lang_string(with_hole=True)}")
    print(f"answer:   {t.to_drum_lang_string(with_hole=False)}")
    t.play()
