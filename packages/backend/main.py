from typing import Union
from fastapi import FastAPI
from packages.backend.src.api import jobs, files

app: FastAPI = FastAPI()

# import sub-apis
app.include_router(
    jobs.router,
    prefix="/api/jobs",
    tags=["jobs"],
    responses={404: {"description": "Not found"}}
)
app.include_router(
    files.router,
    prefix="/api/files",
    tags=["files"],
    responses={404: {"description": "Not found"}}
)

# health check
@app.get("/")
async def root():
    return "ESEF Fixup: backend up and running!"
