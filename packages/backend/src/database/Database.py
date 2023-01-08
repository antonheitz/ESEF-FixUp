import sqlite3
import os
from typing import List, Tuple
from packages.backend.src.dataclasses.jobs_dataclasses import Job

DATABASE_FOLDER: str = os.path.dirname(os.path.realpath(__file__))
DATABASE_FILE: str = os.path.join(DATABASE_FOLDER, "database.db")


class Database:
    def __init__(self):
        db: sqlite3.Connection = sqlite3.connect(DATABASE_FILE)
        cursor: sqlite3.Cursor = db.cursor()
        # check if any table is already known
        if not cursor.execute("SELECT name FROM sqlite_master").fetchone():
            # get script
            with open(os.path.join(DATABASE_FOLDER, "init.sql"), "r") as f:
                sql_script: str = f.read()
            # insert table
            cursor.executescript(sql_script)

    def _get_connection(self) -> Tuple[sqlite3.Connection, sqlite3.Cursor]:
        db_conn = sqlite3.connect(DATABASE_FILE)
        cursor = db_conn.cursor()
        return db_conn, cursor

    def add_job(self) -> int:
        con, cursor = self._get_connection()
        cursor.execute(
            f"INSERT INTO jobs VALUES (null, 'INIT', 'INIT')")
        con.commit()
        return cursor.lastrowid

    def add_file_name(self, job_id: int, file_name: str) -> None:
        con, cursor = self._get_connection()
        cursor.execute(
            f"UPDATE jobs SET file_name = '{file_name}', job_status = '{Job.STATUS_ADDED}' WHERE id = {job_id}"
        )
        con.commit()

    def set_job_status(self, job_id: int, job_status: str) -> None:
        con, cursor = self._get_connection()
        cursor.execute(
            f"UPDATE jobs SET job_status = '{job_status}' WHERE id = {job_id}"
        )
        con.commit()

    def get_job(self, job_id: int) -> Job:
        con, cursor = self._get_connection()
        for raw_job in cursor.execute(f"SELECT * FROM jobs WHERE id = {job_id}"):
            if raw_job[0] == job_id:
                return Job(id=raw_job[0], status=raw_job[1], file_name=raw_job[2])
        return Job(id=0, status="NOT FOUND")

    def get_all_jobs(self) -> List[Job]:
        jobs: List[Job] = []
        con, cursor = self._get_connection()
        for raw_job in cursor.execute(f"SELECT * FROM jobs"):
            jobs.append(Job(id=raw_job[0], status=raw_job[1], file_name=raw_job[2]))
        return jobs
