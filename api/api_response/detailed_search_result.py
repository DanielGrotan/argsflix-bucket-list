from typing import Optional

from ..data_object import DetailedMovie, DetailedSeries, DetailedVisualMedia


class DetailedSearchResult:
    def __init__(self, api_response: dict) -> None:
        self.success = api_response.get("Response") == "True"

        if not self.success:
            self.data = None
            self.error = api_response.get("Error")

            assert self.error is not None, "Error message not found in response"
            return

        media_type = api_response.get("Type")

        if media_type == "movie":
            self.data = DetailedMovie(**api_response)
        elif media_type == "series":
            self.data = DetailedSeries(**api_response)
        else:
            self.data = DetailedVisualMedia(**api_response)

        self.error = None

    def __str__(self) -> str:
        if self.success:
            return f"Success: {self.data}"
        else:
            return f"Error: {self.error}"

    def __repr__(self) -> str:
        return f"DetailedSearchResult(success={self.success}, data={self.data}, error={self.error})"
