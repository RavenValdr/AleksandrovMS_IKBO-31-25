"""Модульные тесты для проверки команд этапов 4 и 5."""

import os
import tempfile
import unittest

from src.commands import CommandExecutor
from src.vfs import VirtualFileSystem


class TestShellEmulator(unittest.TestCase):
    """Набор тестов для основных и дополнительных команд эмулятора."""

    def setUp(self) -> None:
        """Создает временную директорию и загружает ее в VFS."""
        self.temp_dir = tempfile.TemporaryDirectory()
        root = self.temp_dir.name
        os.makedirs(os.path.join(root, "sub"))
        file_path = os.path.join(root, "sub", "note.txt")
        with open(file_path, "w", encoding="utf-8") as file_obj:
            file_obj.write("Hello VFS")
        self.vfs = VirtualFileSystem()
        self.vfs.load_from_directory(root)
        self.executor = CommandExecutor(self.vfs)

    def tearDown(self) -> None:
        """Удаляет временную директорию после завершения теста."""
        self.temp_dir.cleanup()

    def test_ls_and_cd(self) -> None:
        """Проверяет навигацию cd и вывод списка файлов ls."""
        self.assertEqual(self.executor.execute("ls", []), "sub")
        self.executor.execute("cd", ["sub"])
        self.assertEqual(self.executor.execute("ls", []), "note.txt")
        self.executor.execute("cd", [".."])
        self.assertEqual(self.vfs.get_cwd_path(), "/")

    def test_cat_date_uname(self) -> None:
        """Проверяет работу команд cat, date и uname."""
        content = self.executor.execute("cat", ["sub/note.txt"])
        self.assertEqual(content, "Hello VFS")
        self.assertTrue(len(self.executor.execute("date", [])) > 0)
        self.assertTrue(len(self.executor.execute("uname", ["-a"])) > 0)

    def test_chown_in_memory(self) -> None:
        """Проверяет смену владельца узла в памяти без изменения диска."""
        self.executor.execute("chown", ["root", "sub/note.txt"])
        out = self.executor.execute("ls", ["-l", "sub"])
        self.assertIn("root", out)
        with self.assertRaises(ValueError):
            self.executor.execute("chown", ["root"])


if __name__ == "__main__":
    unittest.main()
