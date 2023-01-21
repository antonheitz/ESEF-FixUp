from io import BytesIO
import shutil
import sys
import os
import traceback
from typing import List
from packages.file_handling.FileHandler import FileHandler
from packages.file_handling.dataclasses import FileInformation
from packages.worker.src.fix_all import fix_files
from packages.worker.src.file_utils import load_files, save_files
from packages.worker.src.fixup.base_fixup import FixupOptions

args: List[str] = sys.argv
# extract flags:
options: FixupOptions = FixupOptions()
if "--undercover" in args:
    options.undercover = True
    args = [arg for arg in args if arg != "--undercover"]


# check if the needed parameters are called
if len(args) != 3:
    print("ERROR: Please provide 2 arguments: cli.sh \"path to zip\" \"output zip path & name\"")
    exit(1)

original_file: str = sys.argv[1]
file_name: str = original_file.split(os.path.sep)[-1]
destination_file: str = sys.argv[2]

file_handler: FileHandler = FileHandler()

try:
    print(f"Using file {original_file}")
    # load file into BytesIO object
    with open(original_file, "rb") as f:
        file: BytesIO = BytesIO(f.read())
    file_information: FileInformation = file_handler.save_file(
        1, file_name, file)
    files, result_folder = load_files(
        file_information.path, file_information.workdir, options)
    # run works on the ZIP
    fix_files(files, options)
    save_files(files)
    final_file: FileInformation = file_handler.create_zip(
        1, file_name, os.path.join(result_folder, files[0].zip_root))
    file_handler.delete_file(file_information.workdir)
    # send final file to api
    print(f"Creating file {destination_file}")
    shutil.copy(final_file.path, destination_file)
    file_handler.delete_file(final_file.workdir)
    file_handler.cleanup()
except Exception:
    file_handler.cleanup()
    print(traceback.format_exc())
