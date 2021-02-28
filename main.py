from src.file_manager.manager import Manager
import os

if __name__ == '__main__':
    root_path = os.path.join(os.getcwd(), "test_dir")
    manager = Manager(root_path)
    print(manager.remove_dir("level_0/level_1", ["-r"]))
