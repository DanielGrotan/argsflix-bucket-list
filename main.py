import requests

from api.api_response import DetailedSearchResult

res = requests.get("https://omdbapi.com/?apikey=fb117798&i=tt3428912").json()
print(DetailedSearchResult(**res))
