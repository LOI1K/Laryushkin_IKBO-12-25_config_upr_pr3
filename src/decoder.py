"""Decode binary instructions of the educational virtual machine."""

from src.machine_code import BITS_PER_BYTE, FORMATS, OPCODE_BITS


OPCODE_MASK = (1 << OPCODE_BITS) - 1


def decode_instruction(data, offset=0):
    """Decode one instruction and return its fields and size."""
    if offset < 0 or offset >= len(data):
        raise ValueError("Неверное смещение команды")

    opcode = data[offset] & OPCODE_MASK

    if opcode not in FORMATS:
        raise ValueError(f"Неизвестный код операции: {opcode}")

    widths = FORMATS[opcode]
    bit_count = OPCODE_BITS + sum(widths.values())
    size = (bit_count + BITS_PER_BYTE - 1) // BITS_PER_BYTE

    if offset + size > len(data):
        raise ValueError("Неполная машинная команда")

    value = int.from_bytes(data[offset:offset + size], "little")
    instruction = {"A": opcode}
    shift = OPCODE_BITS

    for field, width in widths.items():
        instruction[field] = (value >> shift) & ((1 << width) - 1)
        shift += width

    return instruction, size


def decode_program(data):
    """Decode all instructions from a binary program."""
    program = []
    offset = 0

    while offset < len(data):
        instruction, size = decode_instruction(data, offset)
        program.append(instruction)
        offset += size

    return program
