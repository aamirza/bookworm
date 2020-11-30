import argparse
import datetime
import sys

from cli import goal_parser


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


def main(args):
    if len(args) == 0:
        # Print books available, or help.
        pass
    command = parse_command([args[1]])
    if command == 'add_goal':
        goal_parser.parse(args[2:])
    elif command == 'add_book':
        # TODO: Add argument for add book
        pass


if __name__ == "__main__":
    main(sys.argv)
