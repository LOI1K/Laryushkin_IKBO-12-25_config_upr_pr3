"""Virtual machine with registers and separate data memory."""

from src.assembler import INSTRUCTIONS
from src.decoder import decode_instruction


REGISTER_COUNT = 32
MEMORY_SIZE = 65536
LOAD_OPCODE = INSTRUCTIONS["LOAD"][0]
READ_OPCODE = INSTRUCTIONS["READ"][0]
STORE_OPCODE = INSTRUCTIONS["STORE"][0]
AND_OPCODE = INSTRUCTIONS["AND"][0]


class VirtualMachine:
    """Execute instructions of the educational virtual machine."""

    def __init__(self, code):
        """Initialize instruction memory, registers and data memory."""
        self.code = bytes(code)
        self.registers = [0] * REGISTER_COUNT
        self.memory = [0] * MEMORY_SIZE

    def check_address(self, address):
        """Reject addresses outside data memory."""
        if not 0 <= address < MEMORY_SIZE:
            raise ValueError(f"Недопустимый адрес памяти: {address}")

    def execute(self, instruction):
        """Execute a virtual machine instruction."""
        opcode = instruction["A"]

        if opcode == LOAD_OPCODE:
            self.registers[instruction["C"]] = instruction["B"]

        elif opcode == READ_OPCODE:
            address = (
                self.registers[instruction["B"]]
                + instruction["D"]
            )
            self.check_address(address)
            self.registers[instruction["C"]] = self.memory[address]

        elif opcode == STORE_OPCODE:
            address = self.registers[instruction["C"]]
            self.check_address(address)
            self.memory[address] = self.registers[instruction["B"]]

        elif opcode == AND_OPCODE:
            address = instruction["C"]
            self.check_address(address)
            self.registers[instruction["D"]] = (
                self.memory[address] & self.registers[instruction["B"]]
            )

        else:
            raise ValueError(f"Неизвестная команда: {opcode}")


    def run(self):
        """Decode and execute the machine-code program."""
        offset = 0

        while offset < len(self.code):
            instruction, size = decode_instruction(
                self.code, offset
            )
            self.execute(instruction)
            offset += size
