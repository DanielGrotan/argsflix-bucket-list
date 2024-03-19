from pydantic import Field

from .detailed_visual_media import DetailedVisualMedia


class DetailedSeries(DetailedVisualMedia):
    total_seasons: str = Field(alias="totalSeasons")
