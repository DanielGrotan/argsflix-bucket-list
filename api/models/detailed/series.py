from pydantic import Field

from .media import DetailedMedia


class DetailedSeries(DetailedMedia):
    total_seasons: str = Field(alias="totalSeasons")
