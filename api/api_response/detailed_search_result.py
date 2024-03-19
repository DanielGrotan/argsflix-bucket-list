from typing import Optional

from pydantic import BaseModel, Field, validator

from ..data_object import DetailedVisualMedia


class DetailedSearchResult(BaseModel):
    success: bool = Field(alias="Response")
    data: Optional[DetailedVisualMedia] = None
    error: Optional[str] = Field(alias="Error")

    @validator("data", always=True)
    def validate_data(cls, _, values):
        if values["success"]:
            return DetailedVisualMedia(**values)

        return None
