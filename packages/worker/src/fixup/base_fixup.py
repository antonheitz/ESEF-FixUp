from dataclasses import dataclass
from typing import List
from packages.worker.src.file_dataclasses import PackageFile


@dataclass
class FixupOptions:
    undercover: bool = False


class BaseFixup:
    def __init__(self, name: str):
        self.name: str = name

    def run(self, files: List[PackageFile], options: FixupOptions) -> None:
        print(f"Starting fixup {self.name}...")
        for file in files:
            self.run_file(file, options)
        print(f"Finished fixup {self.name}.")

    def run_file(self, file: PackageFile, options: FixupOptions) -> None:
        pass
