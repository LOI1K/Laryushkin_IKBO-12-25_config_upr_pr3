"""Virtual machine with registers and separate data memory."""

from src.decoder import decode_instruction


REGISTER_COUNT = 32
MEMORY_SIZE = 65536


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

        if opcode == 4:
            self.registers[instruction["C"]] = instruction["B"]

        elif opcode == 6:
            address = (
                self.registers[instruction["B"]]
                + instruction["D"]
            )
            self.check_address(address)
            self.registers[instruction["C"]] = self.memory[address]

        elif opcode == 3:
            address = self.registers[instruction["C"]]
            self.check_address(address)
            self.memory[address] = self.registers[instruction["B"]]

        elif opcode == 1:
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
