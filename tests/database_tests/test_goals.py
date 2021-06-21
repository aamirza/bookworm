import time
import unittest

from freezegun import freeze_time

import database.goals
from lib.goal import Goal


class GoalDatabaseTests(unittest.TestCase):
    def setUp(self) -> None:
        self.goals = database.goals.Goals(':memory:')
        self.example_goal = Goal(50, "2020-01-01", "2020-12-31")
        self.example_goal2 = Goal(10, "2019-01-01", "2020-12-31")

    def add_two_goals_to_database(self):
        self.goals.add_goal(self.example_goal)
        self.goals.add_goal(self.example_goal2)

    @freeze_time("2020-07-31")
    def test_addGoals_addsGoalsToDatabase(self):
        self.add_two_goals_to_database()
        self.assertEqual([self.example_goal, self.example_goal2],
                         self.goals.get_all_goals())

    @freeze_time("2020-07-31")
    def test_currentGoal_isLatestGoal(self):
        self.add_two_goals_to_database()
        self.assertEqual(self.example_goal2,
                         self.goals.get_current_goal())

    def test_noGoals_raisesError(self):
        with self.assertRaisesRegex(database.goals.NoGoalCreatedError,
                                    "You have no goals"):
            self.goals.get_current_goal()

    def test_inactivateAllGoals(self):
        self.add_two_goals_to_database()
        self.goals.inactivate_all_goals()
        self.assertIsNone(self.goals.get_current_goal())

    def test_activeGoalExists_noActiveGoal_returnsFalse(self):
        self.assertFalse(self.goals.active_goal_exists())

    @freeze_time("2020-07-31")
    def test_activeGoalExists_noActiveGoal_returnsTrue(self):
        self.add_two_goals_to_database()
        self.assertTrue(self.goals.active_goal_exists())



if __name__ == '__main__':
    unittest.main()
