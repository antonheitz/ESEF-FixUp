from io import BytesIO
import time
import traceback
from typing import BinaryIO, List
from packages.backend.src.dataclasses.jobs_dataclasses import Job
from packages.file_handling.FileHandler import FileHandler
from packages.file_handling.dataclasses import FileInformation
from packages.worker.src.api import Api
from packages.worker.src.file_dataclasses import PackageFile
from packages.worker.src.file_utils import extract_zip, load_files

api: Api = Api()
file_handler: FileHandler = FileHandler()

def check_backend_connection():
    return api.available()

print("Booting worker...")
if check_backend_connection():
    print("Connected to backend.")
    counter: int = 0
    while True:
        available_jobs: List[Job] = [job for job in api.get_jobs() if job.status == job.STATUS_WAITING]
        if available_jobs:
            job: Job = available_jobs[0]
            try:
                if api.set_job_in_progress(job.id):
                    print(f"Working on id {job.id}...")
                    # save and extract the file
                    file: BinaryIO = api.get_original_file(job.id, job.file_name)
                    file_information: FileInformation = file_handler.save_file(job.id, job.file_name, file)
                    extract_path: str = extract_zip(file_information.path, file_information.workdir)
                    files: List[PackageFile] = load_files(extract_path)
                    for file in files:
                        print(file)
            except Exception:
                api.set_job_failed(job.id)
                print(traceback.format_exc())
        time.sleep(2)
        counter += 1