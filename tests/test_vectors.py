"""Tests for the final vector processing task."""

import unittest

from src.assembler import load_program, translate
from src.machine_code import encode_program
from src.virtual_machine import VirtualMachine


VECTOR_LENGTH = 9
COMMANDS_PER_ELEMENT = 8

SAMPLES = {
    1: (
        [12, 15, 7, 0, 255, 170, 85, 128, 31],
        [10, 3, 14, 99, 15, 204, 240, 127, 16],
    ),
    2: (
        [0, 255, 1, 2, 4, 8, 16, 32, 64],
        [255, 0, 255, 255, 255, 255, 255, 255, 255],
    ),
    3: (
        [9, 18, 36, 72, 144, 7, 28, 63, 200],
        [5, 27, 60, 12, 240, 11, 21, 42, 100],
    ),
}


class TestVectors(unittest.TestCase):
    """Verify the three vector processing programs."""

    def check_vector(self, number):
        """Check the source and resulting memory vectors."""
        first, second = SAMPLES[number]
        source = load_program(f"examples/vector_{number}.yaml")
        program = translate(source)

        self.assertEqual(
            len(program), VECTOR_LENGTH * COMMANDS_PER_ELEMENT
        )

        machine = VirtualMachine(encode_program(program))
        machine.run()

        expected = [a & b for a, b in zip(first, second)]

        self.assertEqual(machine.memory[100:109], first)
        self.assertEqual(machine.memory[200:209], expected)

    def test_first_vector(self):
        """Verify the first input data set."""
        self.check_vector(1)

    def test_second_vector(self):
        """Verify the second input data set."""
        self.check_vector(2)

    def test_third_vector(self):
        """Verify the third input data set."""
        self.check_vector(3)


if __name__ == "__main__":
    unittest.main()
