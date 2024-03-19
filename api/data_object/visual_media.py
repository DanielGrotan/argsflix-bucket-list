from pydantic import BaseModel, Field


class VisualMedia(BaseModel):
    title: str = Field(alias="Title")
    year: str = Field(alias="Year")
    imdb_id: str = Field(alias="imdbID")
    poster: str = Field(alias="Poster")
    type: str = Field(alias="Type")
