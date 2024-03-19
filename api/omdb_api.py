import requests

from .api_response import DetailedSearchResult, SearchResult


class OmdbAPI:
    def __init__(self, api_key: str) -> None:
        self.base_url = f"http://www.omdbapi.com/?apikey={api_key}&"

        self.search_cache = {}
        self.details_cache = {}

    def _create_url(self, query_params: dict[str, str]) -> str:
        mapped_params = map(lambda x: f"{x[0]}={x[1]}", query_params.items())
        return self.base_url + "&".join(mapped_params)

    def search(self, query: str):
        if query in self.search_cache:
            return self.search_cache[query]

        url = self._create_url({"s": query})
        response = requests.get(url).json()

    def get_details(self, imdb_id: str):
        if imdb_id in self.details_cache:
            return self.details_cache[imdb_id]

        url = self._create_url({"i": imdb_id})
        response = requests.get(url)
        response.json()
        # TODO: handle response
