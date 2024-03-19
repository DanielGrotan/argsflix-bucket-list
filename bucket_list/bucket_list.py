import json
import os


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

    def remove(self, item: dict) -> None:
        """Remove an item from the bucket list."""

        self.bucket_list.remove(item)

    def save(self) -> None:
        """Save the bucket list to disk."""

        with open(self.file_path, "w") as file:
            json.dump(self.bucket_list, file)
