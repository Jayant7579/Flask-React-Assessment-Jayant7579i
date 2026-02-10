from modules.application.common.types import PaginationResult
from modules.task.internal.task_reader import TaskReader
from modules.task.internal.task_writer import TaskWriter
from modules.task.types import (
    CreateTaskParams,
    DeleteTaskParams,
    GetPaginatedTasksParams,
    GetTaskParams,
    Task,
    TaskDeletionResult,
    UpdateTaskParams,
)


class TaskService:
    @staticmethod
    def create_task(*, params: CreateTaskParams) -> Task:
        result = TaskWriter.create_task(params=params)
        return result

    @staticmethod
    def get_task(*, params: GetTaskParams) -> Task:
        result = TaskReader.get_task(params=params)
        return result

    @staticmethod
    def get_paginated_tasks(*, params: GetPaginatedTasksParams) -> PaginationResult[Task]:
        result = TaskReader.get_paginated_tasks(params=params)
        return result

    @staticmethod
    def update_task(*, params: UpdateTaskParams) -> Task:
        result = TaskWriter.update_task(params=params)
        return result

    @staticmethod
    def delete_task(*, params: DeleteTaskParams) -> TaskDeletionResult:
        result = TaskWriter.delete_task(params=params)
        return result
