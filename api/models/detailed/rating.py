from pydantic import BaseModel, Field


class Rating(BaseModel):
    source: str = Field(alias="Source")
    value: str = Field(alias="Value")

    def __repr__(self) -> str:
        return str(self)

    def __str__(self) -> str:
        return f"{self.source} {self.value}"
