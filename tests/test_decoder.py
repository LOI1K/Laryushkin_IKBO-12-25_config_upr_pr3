"""Tests for binary instruction decoding."""

import unittest

from src.assembler import load_program, translate
from src.decoder import decode_instruction, decode_program
from src.machine_code import encode_program


class TestDecoder(unittest.TestCase):
    """Check decoding of machine instructions."""

    @classmethod
    def setUpClass(cls):
        """Prepare the reference machine program."""
        source = load_program("examples/spec_tests.yaml")
        cls.program = translate(source)
        cls.binary = encode_program(cls.program)

    def test_round_trip(self):
        """Restore the original instruction fields."""
        self.assertEqual(
            decode_program(self.binary), self.program
        )

    def test_instruction_sizes(self):
        """Check instruction sizes and offsets."""
        for offset, expected_size in (
            (0, 3), (3, 3), (6, 2), (8, 6)
        ):
            _, size = decode_instruction(self.binary, offset)
            self.assertEqual(size, expected_size)

    def test_incomplete_instruction(self):
        """Reject truncated binary instructions."""
        with self.assertRaises(ValueError):
            decode_instruction(b"\xD4\x00")

    def test_unknown_opcode(self):
        """Reject unsupported operation codes."""
        with self.assertRaises(ValueError):
            decode_instruction(b"\x07")

    def test_invalid_offset(self):
        """Reject invalid instruction offsets."""
        with self.assertRaises(ValueError):
            decode_instruction(self.binary, -1)


if __name__ == "__main__":
    unittest.main()
