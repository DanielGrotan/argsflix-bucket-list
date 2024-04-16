from pydantic import BaseModel, Field


class Media(BaseModel):
    title: str = Field(alias="Title")
    year: str = Field(alias="Year")
    imdb_id: str = Field(alias="imdbID")
    poster: str = Field(alias="Poster")
    type: str = Field(alias="Type")

    def __str__(self) -> str:
        return f"{self.type.title()}: {self.title} ({self.year}) - {self.imdb_id}"
