import argparse
import datetime
import sys

from cli import validate
import database.goals as goals_db


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
    # TODO: Add argument for add goal
    today = datetime.datetime.today().date()
    year_from_now = datetime.datetime(today.year + 1, today.month, today.day)

    parser = argparse.ArgumentParser(prog="Bookworm add_goal")
    parser.add_argument('number_of_books', type=validate.goal_number,
                        help="Number of books you want to read.")
    parser.add_argument("end_date", default=year_from_now,
                        type=validate.get_future_date,
                        help="When you want this goal to end. Default: Year "
                             "from now.")
    parser.add_argument("-sd", "--sd", "-start_date", type=validate.get_date,
                        metavar="start_date", default=today,
                        dest="start_date",
                        help="The day you started this goal. Default: Today")
    goal = parser.parse_args(args)
    goal = validate.goal(goal.number_of_books, goal.start_date, goal.end_date)
    return goal


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


def main(args):
    command = parse_command([args[1]])
    if command == 'add_goal':
        db = goals_db.Goals()
        goal = goal_parser(args[2:])
        db.add_goal(goal)


if __name__ == "__main__":
    main(sys.argv)
