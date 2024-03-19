from cmd import Cmd
from typing import override

from .user_interface import UserInterface


class CLI(UserInterface, Cmd):
    intro = (
        "Welcome to the OMDB command line interface. Type help or ? to list commands.\n"
    )

    def __init__(self, api, bucket_list) -> None:
        super().__init__(api, bucket_list)
        Cmd.__init__(self)

    @override
    def run(self) -> None:
        self.cmdloop()

    def do_search(self, arg: str) -> None:
        """List results for a given query."""

        print("Searching for " + arg + "...")
        result = self.api.search(arg)

        if result.success and result.search is not None:
            print("Search results:")

            for media in result.search:
                print(f"{media.title} ({media.year}) - {media.imdb_id}")

            return

        print(result.error)

    def do_get_details(self, arg: str) -> None:
        """Get details for a given IMDB ID."""

        print("Getting details for " + arg + "...")
        result = self.api.get_details(arg)

        if result.success and result.data is not None:
            data = result.data

            for field in data.model_fields:
                print(f"{field.capitalize()}: {getattr(data, field)}")

            return

        print(result.error)

    def do_add(self, arg) -> None:
        """Add a movie to the bucket list"""

        print("Adding " + arg + "...")

        # check if id is valid
        result = self.api.get_details(arg)
        if not result.success or result.data is None:
            print("Invalid IMDB ID.")
            return

        if any(movie["imdb_id"] == arg for movie in self.bucket_list.view()):
            print("Movie already in bucket list.")
            return

        self.bucket_list.add(
            {"title": result.data.title, "imdb_id": arg, "seen": False}
        )
        print("Added to bucket list.")

    def do_list(self, arg) -> None:
        """List all movies in the bucket list"""

        print("Listing all movies...")
        for movie in self.bucket_list.view():
            print(f"{movie['title']} ({movie['imdb_id']}) - Seen: {movie['seen']}")

    def do_remove(self, arg) -> None:
        """Remove a movie from the bucket list"""

        print("Removing " + arg + "...")

        for movie in self.bucket_list.view():
            if movie["imdb_id"] == arg:
                self.bucket_list.remove(movie)
                print("Removed from bucket list.")
                return

        print("Movie not found in bucket list.")

    def do_save(self, arg) -> None:
        """Save the bucket list to disk."""

        print("Saving bucket list...")
        self.bucket_list.save()
        print("Bucket list saved.")

    def do_quit(self, arg) -> bool:
        """Quit the program."""

        print("Quitting...")
        return True
