from database.db import db
from goal import Goal
from goal_tracker import GoalTracker


class Goals(db):
    def __init__(self, db_name="shelf.py"):
        super().__init__(db_name)

    def add_goal(self, goal: Goal):
        assert type(goal) is GoalTracker, "goal must be of type GoalTracker"
        self.c.execute("""
        INSERT INTO GOALS (book_goal, start_date, end_date) VALUES (?, ?, ?) 
        """, (
            goal.num_books,
            self._date_to_unix_timestamp(goal.start_date),
            self._date_to_unix_timestamp(goal.end_date)
        ))
