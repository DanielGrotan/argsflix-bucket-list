import json
import os
from typing import Literal


class BucketList:
    def __init__(self, file_path: str) -> None:
        self.file_path = file_path
        self.bucket_list = []

        if os.path.exists(file_path):
            self.load()

    def load(self) -> None:
        """Load the bucket list from disk."""

        with open(self.file_path, "r") as file:
            self.bucket_list = json.load(file)

    def add(self, item: dict) -> None:
        """Add an item to the bucket list."""

        self.bucket_list.append(item)

    def view(self) -> list[dict]:
        """Return a list of all items in the bucket list."""

        return self.bucket_list.copy()

    def remove(self, index: int) -> None:
        """Remove an item from the bucket list."""

        self.bucket_list.pop(index)

    def update(self, index: int, values: dict) -> None:
        """Update an item in the bucket list."""

        self.bucket_list[index].update(values)

    def sort_copy(self, field: str, order: Literal["asc", "desc"]) -> list[dict]:
        """Sort the bucket list by field."""

        return sorted(
            self.bucket_list, key=lambda x: x.get(field) or 0, reverse=order == "desc"
        )

    def save(self) -> None:
        """Save the bucket list to disk."""

        with open(self.file_path, "w") as file:
            json.dump(self.bucket_list, file, separators=(",", ":"))
