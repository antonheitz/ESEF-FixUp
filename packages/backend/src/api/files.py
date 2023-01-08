from io import BytesIO
from fastapi import APIRouter, UploadFile, File
from fastapi.responses import FileResponse
from packages.file_handling.FileHandler import FileHandler, TMP_STORAGE_PATH
from packages.backend.src.database.Database import Database
from packages.backend.src.dataclasses.jobs_dataclasses import Job
import os

router = APIRouter()
file_handler: FileHandler = FileHandler()
database: Database = Database()

@router.get("/original/{id}/{file_name}")
async def get_file(id: int, file_name: str):
    return FileResponse(path=os.path.join(TMP_STORAGE_PATH, str(id), file_name), media_type='application/octet-stream', filename=file_name)

@router.post("/final/{id}")
async def get_file(id: int, file: UploadFile = File()):
    file_handler.save_file(file_handler.final_folder(id), file.filename, BytesIO(file.file.read()))
    database.set_job_status(id, Job.STATUS_DONE)
    return

@router.get("/final/{id}/{file_name}")
async def get_file(id: int, file_name: str):
    return FileResponse(path=os.path.join(TMP_STORAGE_PATH, file_handler.final_folder(id), file_name), media_type='application/octet-stream', filename=file_name)
