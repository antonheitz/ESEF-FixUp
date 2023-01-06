from typing import List
import zipfile
import os
from packages.worker.src.file_dataclasses import PackageFile

EXTRACT_FOLDER: str = "TMP_EXTRACT"

def extract_zip(file_path: str, working_dir: str) -> str:
    result_folder: str = os.path.join(working_dir, EXTRACT_FOLDER)
    with zipfile.ZipFile(file_path, 'r') as f:
        f.extractall(result_folder)
    return result_folder

def load_files(folder: str) -> List[PackageFile]:
    for r, d, f in os.walk(path):
        for file in f:
            print(file)