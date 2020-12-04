import argparse
import sys

from cli import recommendation
from cli import book_parser
from cli import goal_parser

PROGRAM_NAME = "Bookworm"
PROGRAM_DESCRIPTION = "Have a book reading goal and keep track of your " \
                      "progress"

COMMANDS = (
    'add_goal', '-ag'
                'add_book', '-ab'
                            'update_goal', '-ug'
                                           'update_book', '-ub'
                                                          'drop_book', 'db'
)


def parse_command(args):
    parser = argparse.ArgumentParser(prog=PROGRAM_NAME,
                                     description=PROGRAM_DESCRIPTION)
    # If no goal is set, raise that error message
    if len(args) == 0:
        # No arguments passed
        # By default, recommendations should be shown
        pass
    # TODO: Integrate with lower classes
    parser.add_argument("Command", choices=COMMANDS, type=str,
                        metavar="command", nargs=1, action='store',
                        help="Choose one of the following: add_goal (-ag), "
                             "add_book "
                             "(-ab), update_goal (-ug), update_book (-ub), "
                             "or drop_book (-db).")
    return parser.parse_args(args).Command[0]


def main(args):
    if len(args) > 1:
        command = parse_command([args[1]])
        if command in ('add_goal', '-ag'):
            goal_parser.parse(args[2:])
        elif command in ('add_book', '-ab'):
            book_parser.parse(args[2:])
        elif command in ('update_book', '-ub'):
            # TODO: Command for update book
            pass
    recommendation.print_books()


if __name__ == "__main__":
    main(sys.argv)
