import argparse
import sys

PROGRAM_NAME = "Bookworm"
PROGRAM_DESCRIPTION = "Have a book reading goal and keep track of your " \
                      "progress"

COMMANDS = ['add_goal', '-ag',
            'add_book', '-ab',
            'add_ibook', '-aib',
            'add_audiobook', 'add_ab', '-aab',
            'update_goal', '-ug',
            'update_book', '-ub',
            'drop_book', '-db',
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


def parse_args(args):
    parser = argparse.ArgumentParser(prog=PROGRAM_NAME,
                                     description=PROGRAM_DESCRIPTION)
    # If no goal is set, raise that error message
    if len(args) == 0:
        # No arguments passed
        # By default, recommendations should be shown
        pass
    parser.add_argument("command", choices=COMMANDS,
                        metavar="command")
    # TODO: Add argument for add goal
    # TODO: Add argument for add book
    # TODO: Add argument for update book
    return parser.parse_args(args)


def main():
    parse_args(sys.argv[1:])
