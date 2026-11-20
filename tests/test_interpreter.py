"""Tests for the command-line interpreter."""

import json
import subprocess
import sys
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

from src.assembler import load_program, translate
from src.interpreter import save_dump
from src.machine_code import encode_program


class TestInterpreter(unittest.TestCase):
    """Check JSON dumps and command-line execution."""

    def test_save_dump(self):
        """Save the selected memory addresses."""
        with TemporaryDirectory() as directory:
            output = Path(directory) / "dump.json"
            save_dump([0, 7, 12, 25], 1, 3, output)

            result = json.loads(output.read_text())
            self.assertEqual(
                result, {"1": 7, "2": 12, "3": 25}
            )

    def test_invalid_range(self):
        """Reject an invalid dump address range."""
        with TemporaryDirectory() as directory:
            output = Path(directory) / "dump.json"

            with self.assertRaises(ValueError):
                save_dump([0, 7], 1, 2, output)

    def test_cli_copy_array(self):
        """Execute a binary file and check its JSON dump."""
        source = load_program("examples/copy_array.yaml")
        binary = encode_program(translate(source))

        with TemporaryDirectory() as directory:
            program = Path(directory) / "copy.bin"
            output = Path(directory) / "dump.json"
            program.write_bytes(binary)

            result = subprocess.run(
                [
                    sys.executable, "-m", "src.interpreter",
                    str(program), str(output),
                    "--start", "200", "--end", "202",
                ],
                capture_output=True,
                text=True,
                check=False,
            )

            self.assertEqual(result.returncode, 0)
            data = json.loads(output.read_text())
            self.assertEqual(
                data, {"200": 7, "201": 12, "202": 25}
            )


if __name__ == "__main__":
    unittest.main()
