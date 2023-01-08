from fastapi import APIRouter, UploadFile, File
from packages.backend.src.handlers.JobsHandler import JobsHandler

router = APIRouter()
handler: JobsHandler = JobsHandler()

@router.get("/data")
async def get_data():
    return [job.to_dict() for job in handler.get_jobs()]

@router.get("/data/{job_id}")
async def get_all_data(job_id: int):
    return handler.get_job(job_id).to_dict()

@router.post("/add")
async def add_job(file: UploadFile = File(...)):
    return handler.add_job(file.filename, file.file)

@router.post("/start/{job_id}")
async def start_job(job_id: int):
    handler.start_job(job_id)
    return 

@router.post("/work/{job_id}")
async def work_job(job_id: int):
    return { "started": handler.work_job(job_id) }
    
@router.post("/fail/{job_id}")
async def fail_job(job_id: int):
    handler.fail_job(job_id)
    return 
