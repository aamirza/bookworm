from database.db import db
from goal import Goal


class NoGoalCreatedError(Exception):
    pass


class Goals(db):
    def __init__(self, db_name="shelf.py"):
        super().__init__(db_name)

    def get_current_goal(self):
        self.c.execute("""
        SELECT book_goal, start_date, end_date
        FROM goals
        WHERE active = 1
        """)
        try:
            goal = Goal(*self.c.fetchone())
        except TypeError:
            if len(self.get_all_goals()) == 0:
                raise NoGoalCreatedError("You have no goals initialized.")
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
        assert type(goal) is Goal, "goal must be of type GoalTracker"
        self.inactivate_all_goals()
        self.c.execute("""
        INSERT INTO GOALS (book_goal, start_date, end_date) VALUES (?, ?, ?) 
        """, (
            goal.num_books,
            self._date_to_unix_timestamp(goal.start_date),
            self._date_to_unix_timestamp(goal.end_date)
        ))

    def inactivate_all_goals(self):
        self.c.execute("""
        UPDATE GOALS
        SET active = 0
        WHERE active = 1
        """)
