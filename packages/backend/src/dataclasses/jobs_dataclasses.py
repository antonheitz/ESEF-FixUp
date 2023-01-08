from dataclasses import dataclass

@dataclass
class Job:
    id: int
    status: str
    file_name: str

    STATUS_ADDED: str = "ADDED"
    STATUS_WAITING: str = "WAITING"
    STATUS_IN_PROGRSS: str = "IN PROGRESS"
    STATUS_DONE: str = "DONE"
    STATUS_FAILED: str = "FAILED"

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "status": self.status,
            "file_name": self.file_name
        }

    @classmethod
    def from_dict(self, data: dict) -> 'Job':
        return Job(
            id=data.get("id"),
            status=data.get("status"),
            file_name=data.get("file_name")
        )