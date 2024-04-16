from pydantic import BaseModel, Field


class StoredMedia(BaseModel):
    title: str
    year: int
    imdb_id: str
    poster: str
    type: str
    seen: bool = Field(default=False)

    def __str__(self) -> str:
        return f"{self.type.title()}: {self.title} ({self.year}) - {self.imdb_id}. Seen: {self.seen}"
