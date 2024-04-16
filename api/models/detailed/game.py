from pydantic import Field

from .media import DetailedMedia


class DetailedGame(DetailedMedia):
    dvd: str = Field(alias="DVD")
    box_office: str = Field(alias="BoxOffice")
    production: str = Field(alias="Production")
    website: str = Field(alias="Website")
