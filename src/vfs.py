"""Модуль виртуальной файловой системы (VFS), работающей в памяти."""

import getpass
import os
from dataclasses import dataclass, field
from typing import Dict, Optional


@dataclass
class VFSNode:
    """Узел виртуальной файловой системы (файл или директория)."""

    name: str
    is_dir: bool
    owner: str = field(default_factory=getpass.getuser)
    content: str = ""
    children: Dict[str, "VFSNode"] = field(default_factory=dict)
    parent: Optional["VFSNode"] = None


class VirtualFileSystem:
    """Класс управления VFS в оперативной памяти."""

    def __init__(self) -> None:
        """Инициализирует пустую VFS с корневым узлом."""
        self.root = VFSNode(name="", is_dir=True)
        self.root.parent = self.root
        self.cwd = self.root

    def load_from_directory(self, physical_path: str) -> None:
        """Загружает структуру директории с диска в память."""
        if not os.path.exists(physical_path):
            raise FileNotFoundError(f"VFS не найдена: {physical_path}")
        if not os.path.isdir(physical_path):
            raise ValueError(f"Неверный формат VFS: {physical_path}")
        self._populate_node(self.root, physical_path)

    def _populate_node(self, node: VFSNode, current_path: str) -> None:
        """Рекурсивно заполняет узел VFS данными из директории."""
        for entry in sorted(os.listdir(current_path)):
            full_path = os.path.join(current_path, entry)
            if os.path.isdir(full_path):
                child = VFSNode(name=entry, is_dir=True, parent=node)
                node.children[entry] = child
                self._populate_node(child, full_path)
            elif os.path.isfile(full_path):
                text = self._read_file_safe(full_path)
                child = VFSNode(
                    name=entry, is_dir=False, content=text, parent=node
                )
                node.children[entry] = child

    def _read_file_safe(self, file_path: str) -> str:
        """Безопасно считывает текстовое содержимое файла в память."""
        try:
            with open(file_path, "r", encoding="utf-8") as file_obj:
                return file_obj.read()
        except OSError as exc:
            raise ValueError(f"Ошибка чтения файла: {file_path}") from exc

    def resolve_path(self, path: str) -> Optional[VFSNode]:
        """Разрешает абсолютный или относительный путь в узел VFS."""
        if not path:
            return self.cwd
        current = self.root if path.startswith("/") else self.cwd
        for part in path.strip("/").split("/"):
            if not part or part == ".":
                continue
            if part == "..":
                current = current.parent if current.parent else self.root
            elif current.is_dir and part in current.children:
                current = current.children[part]
            else:
                return None
        return current

    def get_cwd_path(self) -> str:
        """Возвращает полный путь текущей директории внутри VFS."""
        if self.cwd == self.root:
            return "/"
        parts = []
        curr: Optional[VFSNode] = self.cwd
        while curr and curr != self.root:
            parts.append(curr.name)
            curr = curr.parent
        return "/" + "/".join(reversed(parts))
