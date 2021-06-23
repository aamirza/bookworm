# TODO: Write comments

import argparse
import sys

from cli import prompt
from cli import recommendation
from cli import book_parser
from cli import goal_parser
from database.goals import NoGoalCreatedError

PROGRAM_NAME = "Bookworm"
PROGRAM_DESCRIPTION = "Have a book reading goal and keep track of your " \
                      "progress"

COMMANDS = (
    'add_goal', 'ag',
    'add_book', 'ab',
    'update_goal', 'ug',
    'update_book', 'ub', 'up',
    'drop_book', 'db',
    'next_day', 'nd',
    'all'
)


def parse_command(args):
    parser = argparse.ArgumentParser(prog=PROGRAM_NAME,
                                     description=PROGRAM_DESCRIPTION)

    # TODO: Add help for tomorrow's recommendations
    parser.add_argument("Command", choices=COMMANDS, type=str,
                        metavar="command", nargs=1, action='store',
                        help="Choose from one of the following: add_goal (ag),"
                             " add_book (ab), update_goal (ug), update_book "
                             "(ub or up), or drop_book (db), or "
                             "next_day (nd), or 'all'.")
    return parser.parse_args(args).Command[0]


def main(args):
    next_day_recommendations = False
    show_all_books = False
    if len(args) > 1:
        try:
            command = parse_command([args[1]])
            if command in ('add_goal', 'ag'):
                goal_parser.add_goal(args[2:])
            elif command in ('add_book', 'ab'):
                book_parser.add_book(args[2:])
            elif command in ('update_book', 'ub', 'up'):
                book_parser.update_book(args[2:])
            elif command in ('update_goal', 'ug'):
                goal_parser.update_goal(args[2:])
            elif command in ('next_day', 'nd'):
                next_day_recommendations = True
            elif command in ('all',):
                show_all_books = True
        except argparse.ArgumentTypeError as err:
            print(f"Error: {err}")
            raise SystemExit

    try:
        recommendation.print_books(next_day_recommendations, show_all_books)
    except NoGoalCreatedError:
        try:
            prompt.add_goal()
            recommendation.print_books()
        except argparse.ArgumentTypeError:
            raise SystemExit


if __name__ == "__main__":
    main(sys.argv)
