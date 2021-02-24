import os
import shutil
from pathlib import Path


class FileManager:

    def __init__(self, path: str):
        path = Path(path).absolute()

        try:
            os.chdir(path)
        except FileNotFoundError:
            raise FmRootDirNotFoundError(f"Не удается найти корневую директорию: {path}") from None

        self._root: Path = path
        self._cwd: Path = self._root

    @property
    def root(self) -> str:
        return str(self._root)

    @property
    def cwd(self) -> str:
        return str(self._cwd)

    def set_cwd(self, path: str):
        path = Path(path).absolute()

        if not path.is_dir():
            raise FmNotADirectoryError(f"Указанный путь не является директорией: {path}")

        if not self._in_scope_root(path):
            raise FmRootScopeError(f"Указанный путь находится за пределами корневого каталога: "
                                   f"target - {path}, root - {self._root}")

        try:
            os.chdir(path.name)
        except FileNotFoundError:
            raise FmDirNotFoundError(f"Не удается найти указанный каталог: {path}") from None

        self._cwd = path

    def create_dir(self, path: str, parents=False, exist_ok=False):
        path = Path(path).absolute()

        if not self._in_scope_root(path):
            raise FmRootScopeError(f"Указанный путь находится за пределами корневого каталога: "
                                   f"target - {path}, root - {self._root}")
        try:
            path.mkdir(parents=parents, exist_ok=exist_ok)
        except FileExistsError:
            raise FmDirExistsError(f"Невозможно создать каталог, так как он уже существует: {path}") from None
        except FileNotFoundError:
            raise FmDirNotFoundError(f"Не удается найти указанный путь: {path}") from None

    def remove_dir(self, path: str):
        self._cwd.joinpath(path).rmdir()  # удаляет пустую директорию
        os.removedirs(path)  # удаляет директории рекурсивно - только пустые
        shutil.rmtree(path)  # удаляет директорию рекурсивно

    def change_dir(self, path: str):
        os.chdir(path)
        self.set_cwd(path)

    def create_file(self, path: str):
        self._cwd.joinpath(path).touch()

    def write_file(self, path: str, data: str):
        self._cwd.joinpath(path).write_text(data)

    def show_file(self, path: str):
        return self._cwd.joinpath(path).read_text()

    def remove_file(self, path: str):
        self._cwd.joinpath(path).unlink()

    def copy_file(self, src: str, dst: str):
        shutil.copy2(src, dst)

    def move_file(self, src: str, dst: str):
        shutil.move(src, dst)

    def rename_file(self, target: str):
        self._cwd.joinpath().rename(target)

    def _make_absolute(self, path: str) -> Path:
        path = Path(path)
        if not path.is_absolute():
            path = self._cwd.joinpath(path)

        return path

    def _in_scope_root(self, path: Path) -> bool:
        return self._root in path.parents


class FileManagerError(OSError):
    pass


class FmNotADirectoryError(FileManagerError):
    pass


class FmNotAFileError(FileManagerError):
    pass


class FmFileNotFoundError(FileManagerError):
    pass


class FmDirNotFoundError(FmFileNotFoundError):
    pass


class FmRootDirNotFoundError(FmDirNotFoundError):
    pass


class FmRootScopeError(FileManagerError):
    pass


class FmFileExistsError(FileManagerError):
    pass


class FmDirExistsError(FileManagerError):
    pass
