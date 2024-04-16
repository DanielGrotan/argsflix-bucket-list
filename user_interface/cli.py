import functools
import re
from cmd import Cmd
from typing import Callable

from api.models import Media
from bucket_list import StoredMedia

from .user_interface import UserInterface

ARGUMENTS_REGEX = re.compile(r'(".+"|.*)')


def validate_arguments(*argument_types: type):
    def decorator(function: Callable):
        @functools.wraps(function)
        def wrapper(self, raw_arguments: str):
            parsed_arguments: list[str] = ARGUMENTS_REGEX.findall(raw_arguments)

            if len(parsed_arguments) < len(argument_types):
                print("Too few arguments")
                return

            type_casted_arguments = []

            for argument, argument_type in zip(parsed_arguments, argument_types):
                try:
                    type_casted_arguments.append(argument_type(argument))
                except ValueError:
                    print(f"Invalid input. Expected type {argument_type.__name__}")
                    return

            return function(self, *type_casted_arguments)

        return wrapper

    return decorator


class CLI(UserInterface, Cmd):
    intro = (
        "Welcome to the OMDB command line interface. Type help or ? to list commands.\n"
    )
    prompt = ">>> "

    def __init__(self, api, bucket_list) -> None:
        super().__init__(api, bucket_list)
        Cmd.__init__(self)

        self.previous_results: list[Media] = []

    def print_medias(self, medias: list[StoredMedia] | list[Media]) -> None:
        for i, media in enumerate(medias, 1):
            print(f"{i}. {media}")

    def postcmd(self, stop: bool, _) -> bool:
        print()
        return stop

    def run(self) -> None:
        self.cmdloop()

    def do_clear(self, _) -> None:
        """Clear the screen. Usage clear"""

        print("\033c", end="")

    @validate_arguments(str)
    def do_search(self, query: str) -> None:
        """List results for a given query. Usage search <query>"""

        print("Searching for " + query + "...")
        result = self.api.search(query)

        if result is None:
            print("Invalid query. Either too many or too few results.")

            self.previous_results = []
            return

        self.previous_results = result

        self.print_medias(result)

    @validate_arguments(int)
    def do_get_details(self, index: int) -> None:
        """Get details for search result at given index. Usage get_details <index>"""

        if index < 1 or index > len(self.previous_results):
            print("Invalid index.")
            return

        print(f"Getting details for {index}...")
        result = self.api.get_details(self.previous_results[index - 1].imdb_id)

        if result is None:
            print("No result found.")
            return

        print(result)

    @validate_arguments(int)
    def do_add(self, index: int) -> None:
        """Add a movie from the search results to the bucket list. Usage add <index>"""

        if index < 1 or index > len(self.previous_results):
            print("Invalid index.")
            return

        result = self.previous_results[index - 1]

        if any(media.imdb_id == result.imdb_id for media in self.bucket_list.view()):
            print("Media already in bucket list.")
            return

        self.bucket_list.add(result)
        print(f"Added {result.title} to bucket list.")

    def do_list(self, _) -> None:
        """List all movies in the bucket list. Usage list"""

        self.print_medias(self.bucket_list.view())

    @validate_arguments(int)
    def do_remove(self, index: int) -> None:
        """Remove a movie from the bucket list. Usage remove <index>"""

        bucket_list = self.bucket_list.view()

        if index < 1 or index > len(bucket_list):
            print("Invalid index.")
            return

        media = bucket_list[index - 1]

        self.bucket_list.remove(index - 1)
        print(f"Removed {media.title} from bucket list.")

    @validate_arguments(int)
    def do_mark_seen(self, index: int) -> None:
        """Mark a movie as seen in the bucket list. Usage mark_seen <index>"""

        bucket_list = self.bucket_list.view()

        if index < 1 or index > len(bucket_list):
            print("Invalid index.")
            return

        media = bucket_list[index - 1]

        self.bucket_list.mark_seen(index - 1)
        print(f"Marked {media.title} as seen.")

    @validate_arguments(int)
    def do_unmark_seen(self, index: int) -> None:
        """Mark a movie as unseen in the bucket list. Usage unmark_seen <index>"""

        bucket_list = self.bucket_list.view()

        if index < 1 or index > len(bucket_list):
            print("Invalid index.")
            return

        media = bucket_list[index - 1]

        self.bucket_list.mark_unseen(index - 1)
        print(f"Marked {media.title} as unseen.")

    @validate_arguments(str, str)
    def do_sort(self, field: str, order: str) -> None:
        """Sort the bucket list by field. Valid fields are 'title', 'year', 'imdb_id', 'type' and 'seen'. Usage sort <field> <order>"""

        if order not in ["asc", "desc"]:
            print("Invalid order. Must be either 'asc' or 'desc'.")
            return

        sorted_bucket_list = self.bucket_list.sort(field, order)

        self.print_medias(sorted_bucket_list)

    @validate_arguments(str, str)
    def do_filter(self, field: str, value: str) -> None:
        """Filter the bucket list by field and value. Valid fields are 'title', 'year', 'imdb_id', 'type' and 'seen'. Usage sort <field> <value>"""

        medias = self.bucket_list.filter(field, value)

        if not medias:
            print("No results...")
            return

        self.print_medias(medias)

    def do_save(self, _) -> None:
        """Save the bucket list to disk. Usage save"""

        self.bucket_list.save()
        print("Bucket list saved.")

    def do_quit(self, _) -> bool:
        """Quit the program. Usage quit"""

        return True
