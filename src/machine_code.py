"""Encode virtual machine instructions into binary data."""

from src.assembler import INSTRUCTIONS


OPCODE_BITS = 3
BITS_PER_BYTE = 8

FORMATS = {
    opcode: widths
    for opcode, widths in INSTRUCTIONS.values()
}


def encode_instruction(instruction):
    """Encode one instruction using little-endian byte order."""
    opcode = instruction["A"]

    if opcode not in FORMATS:
        raise ValueError(f"Неизвестный код операции: {opcode}")

    value = opcode
    shift = OPCODE_BITS

    for field, width in FORMATS[opcode].items():
        value |= instruction[field] << shift
        shift += width

    size = (shift + BITS_PER_BYTE - 1) // BITS_PER_BYTE

    return value.to_bytes(size, "little")


def encode_program(program):
    """Encode all instructions into one binary sequence."""
    return b"".join(
        encode_instruction(instruction)
        for instruction in program
    )
