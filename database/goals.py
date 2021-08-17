"""
Class interface for the goals table of the database. Stores and updates the user's active goal and its properties.
"""

from database.db import db
from lib.goal import Goal


class NoGoalCreatedError(Exception):
    """Error is raised when there is no goal in the database."""
    pass


class Goals(db):
    """Interface for interacting with the goals table of the database."""
    def __init__(self, db_name=""):
        if db_name:
            super().__init__(db_name)
        else:
            super().__init__()

    def get_current_goal(self) -> Goal:
        self.c.execute("""
        SELECT book_goal, start_date, end_date
        FROM goals
        WHERE active = 1
        """)
        try:
            goal = Goal(*self.c.fetchone())
        except TypeError:
            if len(self.get_all_goals()) == 0:
                # TODO: Make more user friendly.
                raise NoGoalCreatedError("You have no goals initialized. "
                                         "Add a goal with the command \"ag\"")
            else:
                goal = None
        return goal

    def get_all_goals(self):
        self.c.execute("""
        SELECT book_goal, start_date, end_date
        FROM goals
        """)
        goals = [Goal(*goal) for goal in self.c.fetchall()]
        return goals

    def add_goal(self, goal: Goal):
        assert type(goal) is Goal, "goal must be of type Goal"
        self.inactivate_all_goals()
        self.c.execute("""
        INSERT INTO GOALS (book_goal, start_date, end_date) VALUES (?, ?, ?) 
        """, (
            goal.num_books,
            self._date_to_unix_timestamp(goal.start_date),
            self._date_to_unix_timestamp(goal.end_date)
        ))

    def update_active_goal_num_books(self, num_books):
        self.c.execute("""
        UPDATE GOALS 
        SET book_goal = ?
        WHERE active = 1
        """, (num_books,))

    def update_active_goal_end_date(self, end_date):
        self.c.execute("""
        UPDATE GOALS
        SET end_date = ?
        WHERE active = 1
        """, (self._date_to_unix_timestamp(end_date),))

    def inactivate_all_goals(self):
        self.c.execute("""
        UPDATE GOALS
        SET active = 0
        WHERE active = 1
        """)
