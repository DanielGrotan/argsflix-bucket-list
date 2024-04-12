from cmd import Cmd

from .user_interface import UserInterface


class CLI(UserInterface, Cmd):
    intro = (
        "Welcome to the OMDB command line interface. Type help or ? to list commands.\n"
    )
    prompt = ">>> "

    def __init__(self, api, bucket_list) -> None:
        super().__init__(api, bucket_list)
        Cmd.__init__(self)

        self.previous_results = []

    def print_bucket_list(self, bucket_list: list[dict]) -> None:
        for i, movie in enumerate(bucket_list, 1):
            print(f"{i}. {movie['title']} ({movie['imdb_id']}) - Seen: {movie['seen']}")

    def postcmd(self, stop: bool, _) -> bool:
        print()
        return stop

    def run(self) -> None:
        self.cmdloop()

    def do_clear(self, _) -> None:
        """Clear the screen. Usage clear"""

        print("\033c", end="")

    def do_search(self, arg: str) -> None:
        """List results for a given query. Usage search <query>"""

        print("Searching for " + arg + "...")
        result = self.api.search(arg)

        if result.success and result.search is not None:
            self.previous_results = result.search

            for i, media in enumerate(result.search, 1):
                print(f"{i}. {media.title} - {media.type} ({media.imdb_id})")

            return

        self.previous_results = []

        print(result.error)

    def do_get_details(self, arg: str) -> None:
        """Get details for search result at given index. Usage get_details <index>"""

        try:
            index = int(arg)
        except ValueError:
            print("Invalid input.")
            return

        if index < 1 or index > len(self.previous_results):
            print("Invalid index.")
            return

        print("Getting details for " + arg + "...")
        result = self.api.get_details(self.previous_results[index - 1].imdb_id)

        if result.success and result.data is not None:
            data = result.data

            for field in data.model_fields:
                print(f"{field.capitalize()}: {getattr(data, field)}")

            return

        print(result.error)

    def do_add(self, arg: str) -> None:
        """Add a movie from the search results to the bucket list. Usage add <index>"""

        try:
            index = int(arg)
        except ValueError:
            print("Invalid input.")
            return

        if index < 1 or index > len(self.previous_results):
            print("Invalid index.")
            return

        result = self.previous_results[index - 1]

        if any(movie["imdb_id"] == result.imdb_id for movie in self.bucket_list.view()):
            print("Movie already in bucket list.")
            return

        self.bucket_list.add(
            {"title": result.title, "imdb_id": result.imdb_id, "seen": False}
        )
        print(
            f"Added {result.title} ({result.year}) - {result.imdb_id} to bucket list."
        )

    def do_list(self, _) -> None:
        """List all movies in the bucket list. Usage list"""

        for i, movie in enumerate(self.bucket_list.view(), 1):
            print(f"{i}. {movie['title']} ({movie['imdb_id']}) - Seen: {movie['seen']}")

    def do_remove(self, arg: str) -> None:
        """Remove a movie from the bucket list. Usage remove <index>"""

        try:
            index = int(arg)
        except ValueError:
            print("Invalid input.")
            return

        bucket_list = self.bucket_list.view()

        if index < 1 or index > len(bucket_list):
            print("Invalid index.")
            return

        media = bucket_list[index - 1]

        self.bucket_list.remove(index - 1)
        print(f"Removed {media['title']} ({media['imdb_id']}) from bucket list.")

    def do_mark_seen(self, arg: str) -> None:
        """Mark a movie as seen in the bucket list. Usage mark_seen <index>"""

        try:
            index = int(arg)
        except ValueError:
            print("Invalid input.")
            return

        bucket_list = self.bucket_list.view()

        if index < 1 or index > len(bucket_list):
            print("Invalid index.")
            return

        media = bucket_list[index - 1]

        self.bucket_list.update(index - 1, {"seen": True})
        print(f"Marked {media['title']} ({media['imdb_id']}) as seen.")

    def do_unmark_seen(self, arg: str) -> None:
        """Mark a movie as unseen in the bucket list. Usage unmark_seen <index>"""

        try:
            index = int(arg)
        except ValueError:
            print("Invalid input.")
            return

        bucket_list = self.bucket_list.view()

        if index < 1 or index > len(bucket_list):
            print("Invalid index.")
            return

        media = bucket_list[index - 1]

        self.bucket_list.update(index - 1, {"seen": False})
        print(f"Marked {media['title']} ({media['imdb_id']}) as unseen.")

    def do_sort(self, arg: str) -> None:
        """Sort the bucket list by field. Valid fields are 'title', 'imdb_id', and 'seen'. Usage sort <field> <order>"""

        if arg == "":
            print("Invalid input.")
            return

        arguments = arg.split()

        if len(arguments) != 2:
            print("Invalid arguments. Use 'help sort' for more info.")
            return

        field, order = arguments

        if order not in ["asc", "desc"]:
            print("Invalid order. Must be either 'asc' or 'desc'.")
            return

        sorted_bucket_list = self.bucket_list.sort_copy(field, order)
        self.print_bucket_list(sorted_bucket_list)

    def do_filter(self, arg: str) -> None:
        """Filter the bucket list by field and value. Valid fields are 'title', 'imdb_id', and 'seen'. Usage sort <field> <value>"""

        if arg == "":
            print("Invalid input.")
            return

        arguments = arg.split()

        if len(arguments) != 2:
            print("Invalid arguments. Use 'help filter' for more info.")
            return

        field, value = arguments

        media = list(
            filter(
                lambda medium: value.lower() in str(medium.get(field)).lower(),
                self.bucket_list.view(),
            )
        )

        if not media:
            print("No results...")
            return

        self.print_bucket_list(media)

    def do_save(self, _) -> None:
        """Save the bucket list to disk. Usage save"""

        print("Saving bucket list...")
        self.bucket_list.save()
        print("Bucket list saved.")

    def do_quit(self, _) -> bool:
        """Quit the program. Usage quit"""

        return True
