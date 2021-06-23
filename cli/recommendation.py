# TODO: Write comments

from database.books import Books
from database.goals import Goals
from lib.goal_tracker import GoalTracker
from lib.shelf import Shelf

EMPTY_LINE = ""


def goal_message(tracker: GoalTracker):
    """Return a string in the form of 'You are X days ahead on your goal to
    read Y books by YYYY-MM-DD'"""
    opening_message = tracker.days_ahead_message()  # "You are 5 days ahead"
    opening_message += " on your goal to "
    opening_message += "r" + tracker.goal.message()[1:]  # "read 5 books by 2021" # Bootleg attempt to lowercase R.
    return opening_message


def num_of_books_complete_message(tracker):
    """Return the number of books complete in a message string format."""
    num_of_books_complete = tracker.shelf.num_complete_books
    message = f"You have completed {num_of_books_complete} book"
    message += "s" if num_of_books_complete != 1 else ""  # Add plural
    message += " so far."
    return message


def print_books(next_day=False, show_completed_books=False):
    goals_database = Goals()
    books_database = Books()
    tracker = GoalTracker(goals_database.get_current_goal(),
                          Shelf(books_database.get_all_books()))

    print(EMPTY_LINE)
    print(goal_message(tracker))
    print(EMPTY_LINE)
    print(num_of_books_complete_message(tracker))
    print(EMPTY_LINE)
    for recommendation in tracker.minimum_page_recommendations(
            force_next_day=next_day,
            show_completed_books=show_completed_books):
        print(recommendation)
    print(EMPTY_LINE)
