from typing import Any, Tuple, Type

from modules.application.internal.worker_manager import WorkerManager
from modules.application.types import BaseWorker, Worker


class ApplicationService:
    @staticmethod
    def connect_temporal_server() -> None:
        result = WorkerManager.connect_temporal_server()
        return result

    @staticmethod
    def get_worker_by_id(*, worker_id: str) -> Worker:
        result = WorkerManager.get_worker_by_id(worker_id=worker_id)
        return result

    @staticmethod
    def run_worker_immediately(*, cls: Type[BaseWorker], arguments: Tuple[Any, ...] = ()) -> str:
        result = WorkerManager.run_worker_immediately(cls=cls, arguments=arguments)
        return result

    @staticmethod
    def schedule_worker_as_cron(*, cls: Type[BaseWorker], cron_schedule: str) -> str:
        result = WorkerManager.schedule_worker_as_cron(cls=cls, cron_schedule=cron_schedule)
        return result

    @staticmethod
    def cancel_worker(*, worker_id: str) -> None:
        result = WorkerManager.cancel_worker(worker_id=worker_id)
        return result

    @staticmethod
    def terminate_worker(*, worker_id: str) -> None:
        result = WorkerManager.terminate_worker(worker_id=worker_id)
        return result
