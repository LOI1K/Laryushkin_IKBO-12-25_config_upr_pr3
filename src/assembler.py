"""Translate YAML instructions to an intermediate representation."""

from pathlib import Path

import yaml


INSTRUCTIONS = {
    "LOAD": (4, {"B": 13, "C": 5}),
    "READ": (6, {"B": 5, "C": 5, "D": 6}),
    "STORE": (3, {"B": 5, "C": 5}),
    "AND": (1, {"B": 5, "C": 32, "D": 5}),
}


def load_program(path):
    """Read an assembly program from a YAML file."""
    with Path(path).open(encoding="utf-8") as file:
        return yaml.safe_load(file)


def parse_instruction(raw):
    """Validate an instruction and convert it to fields."""
    if not isinstance(raw, dict):
        raise ValueError("Команда должна быть объектом YAML")

    name = raw.get("command")

    if not isinstance(name, str) or name not in INSTRUCTIONS:
        raise ValueError("Неизвестная команда")

    opcode, widths = INSTRUCTIONS[name]
    expected = set(widths) | {"command"}

    if set(raw) != expected:
        raise ValueError(f"Неверные поля команды {name}")

    result = {"A": opcode}

    for field, width in widths.items():
        value = raw[field]

        if type(value) is not int or not 0 <= value < (1 << width):
            raise ValueError(f"{name}: неверное значение {field}")

        result[field] = value

    return result


def translate(program):
    """Translate a program to an instruction list."""
    if not isinstance(program, list) or not program:
        raise ValueError("Программа должна быть непустым списком")

    return [parse_instruction(item) for item in program]
