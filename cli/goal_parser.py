"""
Child of parser.py

This is the command line arguments for adding, updating goals, and other things to do with goals.
"""

# TODO: Write comments

import argparse
import datetime

import database.goals as goals_db
from cli import validate


def add_goal(args):
    """Parser for adding goals"""
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
    add_goal_to_database(goal)


def add_goal_to_database(goal, db_name=""):
    """Add goal to database."""
    # TODO: Move to database package
    db = goals_db.Goals(db_name=db_name)
    if not db.active_goal_exists():
        db.add_goal(goal)
    else:
        # TODO: Make it so you can add multiple goals
        print("You already have an active goal.")


def update_goal(args):
    """Parser for updating goals"""
    db = goals_db.Goals()
    active_goal = db.get_current_goal()

    parser = argparse.ArgumentParser(prog="Bookworm update_goal")
    parser.add_argument("-n", "-num_of_books", dest="num_books",
                        type=validate.goal_number,
                        default=active_goal.num_books,
                        help="Number of books you want to read")
    parser.add_argument("-ed", "-end_date", dest="end_date",
                        type=validate.get_future_date,
                        default=active_goal.end_date,
                        help="By what date you want to complete this goal.")

    if len(args) == 0:
        # Show help if no arguments passed
        args.append('-h')
    goal = parser.parse_args(args)

    new_goal = validate.goal(goal.num_books, active_goal.start_date,
                             goal.end_date)
    if new_goal.num_books != active_goal.num_books:
        db.update_active_goal_num_books(new_goal.num_books)
    if new_goal.end_date != active_goal.end_date:
        db.update_active_goal_end_date(new_goal.end_date)
