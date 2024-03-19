from pydantic import BaseModel


class Rating(BaseModel):
    source: str
    value: str
