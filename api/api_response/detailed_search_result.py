from typing import Optional

from ..data_object import DetailedVisualMedia


class DetailedSearchResult:
    def __init__(self, api_response: dict) -> None:
        self.success = api_response.get("Response") == "True"

        if not self.success:
            self.data = None
            self.error = api_response.get("Error")

            assert self.error is not None, "Error message not found in response"
            return

        self.data = DetailedVisualMedia(**api_response)
        self.error = None

    def __str__(self) -> str:
        if self.success:
            return f"Success: {self.data}"
        else:
            return f"Error: {self.error}"

    def __repr__(self) -> str:
        return f"DetailedSearchResult(success={self.success}, data={self.data}, error={self.error})"
