"""Tests for virtual machine execution."""

import unittest

from src.assembler import load_program, translate
from src.machine_code import encode_program
from src.virtual_machine import MEMORY_SIZE, VirtualMachine


class TestVirtualMachine(unittest.TestCase):
    """Check registers, memory and instruction execution."""

    def test_copy_array(self):
        """Copy three values to another memory area."""
        source = load_program("examples/copy_array.yaml")
        code = encode_program(translate(source))

        machine = VirtualMachine(code)
        machine.run()

        self.assertEqual(machine.memory[100:103], [7, 12, 25])
        self.assertEqual(machine.memory[200:203], [7, 12, 25])

    def test_load_constant(self):
        """Load an immediate value into a register."""
        machine = VirtualMachine(b"")
        machine.execute({"A": 4, "B": 42, "C": 1})
        self.assertEqual(machine.registers[1], 42)

    def test_read_with_offset(self):
        """Read memory using a base register and offset."""
        machine = VirtualMachine(b"")
        machine.registers[0] = 100
        machine.memory[102] = 37

        machine.execute({"A": 6, "B": 0, "C": 1, "D": 2})
        self.assertEqual(machine.registers[1], 37)

    def test_invalid_address(self):
        """Reject writes outside data memory."""
        machine = VirtualMachine(b"")
        machine.registers[1] = 15
        machine.registers[2] = MEMORY_SIZE

        with self.assertRaises(ValueError):
            machine.execute({"A": 3, "B": 1, "C": 2})

    def test_and_operation(self):
        """Apply bitwise AND to memory and register values."""
        machine = VirtualMachine(b"")
        machine.memory[100] = 12
        machine.registers[2] = 10

        machine.execute({"A": 1, "B": 2, "C": 100, "D": 4})

        self.assertEqual(machine.registers[4], 8)
        self.assertEqual(machine.memory[100], 12)

    def test_and_invalid_address(self):
        """Reject invalid memory addresses in AND instructions."""
        machine = VirtualMachine(b"")

        with self.assertRaises(ValueError):
            machine.execute({
                "A": 1, "B": 2,
                "C": MEMORY_SIZE, "D": 4,
            })



if __name__ == "__main__":
    unittest.main()
