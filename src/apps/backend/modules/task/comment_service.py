from modules.application.common.types import PaginationResult
from modules.task.comment_types import (
    Comment,
    CommentDeletionResult,
    CreateCommentParams,
    DeleteCommentParams,
    GetCommentParams,
    GetPaginatedCommentsParams,
    UpdateCommentParams,
)
from modules.task.internal.comment_reader import CommentReader
from modules.task.internal.comment_writer import CommentWriter
from modules.task.internal.task_reader import TaskReader
from modules.task.types import GetTaskParams


class CommentService:
    @staticmethod
    def create_comment(*, params: CreateCommentParams) -> Comment:
        TaskReader.get_task(params=GetTaskParams(account_id=params.account_id, task_id=params.task_id))
        result = CommentWriter.create_comment(params=params)
        return result

    @staticmethod
    def get_comment(*, params: GetCommentParams) -> Comment:
        TaskReader.get_task(params=GetTaskParams(account_id=params.account_id, task_id=params.task_id))
        result = CommentReader.get_comment(params=params)
        return result

    @staticmethod
    def get_paginated_comments(*, params: GetPaginatedCommentsParams) -> PaginationResult[Comment]:
        TaskReader.get_task(params=GetTaskParams(account_id=params.account_id, task_id=params.task_id))
        result = CommentReader.get_paginated_comments(params=params)
        return result

    @staticmethod
    def update_comment(*, params: UpdateCommentParams) -> Comment:
        TaskReader.get_task(params=GetTaskParams(account_id=params.account_id, task_id=params.task_id))
        result = CommentWriter.update_comment(params=params)
        return result

    @staticmethod
    def delete_comment(*, params: DeleteCommentParams) -> CommentDeletionResult:
        TaskReader.get_task(params=GetTaskParams(account_id=params.account_id, task_id=params.task_id))
        result = CommentWriter.delete_comment(params=params)
        return result
