import argparse
import sys

from database.books import Books
from cli import book_parser
from cli import goal_parser
from lib.goal_tracker import GoalTracker
from database.goals import Goals
from lib.shelf import Shelf
from lib.ibook import Format

PROGRAM_NAME = "Bookworm"
PROGRAM_DESCRIPTION = "Have a book reading goal and keep track of your " \
                      "progress"

COMMANDS = (
    'add_goal',
    'add_book',
    'update_goal',
    'update_book',
    'drop_book',
)


# TODO: Add argument for update book

def parse_command(args):
    parser = argparse.ArgumentParser(prog=PROGRAM_NAME,
                                     description=PROGRAM_DESCRIPTION)
    # If no goal is set, raise that error message
    if len(args) == 0:
        # No arguments passed
        # By default, recommendations should be shown
        pass
    # TODO: Create a proper help
    # TODO: Integrate with lower classes
    parser.add_argument("Command", choices=COMMANDS, type=str,
                        metavar="command", nargs=1, action='store')
    return parser.parse_args(args).Command[0]


def get_reading_recommendations():
    goals_db = Goals()
    books_db = Books()
    tracker = GoalTracker(goals_db.get_current_goal(),
                          Shelf(books_db.get_all_books()))
    print(f"\n{tracker.days_ahead_message()} on your goal to "
          f"{tracker.goal.message().lower()}.\n")
    for recommendation in tracker.minimum_page_recommendations():
        print(recommendation)
    print("")


def main(args):
    if len(args) == 1:
        # TODO: Print books available, or help.
        get_reading_recommendations()
        raise SystemExit
    command = parse_command([args[1]])
    if command == 'add_goal':
        goal_parser.parse(args[2:])
    elif command == 'add_book':
        book_parser.parse(args[2:])


if __name__ == "__main__":
    main(sys.argv)
