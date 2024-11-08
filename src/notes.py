from dataclasses import dataclass


@dataclass
class NoteLength:
    value: int
    is_dotted: bool = False
    drum_lang_code: str = ""

    @property
    def name(self) -> str:
        val = str(self.value) if self.value == 1 else f"1/{self.value}"
        if self.is_dotted:
            val += " dotted"
        return val


note_lengths = {
    "sixty_fourth": NoteLength(64, False, "+"),
    "thirty_second": NoteLength(32, False, "0"),
    "sixteenth": NoteLength(16, False, "1"),
    "dotted_sixteenth": NoteLength(16, True, "2"),
    "eighth": NoteLength(8, False, "3"),
    "dotted_eighth": NoteLength(8, True, "4"),
    "quarter": NoteLength(4, False, "5"),
    "dotted_quarter": NoteLength(4, True, "6"),
    "half": NoteLength(2, False, "7"),
    "dotted_half": NoteLength(2, True, "8"),
    "whole": NoteLength(1, False, "9"),
}

# Verify note length names are unique
note_length_names = [length.name for length in note_lengths.values()]
if len(note_length_names) != len(set(note_length_names)):
    duplicate_names = [
        name for name in note_length_names if note_length_names.count(name) > 1
    ]
    raise ValueError(f"Duplicate note length names found: {duplicate_names}")
