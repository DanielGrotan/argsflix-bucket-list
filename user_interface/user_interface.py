from abc import ABC, abstractmethod

from api import OmdbAPI
from bucket_list import BucketList


class UserInterface(ABC):
    def __init__(self, api: OmdbAPI, bucket_list: BucketList) -> None:
        self.api = api
        self.bucket_list = bucket_list

    @abstractmethod
    def run(self) -> None:
        pass
