from src.file_manager.manager import Manager
import os

if __name__ == '__main__':
    root_path = os.path.join(os.getcwd(), "test_dir")
    manager = Manager(root_path)
    print(manager.cwd)
    print(manager.change_dir("level_0/test_on_level_2/").stdout)
    print(manager.cwd)
    manager.change_dir(".....")
    print(manager.cwd)
