from io import BytesIO
from typing import BinaryIO, List
from packages.backend.src.database.Database import Database
from packages.backend.src.dataclasses.jobs_dataclasses import Job
from packages.file_handling.FileHandler import FileHandler
from packages.file_handling.dataclasses import FileInformation


class JobsHandler:
    def __init__(self):
        self.database: Database = Database()
        self.file_handler: FileHandler = FileHandler()

    def add_job(self, filename: str, file: BinaryIO) -> int:
        file_id = self.database.add_job()
        file_information: FileInformation = self.file_handler.save_file(file_id, filename, BytesIO(file.read()))
        self.database.add_file_name(file_id, filename)
        return file_id

    def start_job(self, job_id: int) -> None:
        self.database.set_job_status(job_id, Job.STATUS_WAITING)

    def work_job(self, job_id: int) -> bool:
        jobs: List[Job] = [job for job in self.get_jobs() if job.id == job_id]
        if jobs and jobs[0].status == Job.STATUS_WAITING:
            self.database.set_job_status(job_id, Job.STATUS_IN_PROGRSS)
            return True
        else:
            return False

    def get_job(self, job_id: int) -> Job:
        return self.database.get_job(job_id)
    
    def get_jobs(self) -> List[Job]:
        return self.database.get_all_jobs()

    def finish_job(self, job_id) -> None:
        self.database.set_job_status(job_id, Job.STATUS_DONE)

    def fail_job(self, job_id) -> None:
        self.database.set_job_status(job_id, Job.STATUS_FAILED)