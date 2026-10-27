"""Модуль реализации основных команд оболочки для этапа 4."""

import datetime
import platform
from typing import Callable, Dict, List

from src.vfs import VFSNode, VirtualFileSystem

EMPTY_COUNT = 0
SINGLE_ARG = 1


class CommandExecutor:
    """Исполнитель команд эмулятора оболочки ОС."""

    def __init__(self, vfs: VirtualFileSystem) -> None:
        """Инициализирует привязку команд этапа 4 к методам."""
        self.vfs = vfs
        self.should_exit = False
        self.handlers: Dict[str, Callable[[List[str]], str]] = {
            "ls": self.cmd_ls,
            "cd": self.cmd_cd,
            "date": self.cmd_date,
            "cat": self.cmd_cat,
            "uname": self.cmd_uname,
            "exit": self.cmd_exit,
        }

    def execute(self, cmd_name: str, args: List[str]) -> str:
        """Выполняет команду по имени или сообщает об ошибке."""
        handler = self.handlers.get(cmd_name)
        if handler is None:
            raise ValueError(f"{cmd_name}: команда не найдена")
        return handler(args)

    def cmd_exit(self, args: List[str]) -> str:
        """Завершает работу эмулятора."""
        if len(args) > EMPTY_COUNT:
            raise ValueError("exit: слишком много аргументов")
        self.should_exit = True
        return ""

    def cmd_ls(self, args: List[str]) -> str:
        """Выводит содержимое директории (поддерживает флаг -l)."""
        long_fmt = "-l" in args
        paths = [arg for arg in args if not arg.startswith("-")]
        flags = [arg for arg in args if arg.startswith("-") and arg != "-l"]
        if len(flags) > EMPTY_COUNT:
            raise ValueError(f"ls: неверный ключ '{flags[0]}'")
        target_path = paths[0] if len(paths) > EMPTY_COUNT else ""
        if len(paths) > SINGLE_ARG:
            raise ValueError("ls: слишком много аргументов")
        node = self.vfs.resolve_path(target_path)
        if node is None:
            raise ValueError(f"ls: нет доступа к '{target_path}': Нет файла")
        return self._format_ls_output(node, long_fmt)

    def _format_ls_output(self, node: VFSNode, long_fmt: bool) -> str:
        """Форматирует вывод команды ls для файла или директории."""
        items = list(node.children.values()) if node.is_dir else [node]
        if not long_fmt:
            return "  ".join(item.name for item in items)
        lines = []
        for item in items:
            kind = "d" if item.is_dir else "-"
            size = len(item.content)
            lines.append(f"{kind}rw-r--r-- {item.owner} {size:5d} {item.name}")
        return "\n".join(lines)

    def cmd_cd(self, args: List[str]) -> str:
        """Изменяет текущую рабочую директорию в VFS."""
        if len(args) > SINGLE_ARG:
            raise ValueError("cd: слишком много аргументов")
        target = args[0] if len(args) == SINGLE_ARG else "/"
        node = self.vfs.resolve_path(target)
        if node is None:
            raise ValueError(f"cd: {target}: Нет такого файла или каталога")
        if not node.is_dir:
            raise ValueError(f"cd: {target}: Не является каталогом")
        self.vfs.cwd = node
        return ""

    def cmd_date(self, args: List[str]) -> str:
        """Выводит текущую системную дату и время."""
        if len(args) > EMPTY_COUNT:
            raise ValueError("date: неверные аргументы")
        now = datetime.datetime.now(datetime.timezone.utc)
        return now.strftime("%a %b %d %H:%M:%S UTC %Y")

    def cmd_cat(self, args: List[str]) -> str:
        """Выводит содержимое одного или нескольких файлов из VFS."""
        if len(args) == EMPTY_COUNT:
            raise ValueError("cat: не указан файл")
        outputs = []
        for path in args:
            node = self.vfs.resolve_path(path)
            if node is None:
                raise ValueError(f"cat: {path}: Нет такого файла")
            if node.is_dir:
                raise ValueError(f"cat: {path}: Это каталог")
            outputs.append(node.content.rstrip("\n"))
        return "\n".join(outputs)

    def cmd_uname(self, args: List[str]) -> str:
        """Выводит информацию об операционной системе."""
        if len(args) == EMPTY_COUNT:
            return platform.system()
        if args == ["-a"]:
            info = platform.uname()
            return f"{info.system} {info.node} {info.release} {info.machine}"
        raise ValueError(f"uname: неверный ключ '{args[0]}'")
