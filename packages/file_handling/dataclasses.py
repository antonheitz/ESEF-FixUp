from dataclasses import dataclass


@dataclass
class FileInformation:
    name: str
    path: str
    workdir: str