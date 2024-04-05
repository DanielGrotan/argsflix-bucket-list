import copy
import io

import requests
from PIL import Image

from .api_response import DetailedSearchResult, SearchResult


class OmdbAPI:
    def __init__(self, api_key: str) -> None:
        self.base_url = f"http://www.omdbapi.com/?apikey={api_key}&"

        self.search_cache: dict[str, SearchResult] = {}
        self.details_cache: dict[str, DetailedSearchResult] = {}

    def _create_url(self, query_params: dict[str, str]) -> str:
        mapped_params = map(lambda x: f"{x[0]}={x[1]}", query_params.items())
        return self.base_url + "&".join(mapped_params)

    def search(self, query: str) -> SearchResult:
        if query in self.search_cache:
            return self.search_cache[query].model_copy()

        url = self._create_url({"s": query})
        response = requests.get(url)

        search_result = SearchResult(**response.json())
        self.search_cache[query] = search_result.model_copy()

        return search_result

    def get_details(self, imdb_id: str) -> DetailedSearchResult:
        if imdb_id in self.details_cache:
            return copy.deepcopy(self.details_cache[imdb_id])

        url = self._create_url({"i": imdb_id})
        response = requests.get(url)

        details = DetailedSearchResult(response.json())

        self.details_cache[imdb_id] = copy.deepcopy(details)

        return details
