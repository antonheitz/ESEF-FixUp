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
        
    def save_file(self, file_id: Union[str, int], filename: str, file: io.BytesIO) -> FileInformation:
        workdir: str = os.path.join(TMP_STORAGE_PATH, str(file_id))
        os.mkdir(workdir)
        filepath: str = os.path.join(workdir, filename)
        with open(filepath, 'wb+') as f:
            f.write(file.getbuffer())
        return FileInformation(
            name=filename,
            path=filepath,
            workdir=workdir
        )

    def delete_file(self, workdir: str) -> None:
        shutil.rmtree(workdir)

    def final_folder(self, id: str) -> str:
        return FINAL_PREFIX + str(id)

    def create_zip(self, id: str, file_name: str, source: str) -> FileInformation:
        workdir: str = os.path.join(TMP_STORAGE_PATH, self.final_folder(id))
        os.mkdir(workdir)
        destination = os.path.join(workdir, file_name)
        base = os.path.basename(destination)
        name = ".".join(base.split('.')[:-1])
        format = base.split('.')[-1]
        archive_from = os.path.dirname(source)
        archive_to = os.path.basename(source.strip(os.sep))
        shutil.make_archive(name, format, archive_from, archive_to)
        shutil.move('%s.%s'%(name,format), destination)
        return FileInformation(
            name=file_name,
            path=destination,
            workdir=workdir
        )