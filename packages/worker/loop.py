from io import BytesIO
import time
import os
import traceback
from typing import BinaryIO, List
from packages.backend.src.dataclasses.jobs_dataclasses import Job
from packages.file_handling.FileHandler import FileHandler
from packages.file_handling.dataclasses import FileInformation
from packages.worker.src.api import Api
from packages.worker.src.file_dataclasses import PackageFile
from packages.worker.src.file_utils import load_files, save_files
from packages.worker.src.fix_all import fix_files
from packages.worker.src.fixup.base_fixup import FixupOptions

api: Api = Api()
file_handler: FileHandler = FileHandler()


def check_backend_connection():
    return api.available()


print("Booting worker...")
if check_backend_connection():
    print("Connected to backend.")
    counter: int = 0
    while True:
        available_jobs: List[Job] = [
            job for job in api.get_jobs() if job.status == job.STATUS_WAITING]
        if available_jobs:
            job: Job = available_jobs[0]
            try:
                if api.set_job_in_progress(job.id):
                    print(f"Working on id {job.id}...")
                    options: FixupOptions = FixupOptions()
                    # save and extract the file
                    file: BytesIO = api.get_original_file(
                        job.id, job.file_name)
                    file_information: FileInformation = file_handler.save_file(
                        job.id, job.file_name, file)
                    files, result_folder = load_files(
                        file_information.path, file_information.workdir, options)
                    # run works on the ZIP
                    fix_files(files, options)
                    save_files(files)
                    final_file: FileInformation = file_handler.create_zip(
                        job.id, job.file_name, os.path.join(result_folder, files[0].zip_root))
                    file_handler.delete_file(file_information.workdir)
                    # send final file to api
                    api.post_final_file(job.id, final_file.path)
                    file_handler.delete_file(final_file.workdir)
            except Exception:
                api.set_job_failed(job.id)
                print(traceback.format_exc())
        time.sleep(2)
        counter += 1
