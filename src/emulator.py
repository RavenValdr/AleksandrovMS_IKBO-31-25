"""Главный модуль эмулятора командной строки ОС."""

import argparse
import getpass
import os
import socket
import sys
from typing import List

from src.commands import CommandExecutor
from src.vfs import VirtualFileSystem

EMPTY_LEN = 0


def parse_input(line: str) -> List[str]:
    """Раскрывает переменные окружения ОС и разбивает строку."""
    expanded = os.path.expandvars(line.strip())
    return expanded.split() if expanded else []


def build_prompt(vfs: VirtualFileSystem) -> str:
    """Формирует приглашение к вводу на основе реальных данных ОС."""
    user = getpass.getuser()
    host = socket.gethostname()
    cwd = vfs.get_cwd_path()
    display_cwd = "~" if cwd == "/" else f"~{cwd}"
    return f"{user}@{host}:{display_cwd}$ "


def run_line(line: str, executor: CommandExecutor) -> None:
    """Парсит и выполняет одну строку команды."""
    tokens = parse_input(line)
    if len(tokens) == EMPTY_LEN:
        return
    try:
        output = executor.execute(tokens[0], tokens[1:])
        if output:
            print(output)
    except ValueError as err:
        print(f"Ошибка: {err}")


def execute_script(script_path: str, executor: CommandExecutor) -> None:
    """Последовательно выполняет стартовый скрипт, пропуская ошибки."""
    if not os.path.isfile(script_path):
        print(f"Ошибка скрипта: файл не найден: {script_path}")
        return
    with open(script_path, "r", encoding="utf-8") as script_file:
        for raw_line in script_file:
            clean = raw_line.strip()
            if not clean:
                continue
            print(f"{build_prompt(executor.vfs)}{clean}")
            run_line(clean, executor)
            if executor.should_exit:
                break


def repl_loop(executor: CommandExecutor) -> None:
    """Запускает интерактивный цикл чтения-выполнения-вывода (REPL)."""
    while not executor.should_exit:
        try:
            line = input(build_prompt(executor.vfs))
            run_line(line, executor)
        except (EOFError, KeyboardInterrupt):
            print()
            break


def main() -> None:
    """Точка входа: чтение аргументов, загрузка VFS и старт эмулятора."""
    parser = argparse.ArgumentParser(description="UNIX Shell Emulator")
    parser.add_argument("--vfs", required=True, help="Путь к директории VFS")
    parser.add_argument("--script", default="", help="Путь к скрипту")
    args = parser.parse_args()
    print(f"[DEBUG] VFS path: {args.vfs}")
    print(f"[DEBUG] Script path: {args.script}")
    vfs = VirtualFileSystem()
    try:
        vfs.load_from_directory(args.vfs)
    except (FileNotFoundError, ValueError) as err:
        print(f"Ошибка загрузки VFS: {err}")
        sys.exit(1)
    executor = CommandExecutor(vfs)
    if args.script:
        execute_script(args.script, executor)
    if not executor.should_exit:
        repl_loop(executor)


if __name__ == "__main__":
    main()
