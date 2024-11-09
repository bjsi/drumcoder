import unittest
from drum_lang import parse_primitives_from_drum_lang, parse_track_from_drum_lang
from primitives import (
    DOTTED_HALF,
    DOTTED_SIXTEENTH,
    QUARTER,
    NoteLength,
    Occlusion,
    PlayableTrack,
    DrumSound,
)


class TestDrumLang(unittest.TestCase):
    def test_empty_sequence(self):
        """Test that empty sequences return empty track"""
        empty_track = parse_track_from_drum_lang("")
        self.assertIsInstance(empty_track, PlayableTrack)
        self.assertEqual(empty_track.beats, [])

        whitespace_track = parse_track_from_drum_lang("   ")
        self.assertEqual(whitespace_track.beats, [])

    def test_single_hit(self):
        """Test parsing a single drum hit"""
        track = parse_track_from_drum_lang("S5")
        self.assertIsInstance(track, PlayableTrack)
        self.assertEqual(len(track.beats), 1)
        self.assertIsInstance(track.beats[0].hits[0], DrumSound)
        self.assertEqual(track.beats[0].hits[0].midi_value, 38)  # Snare drum MIDI value
        self.assertEqual(track.beats[0].length, QUARTER)

    def test_multiple_hits(self):
        """Test parsing simultaneous hits"""
        track = parse_track_from_drum_lang("SH2")  # Snare, Hi-hat
        self.assertEqual(len(track.beats), 1)
        self.assertIsInstance(track.beats[0].hits[0], DrumSound)
        self.assertIsInstance(track.beats[0].hits[1], DrumSound)

    def test_note_lengths(self):
        """Test parsing different note lengths"""
        track = parse_track_from_drum_lang("S8H2")  # Different note lengths
        self.assertEqual(len(track.beats), 2)
        self.assertEqual(track.beats[0].length, DOTTED_HALF)
        self.assertEqual(track.beats[1].length, DOTTED_SIXTEENTH)

    def test_whitespace(self):
        """Test that whitespace is handled correctly"""
        result1 = parse_track_from_drum_lang(" S 2 H2 ")
        result2 = parse_track_from_drum_lang("S2H2")
        print(result1)
        print(result2)
        # self.assertEqual(result1, result2)

    def test_roundtrip(self):
        """Test that invalid drum codes raise ValueError"""
        track = parse_track_from_drum_lang("S2H2")
        self.assertEqual(track.to_drum_lang_sequence(), "S2H2")

    def test_occlusion(self):
        """Test that occlusion is parsed correctly"""
        primitives = parse_primitives_from_drum_lang("S2?2")
        self.assertEqual(primitives[0], DrumSound.from_drum_lang_code("S"))
        self.assertEqual(primitives[1], NoteLength.from_drum_lang_code("2"))
        self.assertEqual(primitives[2], Occlusion())
        self.assertEqual(primitives[3], NoteLength.from_drum_lang_code("2"))

        primitives = parse_primitives_from_drum_lang("S2?2S2?2")
        self.assertEqual(primitives[0], DrumSound.from_drum_lang_code("S"))
        self.assertEqual(primitives[1], NoteLength.from_drum_lang_code("2"))
        self.assertEqual(primitives[2], Occlusion())
        self.assertEqual(primitives[3], NoteLength.from_drum_lang_code("2"))
        self.assertEqual(primitives[4], DrumSound.from_drum_lang_code("S"))
        self.assertEqual(primitives[5], NoteLength.from_drum_lang_code("2"))


if __name__ == "__main__":
    unittest.main()
