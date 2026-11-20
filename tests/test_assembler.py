"""Tests for the YAML assembler."""

import unittest

from src.assembler import (
    load_program,
    parse_instruction,
    translate,
)


class TestAssembler(unittest.TestCase):
    """Check instruction parsing and validation."""

    def test_load_program(self):
        """Read the example YAML program."""
        program = load_program("examples/spec_tests.yaml")
        self.assertEqual(len(program), 4)

    def test_specification(self):
        """Match all instruction fields from the specification."""
        program = translate(load_program("examples/spec_tests.yaml"))

        expected = [
            {"A": 4, "B": 26, "C": 16},
            {"A": 6, "B": 20, "C": 24, "D": 46},
            {"A": 3, "B": 21, "C": 29},
            {"A": 1, "B": 14, "C": 100, "D": 12},
        ]
        self.assertEqual(program, expected)

    def test_unknown_command(self):
        """Reject unknown instruction names."""
        with self.assertRaises(ValueError):
            parse_instruction({"command": "UNKNOWN"})

    def test_missing_field(self):
        """Reject missing instruction fields."""
        with self.assertRaises(ValueError):
            parse_instruction({"command": "LOAD", "B": 26})

    def test_extra_field(self):
        """Reject unexpected instruction fields."""
        with self.assertRaises(ValueError):
            parse_instruction({
                "command": "STORE", "B": 21,
                "C": 29, "D": 10,
            })

    def test_negative_value(self):
        """Reject negative field values."""
        with self.assertRaises(ValueError):
            parse_instruction({
                "command": "LOAD", "B": -1, "C": 16,
            })

    def test_out_of_range(self):
        """Reject values exceeding their bit widths."""
        with self.assertRaises(ValueError):
            parse_instruction({
                "command": "LOAD", "B": 8192, "C": 16,
            })

    def test_boolean_value(self):
        """Reject Boolean values instead of integers."""
        with self.assertRaises(ValueError):
            parse_instruction({
                "command": "LOAD", "B": True, "C": 16,
            })

    def test_wrong_value_type(self):
        """Reject string values instead of integers."""
        with self.assertRaises(ValueError):
            parse_instruction({
                "command": "LOAD", "B": "26", "C": 16,
            })

    def test_empty_program(self):
        """Reject an empty assembly program."""
        with self.assertRaises(ValueError):
            translate([])

    def test_invalid_program_type(self):
        """Reject a program that is not a list."""
        with self.assertRaises(ValueError):
            translate({"command": "LOAD"})

    def test_invalid_instruction_type(self):
        """Reject instructions that are not dictionaries."""
        with self.assertRaises(ValueError):
            parse_instruction("LOAD 26 16")


if __name__ == "__main__":
    unittest.main()
