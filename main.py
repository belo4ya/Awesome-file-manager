from src.file_manager.cmd_ui.file_manager import FileManager
import os

if __name__ == '__main__':
    root_path = os.path.join(os.getcwd(), "test_dir")
    FileManager().cmdloop()
