import io
import os
import shutil
from typing import BinaryIO, Union

from packages.file_handling.dataclasses import FileInformation

TMP_STORAGE_PATH = os.path.join(os.getcwd(), "tmp-storage")
FINAL_PREFIX: str = "FINAL_FILE-"

class FileHandler:
    def __init__(self) -> None:
        # create tmp folder if it does not exist yet
        if not os.path.exists(TMP_STORAGE_PATH):
            os.mkdir(TMP_STORAGE_PATH)
        
    def save_file(self, file_id: Union[str, int], filename: str, file: BinaryIO) -> FileInformation:
        workdir: str = os.path.join(TMP_STORAGE_PATH, str(file_id))
        os.mkdir(workdir)
        filepath: str = os.path.join(workdir, filename)
        with open(filepath, 'wb+') as f:
            f.write(file.read())
        return FileInformation(
            name=filename,
            path=filepath,
            workdir=workdir
        )

    def delete_file(self, workdir: str) -> None:
        shutil.rmtree(workdir)

    def final_folder(self, id: str) -> str:
        return FINAL_PREFIX + str(id)