import argparse
import sys
from enum import Enum

PROGRAM_NAME = "Bookworm"
PROGRAM_DESCRIPTION = "Have a book reading goal and keep track of your " \
                      "progress"

COMMANDS = [
    'add_goal',
    'add_book',
    'add_ibook',
    'add_audiobook',
    'update_goal',
    'update_book',
    'drop_book',
]


def goal_parser(parser):
    return parser.add_argument('-ag', '--ag', '-add_goal',
                               action='store',
                               nargs='+',
                               help="Number of books you want to read, and by "
                                    "what date you want to accomplish this "
                                    "goal.",
                               metavar=("NUM_OF_BOOKS", "end_date"),
                               dest="Goal")


# TODO: Add argument for add goal
# TODO: Add argument for add book
# TODO: Add argument for update book

def parse_args(args):
    parser = argparse.ArgumentParser(prog=PROGRAM_NAME,
                                     description=PROGRAM_DESCRIPTION)
    # If no goal is set, raise that error message
    if len(args) == 0:
        # No arguments passed
        # By default, recommendations should be shown
        pass
    # TODO: Create a proper help
    parser.add_argument("command", choices=COMMANDS, metavar="command")
    return parser.parse_args(args)


def main():
    parse_args(sys.argv[1:])
