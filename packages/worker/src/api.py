
from io import BytesIO
from typing import BinaryIO, Dict, List
from packages.backend.src.dataclasses.jobs_dataclasses import Job
import requests

class Api:
    def __init__(self):
        self.url: str = "http://backend:3001"
    
    def available(self) -> bool:
        return requests.get(self.url).status_code == 200

    def get_jobs(self) -> List[Job]:
        return [Job.from_dict(data) for data in requests.get(self.url + "/api/jobs/data").json()]

    def set_job_in_progress(self, job_id: int) -> bool:
        return requests.post(self.url + "/api/jobs/work/" + str(job_id)).json()["started"]
    
    def set_job_failed(self, job_id: int) -> None:
        requests.post(self.url + "/api/jobs/fail/" + str(job_id))

    def get_original_file(self, job_id: int, filename: str) -> BinaryIO:
        r = requests.get("http://www.example.com")
        return BytesIO(r.content)
