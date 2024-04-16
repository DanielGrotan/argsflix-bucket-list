from pydantic import Field

from ..media import Media
from .rating import Rating


class DetailedMedia(Media):
    rated: str = Field(alias="Rated")
    released: str = Field(alias="Released")
    runtime: str = Field(alias="Runtime")
    genre: str = Field(alias="Genre")
    director: str = Field(alias="Director")
    writer: str = Field(alias="Writer")
    actors: str = Field(alias="Actors")
    plot: str = Field(alias="Plot")
    language: str = Field(alias="Language")
    country: str = Field(alias="Country")
    awards: str = Field(alias="Awards")
    ratings: list[Rating] = Field(alias="Ratings")
    metascore: str = Field(alias="Metascore")
    imdb_rating: str = Field(alias="imdbRating")
    imdb_votes: str = Field(alias="imdbVotes")

    def __str__(self) -> str:
        return "\n".join(
            f"{field.capitalize()}: {getattr(self, field)}"
            for field in self.model_fields
        )
