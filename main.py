from api import OmdbAPI
from bucket_list import BucketList
from user_interface import CLI


def main() -> None:
    api = OmdbAPI("fb117798")
    bucket_list = BucketList("bucket_list.json")
    cli = CLI(api, bucket_list)
    cli.run()


if __name__ == "__main__":
    main()
