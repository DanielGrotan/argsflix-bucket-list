from dataclasses import dataclass
from typing import Optional

from pydantic import BaseModel, Field, validator

from ..data_object import VisualMedia


class SearchResult(BaseModel):
    success: bool = Field(alias="Response")
    search: Optional[list[VisualMedia]] = Field(alias="Search", default=None)
    error: Optional[str] = Field(alias="Error", default=None)
