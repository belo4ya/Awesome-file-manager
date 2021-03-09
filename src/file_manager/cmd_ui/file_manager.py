import cmd
import os

from src.file_manager.core.manager import Manager, Answer
from src.file_manager.core.parser import Parser
from src.file_manager.utils import get_abspath


class FileManager(cmd.Cmd):

    def __init__(self, root: str = None):
        super(FileManager, self).__init__()
        self.intro = "Добро пожаловать в простой кроссплатформенный awesome файловый менеджер. " \
                     "Введи help или ? для получения списка команд.\n"

        self.root = root or get_abspath(os.getcwd())
        self.prompt = self._prompt()
        self.out_prompt = "--- "
        self.err_prompt = "*** "

        self._executor = Manager(str(self.root))
        self._parser = Parser()

    def postcmd(self, stop: bool, line: str) -> bool:
        self.prompt = self._prompt()
        return stop

    def do_root(self, args):
        paths, args = self._parser.parse(args)

        if self._unexpected_args(0, args):
            return

        self._on_answer(self._executor.root())

    def do_ls(self, args):
        paths, args = self._parser.parse(args)
        path = paths[0] if paths else os.getcwd()
        mask = ""

        if self._unexpected_args(0, args):
            return

        answer = self._executor.listdir(path, mask)
        if answer.returncode == 0:
            return self.columnize([p.name for p in answer.payload])
        return self._error_handler(answer.error)

    def do_cd(self, args):
        paths, args = self._parser.parse(args)
        path = paths[0] if paths else ""

        if self._unexpected_args(0, args):
            return

        self._on_answer(self._executor.change_dir(path))

    def do_mkdir(self, args):
        paths, args = self._parser.parse(args)
        path = paths[0] if paths else ""

        if self._unexpected_args(2, args):
            return

        self._on_answer(self._executor.create_dir(path, args))

    def do_rmdir(self, args):
        paths, args = self._parser.parse(args)
        path = paths[0] if paths else ""

        if self._unexpected_args(1, args):
            return

        self._on_answer(self._executor.remove_dir(path, args))

    def do_mkfile(self, args):
        paths, args = self._parser.parse(args)
        path = paths[0] if paths else ""

        if self._unexpected_args(1, args):
            return

        self._on_answer(self._executor.create_file(path, args))

    def do_rmfile(self, args):
        paths, args = self._parser.parse(args)
        path = paths[0] if paths else ""

        if self._unexpected_args(1, args):
            return

        self._on_answer(self._executor.remove_file(path, args))

    def do_write(self, args):
        paths, args = self._parser.parse(args)
        path = paths[0] if len(paths) > 0 else ""
        data = paths[1] if len(paths) > 1 else ""

        if self._unexpected_args(0, args):
            return

        self._on_answer(self._executor.write_file(path, data))

    def do_dog(self, args):
        paths, args = self._parser.parse(args)
        path = paths[0] if paths else ""

        if self._unexpected_args(0, args):
            return

        answer = self._executor.show_file(path)
        answer.msg = answer.payload
        self._on_answer(answer)

    def do_cp(self, args):
        paths, args = self._parser.parse(args)
        src = paths[0] if len(paths) > 0 else ""
        dst = paths[1] if len(paths) > 1 else ""

        if self._unexpected_args(1, args):
            return

        self._on_answer(self._executor.copy(src, dst, args))

    def do_mv(self, args):
        paths, args = self._parser.parse(args)
        src = paths[0] if len(paths) > 0 else ""
        dst = paths[1] if len(paths) > 1 else ""

        if self._unexpected_args(0, args):
            return

        self._on_answer(self._executor.move(src, dst))

    def do_rename(self, args):
        paths, args = self._parser.parse(args)
        src = paths[0] if len(paths) > 0 else ""
        dst = paths[1] if len(paths) > 1 else ""

        if self._unexpected_args(0, args):
            return

        self._on_answer(self._executor.rename(src, dst))

    def _unexpected_args(self, expected, args) -> bool:
        if len(args) > expected:
            self._stderr("Неожиданный(-е) аргумент(-ы): {}".format("'" + "', '".join(args[expected:]) + "'"))
            return True

        return False

    def _on_answer(self, answer: Answer):
        if answer.returncode == 0:
            return self._stdout(answer.msg)
        return self._error_handler(answer.error)

    def _stdout(self, msg: str):
        if msg:
            print(self.out_prompt + msg)

    def _stderr(self, msg: str):
        if msg:
            print(self.err_prompt + msg)

    def _error_handler(self, error):
        self._stderr(str(error))

    def _prompt(self):
        cwd = os.getcwd()
        return cwd[cwd.find(self.root.name):] + "::-> "
