import threading
import typing

from common.py.data.entities.project import (
    ProjectJob,
    ProjectJobID,
    ProjectID,
)
from common.py.data.entities.user import UserID
from common.py.data.storage import ProjectJobStorage


class MemoryProjectJobStorage(ProjectJobStorage):
    """
    In-memory storage for project jobs.
    """

    _project_jobs: typing.Dict[ProjectJobID, ProjectJob] = {}
    _lock = threading.RLock()

    def next_id(self) -> ProjectJobID:
        raise NotImplementedError("Project jobs do not support automatic IDs")

    def add(self, entity: ProjectJob) -> None:
        with MemoryProjectJobStorage._lock:
            MemoryProjectJobStorage._project_jobs[self._key_from_entity(entity)] = (
                entity
            )

    def remove(self, entity: ProjectJob) -> None:
        with MemoryProjectJobStorage._lock:
            try:
                del MemoryProjectJobStorage._project_jobs[self._key_from_entity(entity)]
            except Exception as exc:  # pylint: disable=broad-exception-caught
                from common.py.data.storage import StorageException

                raise StorageException(
                    f"A project job with ID {self._key_from_entity(entity)} was not found"
                ) from exc

    def get(self, key: ProjectJobID) -> ProjectJob | None:
        with MemoryProjectJobStorage._lock:
            return (
                MemoryProjectJobStorage._project_jobs[key]
                if key in MemoryProjectJobStorage._project_jobs
                else None
            )

    def list(self) -> typing.List[ProjectJob]:
        with MemoryProjectJobStorage._lock:
            return list(MemoryProjectJobStorage._project_jobs.values())

    def filter_by_user(self, user_id: UserID) -> typing.List[ProjectJob]:
        with MemoryProjectJobStorage._lock:
            return list(
                filter(
                    lambda job: job.user_id == user_id,
                    MemoryProjectJobStorage._project_jobs.values(),
                )
            )

    def filter_by_project(self, project_id: ProjectID) -> typing.List[ProjectJob]:
        with MemoryProjectJobStorage._lock:
            return list(
                filter(
                    lambda job: job.project_id == project_id,
                    MemoryProjectJobStorage._project_jobs.values(),
                )
            )

    def _key_from_entity(self, entity: ProjectJob) -> ProjectJobID:
        return entity.project_id, entity.connector_instance
