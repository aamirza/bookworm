import argparse
import datetime

import database.goals as goals_db
from cli import validate


def parse(args):
    today = datetime.datetime.today().date()
    year_from_now = datetime.datetime(today.year + 1, today.month,
                                      today.day).date()

    parser = argparse.ArgumentParser(prog="Bookworm add_goal")
    parser.add_argument('number_of_books', type=validate.goal_number,
                        help="Number of books you want to read.")
    parser.add_argument("end_date", default=year_from_now, nargs="?",
                        type=validate.get_future_date,
                        help="When you want this goal to end. Default: Year "
                             "from now.")
    parser.add_argument("-sd", "--sd", "-start_date", type=validate.get_date,
                        metavar="start_date", default=today,
                        dest="start_date",
                        help="The day you started this goal. Default: Today")
    goal = parser.parse_args(args)
    goal = validate.goal(goal.number_of_books, goal.start_date, goal.end_date)
    add_goal(goal)


def add_goal(goal):
    db = goals_db.Goals()
    if not db.active_goal_exists():
        db.add_goal(goal)
    else:
        # TODO: Make it so you can add multiple goals
        print("You already have an active goal.")
