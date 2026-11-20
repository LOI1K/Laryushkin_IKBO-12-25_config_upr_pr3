"""Command-line assembler for the educational virtual machine."""

import argparse
import sys
from pathlib import Path

import yaml

from src.assembler import load_program, translate
from src.machine_code import encode_instruction, encode_program


def print_test_output(program):
    """Display instruction fields and encoded bytes."""
    for instruction in program:
        fields = ", ".join(
            f"{name}={value}"
            for name, value in instruction.items()
        )
        byte_values = ", ".join(
            f"0x{byte:02X}"
            for byte in encode_instruction(instruction)
        )
        print(f"{fields} -> {byte_values}")


def main():
    """Assemble a YAML program into a binary file."""
    parser = argparse.ArgumentParser(
        description="Ассемблер учебной виртуальной машины"
    )
    parser.add_argument("source", help="Исходный YAML-файл")
    parser.add_argument("output", help="Выходной бинарный файл")
    parser.add_argument(
        "--test",
        action="store_true",
        help="Вывести поля команд и машинные байты",
    )

    args = parser.parse_args()

    try:
        program = translate(load_program(args.source))
        binary = encode_program(program)

        output = Path(args.output)
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_bytes(binary)
    except (OSError, yaml.YAMLError, ValueError) as error:
        print(f"Ошибка: {error}", file=sys.stderr)
        return 1

    print(f"Ассемблировано команд: {len(program)}")
    print(f"Размер двоичного файла: {len(binary)} байт")

    if args.test:
        print_test_output(program)

    return 0


if __name__ == "__main__":
    sys.exit(main())
