from typing import Any

from modules.task.comment_types import Comment
from modules.task.internal.store.comment_model import CommentModel


class CommentUtil:
    @staticmethod
    def convert_comment_bson_to_comment(comment_bson: dict[str, Any]) -> Comment:
        validated_comment_data = CommentModel.from_bson(comment_bson)
        return Comment(
            account_id=validated_comment_data.account_id,
            task_id=validated_comment_data.task_id,
            content=validated_comment_data.content,
            id=str(validated_comment_data.id),
        )
