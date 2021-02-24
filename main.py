from file_manager import FileManager
import os

if __name__ == '__main__':
    root_path = os.path.join(os.getcwd(), "test_dir")
    file_manager = FileManager(root_path)
    print(file_manager.root)
    print(file_manager.cwd)
    file_manager.create_dir("D:/PyProjects/")
