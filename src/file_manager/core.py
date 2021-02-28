import os
import shutil
from pathlib import Path


class FileSystemApi:

    @staticmethod
    def getcwd() -> Path:
        return Path(os.getcwd())

    @staticmethod
    def change_dir(path: Path):
        os.chdir(path)

    @staticmethod
    def create_dir(path: Path, parents=False, exist_ok=False):
        path.mkdir(parents=parents, exist_ok=exist_ok)

    @staticmethod
    def remove_dir(path: Path, recursive=False):
        if recursive:
            shutil.rmtree(path)
        else:
            path.rmdir()

    @staticmethod
    def create_file(path: Path, exist_ok=True):
        path.touch(exist_ok=exist_ok)

    @staticmethod
    def remove_file(path: Path, missing_ok=False):
        if not path.is_file():
            raise FmNotAFileError(f"Указанный путь не является файлом: {path}")

        path.unlink(missing_ok=missing_ok)

    @staticmethod
    def write_file(path: Path, data: str, encoding="utf-8"):
        if not path.is_file():
            raise FmNotAFileError(f"Указанный путь не является файлом: {path}")

        path.write_text(data, encoding=encoding)

    @staticmethod
    def show_file(path: Path, encoding="utf-8"):
        if not path.is_file():
            raise FmNotAFileError(f"Указанный путь не является файлом: {path}")

        return path.read_text(encoding=encoding)

    @staticmethod
    def copy(src: Path, dst: Path, recursive=False):
        if recursive:
            shutil.copytree(src, dst)
        else:
            shutil.copy2(src, dst)

    @staticmethod
    def move(src: Path, dst: Path):
        shutil.move(src, dst)

    @staticmethod
    def rename(src: Path, dst: Path):
        if set(src.parents) != set(dst.parents):
            raise FmRenameError("Для перемещения файла или директории воспользуйтесь методом move")

        src.rename(dst)


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

    def __init__(self, root=None, target=None):
        message = f"Указанный путь находится за пределами корневого каталога: root - {root}, target - {target}"
        super(FmRootScopeError, self).__init__(message)


class FmFileExistsError(FileManagerError):
    pass


class FmDirExistsError(FileManagerError):
    pass


class FmRenameError(FileManagerError):
    pass
