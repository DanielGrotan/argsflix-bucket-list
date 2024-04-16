import os

from api.models import Media
from bucket_list import BucketList
from utils import get_absolute_path

bucket_list = BucketList(get_absolute_path("temp_bucket_list.json"))


def test_initial_bucket_list_empty():
    assert len(bucket_list.view()) == 0, "Expected empty bucket list"


def test_add_media():
    bucket_list.add(
        Media(
            **{
                "Title": "Test Movie",
                "Year": "1984",
                "imdbID": "ttsghasg171782",
                "Poster": "https://www.hihihaha.com",
                "Type": "movie",
            }
        )
    )
    assert len(bucket_list.view()) == 1, "Expected 1 element in bucket list after add"


def test_remove():
    bucket_list.remove(0)
    assert (
        len(bucket_list.view()) == 0
    ), "Expected 0 element in bucket list after remove"


def test_mark_seen():
    bucket_list.add(
        Media(
            **{
                "Title": "Test Movie",
                "Year": "1984",
                "imdbID": "ttsghasg171782",
                "Poster": "https://www.hihihaha.com",
                "Type": "movie",
            }
        )
    )
    bucket_list.mark_seen(0)

    assert (
        bucket_list.view()[0].seen == True
    ), "Expected first element to be seen after 'mark_seen'"


def test_mark_unseen():
    bucket_list.mark_unseen(0)

    assert (
        bucket_list.view()[0].seen == False
    ), "Expected first element to be unseen after 'mark_unseen'"


def test_sort():
    bucket_list.add(
        Media(
            **{
                "Title": "Test Movie",
                "Year": "2024",
                "imdbID": "ttsghasg171782",
                "Poster": "https://www.hihihaha.com",
                "Type": "movie",
            }
        )
    )

    sorted_medias = bucket_list.sort("year", "desc")

    assert (
        sorted_medias[0].year == 2024
    ), "Expected movie with 'year' = '2024' to be first after sort"


def test_filter():
    bucket_list.mark_seen(1)

    filtered_medias = bucket_list.filter("seen", "True")

    assert len(filtered_medias) == 1, "Expected 1 movie with 'seen' = True"


def test_save():
    bucket_list.save()

    new_bucket_list = BucketList("temp_bucket_list.json")

    assert (
        len(new_bucket_list.view()) > 0
    ), "Expected items to be in the saved bucket list"

    os.remove("temp_bucket_list.json")
