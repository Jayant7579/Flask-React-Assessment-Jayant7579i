from dataclasses import asdict, dataclass
from typing import Any, Optional, Tuple

from pymongo.cursor import Cursor

from modules.application.common.types import PaginationParams, SortParams


@dataclass
class BaseModel:
    def to_bson(self) -> dict[str, Any]:
        # Turn the dataclass into a dict we can store in MongoDB
        data = asdict(self)
        mongo_data: dict[str, Any] = {}

        # Copy fields one by one (explicit is easier to follow)
        for key, value in data.items():
            mongo_data[key] = value

        # Mongo expects "_id" instead of "id"
        if "id" in mongo_data:
            if mongo_data["id"] is not None:
                mongo_data["_id"] = mongo_data["id"]
            # Always remove the "id" field
            mongo_data.pop("id", None)

        result = mongo_data
        return result

    @staticmethod
    def calculate_pagination_values(
        pagination_params: PaginationParams, total_count: int
    ) -> Tuple[PaginationParams, int, int]:
        page = pagination_params.page
        size = pagination_params.size
        offset = pagination_params.offset

        # Calculate how many records to skip
        skip = 0
        skip = (page - 1) * size + offset

        # Calculate total pages (avoid divide by zero)
        total_pages = 0
        if size > 0:
            total_pages = (total_count + size - 1) // size

        result = pagination_params, skip, total_pages
        return result

    @staticmethod
    def apply_sort_params(cursor: Cursor, sort_params: Optional[SortParams]) -> Cursor:
        if sort_params is None:
            result = cursor
            return result

        sort_by = sort_params.sort_by
        sort_dir = sort_params.sort_direction.numeric_value

        sort_list = []
        sort_list.append((sort_by, sort_dir))
        sort_list.append(("_id", sort_dir))

        result = cursor.sort(sort_list)
        return result
