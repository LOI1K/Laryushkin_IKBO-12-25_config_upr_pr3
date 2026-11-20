"""Tests for binary instruction encoding."""

import subprocess
import sys
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

from src.assembler import load_program, translate
from src.machine_code import encode_instruction, encode_program


class TestMachineCode(unittest.TestCase):
    """Check instruction bytes and binary file generation."""

    @classmethod
    def setUpClass(cls):
        """Load the specification example."""
        source = load_program("examples/spec_tests.yaml")
        cls.program = translate(source)

    def test_load(self):
        """Check the LOAD instruction bytes."""
        result = encode_instruction(self.program[0])
        self.assertEqual(result, bytes.fromhex("D4 00 10"))

    def test_read(self):
        """Check the READ instruction bytes."""
        result = encode_instruction(self.program[1])
        self.assertEqual(result, bytes.fromhex("A6 D8 05"))

    def test_store(self):
        """Check the STORE instruction bytes."""
        result = encode_instruction(self.program[2])
        self.assertEqual(result, bytes.fromhex("AB 1D"))

    def test_and(self):
        """Check the AND instruction bytes."""
        result = encode_instruction(self.program[3])
        expected = bytes.fromhex("71 64 00 00 00 0C")
        self.assertEqual(result, expected)

    def test_complete_program(self):
        """Check the complete assembled program."""
        result = encode_program(self.program)
        expected = bytes.fromhex(
            "D4 00 10 A6 D8 05 AB 1D 71 64 00 00 00 0C"
        )
        self.assertEqual(result, expected)
        self.assertEqual(len(result), 14)

    def test_unknown_opcode(self):
        """Reject an unsupported instruction code."""
        with self.assertRaises(ValueError):
            encode_instruction({"A": 7})

    def test_binary_output(self):
        """Check binary file creation through the CLI."""
        with TemporaryDirectory() as directory:
            output = Path(directory) / "program.bin"
            result = subprocess.run(
                [
                    sys.executable, "-m", "src.main",
                    "examples/spec_tests.yaml", str(output),
                    "--test",
                ],
                capture_output=True,
                text=True,
                check=False,
            )

            self.assertEqual(result.returncode, 0)
            self.assertEqual(output.read_bytes(),
                             encode_program(self.program))
            self.assertIn("Ассемблировано команд: 4", result.stdout)


if __name__ == "__main__":
    unittest.main()
