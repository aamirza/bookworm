import argparse
import sys
from enum import Enum

PROGRAM_NAME = "Bookworm"
PROGRAM_DESCRIPTION = "Have a book reading goal and keep track of your " \
                      "progress"

COMMANDS = (
    'add_goal',
    'add_book',
    'add_ibook',
    'add_audiobook',
    'update_goal',
    'update_book',
    'drop_book',
)


def goal_parser(args):
    parser = argparse.ArgumentParser(prog="Bookworm add_goal")
    parser.add_argument('number_of_books', action='store', nargs=1,
                        type=int,
                        help="Number of books you want to read.")
    return parser.parse_args(args)


# TODO: Add argument for add goal
# TODO: Add argument for add book
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


def main():
    command = parse_command(sys.argv[1:])
    if command == 'add_goal':
        pass
