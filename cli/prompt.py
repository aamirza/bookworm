# TODO: Write comments

"""
This is for the walkthrough prompt of adding a goal.
"""
import argparse
import datetime

from cli.goal_parser import add_goal_to_database
from cli import validate


def input_with_arrows(question, newline=False):
    """Show an input prompt that ends with three arrows and a space ( >>> )"""
    if newline:
        question += "\n"
    return input(question + " >>> ")


def get_goal_end_date():
    """Prompt user for their target goal date"""
    end_date_prompt = "By when do you want to achieve this goal? [YYYY-MM-DD]"
    end_date = validate.get_future_date(input_with_arrows(end_date_prompt))
    return end_date


def get_goal():
    """Prompt user on how many books they want to read as their goal."""
    goal_prompt = "How many books would you like to read?"
    goal_number = validate.goal_number(input_with_arrows(goal_prompt))
    return goal_number


def add_goal(db_name=""):
    """Prompt user to enter goal parameters, and then set that goal by adding it to the goals database."""
    try:
        goal_number = get_goal()
        end_date = get_goal_end_date()
        start_date = datetime.date.today()

        goal = validate.goal(goal_number, start_date, end_date)
        add_goal_to_database(goal, db_name=db_name)
    except argparse.ArgumentTypeError as e:
        print(e)
        raise e
