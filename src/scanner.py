import os


SKIPPED_FILES = ("venv", "__pycache__", "Anaconda3", "AppData", "Application Data",
                 "Cookies", "Local Settings", "desktop.ini")


class BaseFileScanHandler:
    def handle_file(self, filename: str, path: str, stats: os.stat_result):
        print(filename, path, stats.st_size, stats.st_ctime, stats.st_mtime)

# todo add source


class FileScanner:
    def __init__(self, handler: BaseFileScanHandler, max_depth: int):
        self.file_scan_handler = handler
        self.max_depth = max_depth

    def process_dir(self, path: str, depth: int) -> None:
        try:
            for dir_entry in os.scandir(path):
                if dir_entry.name == ".git":
                    print(f"Skipping due to git presence: {path}")
                    break

                if self._should_skip_file(dir_entry.name, depth):
                    continue

                if dir_entry.is_dir():
                    self.process_dir(dir_entry.path, depth + 1)

                else:
                    self.process_file(dir_entry.name, dir_entry.path, depth + 1)

        except Exception as e:
            print(f"Skipping {path}, {e}")

    # Depth first folder processing
    def process_file(self, filename: str, path: str, depth: int) -> None:
        if self._should_skip_file(filename, depth):
            return

        stats = os.lstat(path)
        self.file_scan_handler.handle_file(filename, path, stats)

    @classmethod
    def _is_directory(cls, stats: os.stat_result) -> bool:
        return stats.st_mode == 16895

    @classmethod
    def _concat_paths(cls, filename1: str, filename2: str) -> str:
        return f"{filename1}/{filename2}"

    def _should_skip_file(self, filename: str, depth: int):
        if depth > self.max_depth:
            # print(f"Skipping file due to max depth: {filename}")
            return True
        if filename in SKIPPED_FILES:
            print(f"Skipping file due to skip list: {filename}")
            return True
        if filename[0] == ".":
            # print(f"Skipping hidden file: {filename}")
            return True
        return False
