"""Command-line assembler for the educational virtual machine."""

import argparse
import sys

import yaml

from src.assembler import load_program, translate


def main():
    """Read and translate an assembly program."""
    parser = argparse.ArgumentParser(
        description="Ассемблер учебной виртуальной машины"
    )
    parser.add_argument("source", help="Исходный YAML-файл")
    parser.add_argument("output", help="Выходной бинарный файл")
    parser.add_argument(
        "--test",
        action="store_true",
        help="Вывести промежуточное представление",
    )

    args = parser.parse_args()

    try:
        program = translate(load_program(args.source))
    except (OSError, yaml.YAMLError, ValueError) as error:
        print(f"Ошибка: {error}", file=sys.stderr)
        return 1

    if args.test:
        for instruction in program:
            fields = (
                f"{name}={value}"
                for name, value in instruction.items()
            )
            print(", ".join(fields))
    else:
        print(f"Команд разобрано: {len(program)}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
