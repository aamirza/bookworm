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
    opening_message += tracker.goal.message().lower()  # "read 5 books by 2021"
    return opening_message


def print_books(next_day=False):
    goals_database = Goals()
    books_database = Books()
    tracker = GoalTracker(goals_database.get_current_goal(),
                          Shelf(books_database.get_all_books()))

    print(EMPTY_LINE)
    print(goal_message(tracker))
    print(EMPTY_LINE)
    for recommendation in tracker.minimum_page_recommendations(
            force_next_day=next_day):
        print(recommendation)
    print(EMPTY_LINE)