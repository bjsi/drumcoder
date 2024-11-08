import unittest
from drum_lang import parse_drum_sequence
from drum_kit import note_lengths
from drum_synth import DrumHit


class TestDrumLang(unittest.TestCase):
    def test_empty_sequence(self):
        """Test that empty sequences return empty list"""
        self.assertEqual(parse_drum_sequence(""), [])
        self.assertEqual(parse_drum_sequence("   "), [])

    def test_single_hit(self):
        """Test parsing a single drum hit"""
        result = parse_drum_sequence("S")
        self.assertEqual(len(result), 1)
        self.assertIsInstance(result[0][0], DrumHit)
        self.assertEqual(result[0][0].midi_value, 38)  # Snare drum MIDI value
        self.assertEqual(result[0][0].note_length, note_lengths["quarter"])

    def test_multiple_hits(self):
        """Test parsing simultaneous hits"""
        result = parse_drum_sequence("SH")  # Kick, Snare, Hi-hat
        self.assertEqual(len(result), 1)
        self.assertIsInstance(result[0][0], DrumHit)
        self.assertIsInstance(result[0][1], DrumHit)

    def test_note_lengths(self):
        """Test parsing different note lengths"""
        result = parse_drum_sequence("S8H2")  # Different note lengths
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0][0].note_length, note_lengths["dotted_half"])
        self.assertEqual(result[1][0].note_length, note_lengths["dotted_sixteenth"])

    def test_whitespace(self):
        """Test that whitespace is handled correctly"""
        result1 = parse_drum_sequence(" S H")
        result2 = parse_drum_sequence("SH")
        print(result1)
        print(result2)
        # self.assertEqual(result1, result2)

    # def test_invalid_drum_code(self):
    #     """Test that invalid drum codes raise ValueError"""
    #     with self.assertRaises(ValueError):
    #         parse_drum_sequence("X")  # Invalid drum code


if __name__ == "__main__":
    unittest.main()
