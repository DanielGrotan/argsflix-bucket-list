from pydantic import Field

from .detailed_visual_media import DetailedVisualMedia


class DetailedMovie(DetailedVisualMedia):
    dvd: str = Field(alias="DVD")
    box_office: str = Field(alias="BoxOffice")
    production: str = Field(alias="Production")
    website: str = Field(alias="Website")
