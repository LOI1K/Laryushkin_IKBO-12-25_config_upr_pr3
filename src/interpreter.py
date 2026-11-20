"""Command-line interpreter for the educational virtual machine."""

import argparse
import json
import sys
from pathlib import Path

from src.virtual_machine import VirtualMachine


def save_dump(memory, start, end, path):
    """Save an inclusive memory address range to JSON."""
    if not 0 <= start <= end < len(memory):
        raise ValueError("Недопустимый диапазон памяти")

    data = {
        str(address): memory[address]
        for address in range(start, end + 1)
    }

    output = Path(path)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(
        json.dumps(data, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def main():
    """Execute a binary program and save its memory dump."""
    parser = argparse.ArgumentParser(
        description="Интерпретатор учебной виртуальной машины"
    )
    parser.add_argument("program", help="Бинарная программа")
    parser.add_argument("dump", help="Выходной JSON-файл")
    parser.add_argument("--start", type=int, required=True)
    parser.add_argument("--end", type=int, required=True)

    args = parser.parse_args()

    try:
        code = Path(args.program).read_bytes()
        machine = VirtualMachine(code)
        machine.run()

        save_dump(
            machine.memory, args.start, args.end, args.dump
        )
    except (OSError, ValueError) as error:
        print(f"Ошибка: {error}", file=sys.stderr)
        return 1

    print("Программа выполнена успешно")
    print(f"Дамп памяти сохранён: {args.dump}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
