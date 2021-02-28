import os
import re
from pathlib import Path
from typing import List

from src.file_manager.core import FileSystemApi
from src.file_manager.utils import get_abspath


class Manager:

    def __init__(self, root: str):
        self._root = get_abspath(root)
        os.chdir(self._root)

        self._file_system = FileSystemApi

    @property
    def cwd(self):
        return self._file_system.getcwd()

    def change_dir(self, path: str) -> "Answer":
        if re.fullmatch(r"\.+", path):
            n_steps = len(path) - 2
            if n_steps > len(self.cwd.parents):
                return Answer(
                    returncode=1,
                    stderr=f"Попытка выхода за пределы корневого каталога: root - {self._root}, target - {path}.",
                    error=RootScopeError
                )

            path = self.cwd.parents[len(path) - 2]
        else:
            path = get_abspath(path)

        if not self._in_scope_root(path):
            return Answer(
                returncode=1,
                stderr=f"Попытка выхода за пределы корневого каталога: root - {self._root}, target - {path}.",
                error=RootScopeError
            )

        try:
            self._file_system.change_dir(path)
        except NotADirectoryError as e:
            return Answer(
                returncode=1,
                stderr=f"Неверно задано имя папки: {path}.",
                error=e
            )
        except FileNotFoundError as e:
            return Answer(
                returncode=1,
                stderr=f"Неверно задано имя папки: {path}.",
                error=e
            )

        return Answer(returncode=0, stdout="")

    def create_dir(self, path: str, args: List[str]) -> "Answer":
        path = get_abspath(path)
        parents = "-p" in args
        exist_ok = "-q" in args

        if not self._in_scope_root(path):
            return Answer(
                returncode=1,
                stderr=f"Попытка выхода за пределы корневого каталога: root - {self._root}, target - {path}.",
                error=RootScopeError
            )

        if not self._is_valid_params(["-p", "-q"], args):
            return Answer(
                returncode=1,
                stderr=f"Недопустимый параметр.",
                error=OptionError
            )

        try:
            self._file_system.create_dir(path, parents=parents, exist_ok=exist_ok)
        except FileExistsError as e:
            return Answer(
                returncode=1,
                stderr=e.strerror,
                error=FileExistsError
            )
        except FileNotFoundError as e:
            return Answer(
                returncode=1,
                stderr=e.strerror,
                error=FileNotFoundError
            )

        return Answer(returncode=0, stdout="")

    def remove_dir(self, path: str, args: List[str]) -> "Answer":
        path = get_abspath(path)
        recursive = "-r" in args

        if not self._in_scope_root(path):
            return Answer(
                returncode=1,
                stderr=f"Попытка выхода за пределы корневого каталога: root - {self._root}, target - {path}.",
                error=RootScopeError
            )

        if not self._is_valid_params(["-r"], args):
            raise OptionError

        self._file_system.remove_dir(path, recursive=recursive)

    def create_file(self, path: str, args: List[str]) -> "Answer":
        path = get_abspath(path)
        exist_ok = "-q" in args

        if not self._in_scope_root(path):
            return Answer(
                returncode=1,
                stderr=f"Попытка выхода за пределы корневого каталога: root - {self._root}, target - {path}.",
                error=RootScopeError
            )

        if not self._is_valid_params(["-q"], args):
            raise OptionError

        self._file_system.create_file(path, exist_ok=exist_ok)

    def remove_file(self, path: str, args: List[str]) -> "Answer":
        path = get_abspath(path)
        missing_ok = "-q" in args

        if not self._in_scope_root(path):
            return Answer(
                returncode=1,
                stderr=f"Попытка выхода за пределы корневого каталога: root - {self._root}, target - {path}.",
                error=RootScopeError
            )

        if not self._is_valid_params(["-q"], args):
            raise OptionError

        self._file_system.remove_file(path, missing_ok=missing_ok)

    def write_file(self, path: str, data: str, args: List[str]) -> "Answer":
        path = get_abspath(path)

        if not self._in_scope_root(path):
            return Answer(
                returncode=1,
                stderr=f"Попытка выхода за пределы корневого каталога: root - {self._root}, target - {path}.",
                error=RootScopeError
            )

        self._file_system.write_file(path, data)

    def show_file(self, path: str, args: List[str]) -> "Answer":
        pass

    def copy(self, src: str, dst: str, args: List[str]) -> "Answer":
        pass

    def move(self, src: str, dst: str, args: List[str]) -> "Answer":
        pass

    def rename(self, src: str, dst: str, args: List[str]) -> "Answer":
        pass

    def _in_scope_root(self, path: Path) -> bool:
        return path == self._root or self._root in path.parents

    @staticmethod
    def _is_valid_params(params: List[str], args: List[str]):
        for arg in args:
            if arg not in params:
                return False

        return True


class Answer:

    def __init__(self, returncode, stdout="", stderr="", error=None):
        self.returncode = returncode
        self.stdout = stdout
        self.stderr = stderr
        self.error = error


class RootScopeError(OSError):
    def __init__(self, root=None, target=None):
        message = f"Попытка выхода за пределы корневого каталога: root - {root}, target - {target}."
        super(RootScopeError, self).__init__(message)


class OptionError(OSError):
    def __init__(self):
        message = f"Недопустимый параметр."
        super(OptionError, self).__init__(message)
