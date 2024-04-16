import copy
import json
import os

from api.models import Media

from .stored_media import StoredMedia


class BucketList:
    def __init__(self, file_path: str) -> None:
        self.file_path = file_path
        self.bucket_list: list[StoredMedia] = []

        if os.path.exists(file_path):
            self.load()

    def load(self) -> None:
        """Load the bucket list from disk."""

        with open(self.file_path, "r") as file:
            self.bucket_list = list(
                map(lambda values: StoredMedia(**values), json.load(file))
            )

    def add(self, media: Media) -> None:
        """Add an item to the bucket list."""

        self.bucket_list.append(StoredMedia(**media.model_dump()))

    def view(self) -> list[StoredMedia]:
        """Return a list of all items in the bucket list."""

        return copy.deepcopy(self.bucket_list)

    def remove(self, index: int) -> None:
        """Remove an item from the bucket list."""

        self.bucket_list.pop(index)

    def mark_seen(self, index: int) -> None:
        self.bucket_list[index].seen = True

    def mark_unseen(self, index: int) -> None:
        self.bucket_list[index].seen = False

    def sort(self, field: str, order: str) -> list[StoredMedia]:
        """Sort the bucket list by field."""

        return sorted(
            self.bucket_list,
            key=lambda media: getattr(media, field, 0),
            reverse=order == "desc",
        )

    def filter(self, field: str, value: str) -> list[StoredMedia]:
        """Filter the bucket list by field and value"""

        return list(
            filter(
                lambda media: value.lower() in str(getattr(media, field, "")).lower(),
                self.bucket_list,
            )
        )

    def save(self) -> None:
        """Save the bucket list to disk."""

        with open(self.file_path, "w") as file:
            json.dump(
                list(map(StoredMedia.model_dump, self.bucket_list)),
                file,
                separators=(",", ":"),
            )
