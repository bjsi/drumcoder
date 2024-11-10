from typing import List, Tuple
from grammar import Grammar
from dataset import InfillTask
import time


# TODO: instead of pass/fail it could be a distance metric
def score_track(generated_track, task: InfillTask) -> Tuple[bool, float]:
    task_track = task.to_drum_lang_string(with_hole=False)
    if generated_track == task_track:
        return True, 0.0
    else:
        return False, float("-inf")


# Each track has a fixed MDL, so it can only appear in one slice. This ensures that
# a track is not generated multiple times.
# equivalent to @enumerateForTasks in DreamCoder
# All tasks must have the same hole type and should expect the same grammar
def generate_tracks(
    grammar: Grammar,
    tasks: List[InfillTask],
    lower_bound: float = 0,
    upper_bound: float = 100,
    budget_increment: float = 1.0,
    timeout_seconds: float = 2,
):

    request = tasks[0].hole_type
    assert all(
        t.hole_type == request for t in tasks
    ), "generate_tracks: Expected tasks to all have the same hole type"

    start_time = time.time()
    previous_budget = lower_bound
    budget = lower_bound + budget_increment
    generated_tracks_per_task = {t.task_signature: [] for t in tasks}
    total_programs = 0
    valid_programs = 0

    enumerations = grammar.fill_holes(request, debug=True)
    if len(enumerations) == 0:
        print("No valid tracks for any task")
        return generated_tracks_per_task

    for prior, production in enumerations:
        total_programs += 1

        if time.time() - start_time > timeout_seconds:
            print(f"Timeout reached. Stopping generation.")
            print(f"Total tracks generated: {total_programs}")
            print(f"Total valid tracks: {valid_programs}")
            return generated_tracks_per_task

        for i, task in enumerate(tasks):
            generated_track = task.to_drum_lang_string(with_hole=True).replace(
                "?", production.drum_lang_code
            )

            success, likelihood = score_track(generated_track, task)
            if not success:
                continue

            valid_programs += 1
            priority = -(likelihood + prior)
            generated_tracks_per_task[task.task_signature].append(
                (priority, generated_track)
            )

        previous_budget = budget
        budget += budget_increment

        if budget > upper_bound:
            break

    print(f"Generation completed. Total programs generated: {total_programs}")
    print(f"Total valid programs: {valid_programs}")
    return generated_tracks_per_task
