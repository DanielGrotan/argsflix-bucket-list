from pydantic import BaseModel, Field

from .rating import Rating


class DetailedVisualMedia(BaseModel):
    title: str = Field(alias="Title")
    year: str = Field(alias="Year")
    poster: str = Field(alias="Poster")
    type: str = Field(alias="Type")
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
