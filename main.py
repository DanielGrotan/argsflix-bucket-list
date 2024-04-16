import os

from api import OmdbAPI
from bucket_list import BucketList
from user_interface import CLI
from utils import get_absolute_path


def main() -> None:
    api = OmdbAPI("fb117798")
    bucket_list = BucketList(get_absolute_path("bucket_list.json"))
    cli = CLI(api, bucket_list)
    cli.run()


if __name__ == "__main__":
    main()
