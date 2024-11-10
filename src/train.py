from typing import List
from grammar import Grammar
from primitives import drum_lang_primitives
from generator import generate_tracks
from dataset import generate_tasks, init_drum_dataset
from dataset import InfillTask

# TODO: shared grammar vs task-specific grammars?
# TODO: run programs over all tasks or per task?
# TODO: support larger holes for infilling


def train(tasks: List[InfillTask], num_sleep_wake_cycles: int = 1):
    # instantiate a grammar with uniform probabilities across all primitives
    grammar = Grammar.uniform(drum_lang_primitives)
    for _ in range(num_sleep_wake_cycles):

        # generate programs with no neural guidance
        tracks = wake(grammar, tasks)
        print(f"Generated {len(tracks)} tracks")


def wake(grammar: Grammar, tasks: List[InfillTask]):
    # Bin the tasks by request type and grammar
    # If these are the same then we can generate tracks for multiple tasks simultaneously
    grouped_tasks = {}
    for task in tasks:
        key = (task.hole_type, grammar)
        if key not in grouped_tasks:
            grouped_tasks[key] = []
        grouped_tasks[key].append(task)

    # Generate tracks for each group of tasks separately
    all_tracks = {}
    for tasks in grouped_tasks.values():
        tracks = generate_tracks(grammar, tasks)
        all_tracks.extend(tracks)
    return all_tracks


def sleep(grammar):
    pass


def consolidate():
    pass


if __name__ == "__main__":
    tab_files = init_drum_dataset()
    tasks = generate_tasks(tab_files, 50)
    train(tasks)
