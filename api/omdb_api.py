import copy

import requests

from .models import Media
from .models.detailed import DetailedGame, DetailedMedia, DetailedMovie, DetailedSeries

SearchResult = list[Media] | None
DetailedSearchResult = DetailedMedia | None


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
            return copy.deepcopy(self.search_cache[query])

        url = self._create_url({"s": query})
        response = requests.get(url)

        data = response.json()

        if data.get("Response") != "True":
            self.search_cache[query] = None
            return None

        medias = list(map(lambda values: Media(**values), data.get("Search") or []))
        self.search_cache[query] = medias

        return copy.deepcopy(medias)

    def get_details(self, imdb_id: str) -> DetailedSearchResult:
        if imdb_id in self.details_cache:
            return copy.deepcopy(self.details_cache[imdb_id])

        url = self._create_url({"i": imdb_id})
        response = requests.get(url)

        data = response.json()

        if data.get("Response") != "True":
            self.details_cache[imdb_id] = None
            return None

        match data.get("Type"):
            case "movie":
                detailed_media = DetailedMovie(**data)
            case "series":
                detailed_media = DetailedSeries(**data)
            case "game":
                detailed_media = DetailedGame(**data)
            case _:
                detailed_media = None

        self.details_cache[imdb_id] = detailed_media

        return copy.deepcopy(detailed_media)
