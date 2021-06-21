import argparse
import datetime
import os
import unittest
from unittest.mock import patch

from cli import prompt
from cli import validate
from cli.validate import get_future_date
from database import goals
from lib.goal import Goal


@patch('builtins.input')
class TestPrompt(unittest.TestCase):
    @patch('cli.prompt.validate.goal_number')
    def test_invalid_goal_input_gets_validated(self, mock_validate_goal, mock_input):
        invalid_input = "-2"
        mock_input.return_value = invalid_input
        with self.assertRaises(argparse.ArgumentTypeError):
            prompt.add_goal()
        mock_validate_goal.assert_called_once_with(invalid_input)

    @patch.object(prompt.validate, 'get_future_date')
    def test_invalid_date_input_gets_validated(self, mock_validate_date, mock_input):
        invalid_input = "7"
        mock_input.return_value = invalid_input

        def get_futuure_date(output):
            return get_future_date(output)

        mock_validate_date.side_effect = get_futuure_date

        with self.assertRaises(argparse.ArgumentTypeError):
            prompt.add_goal()
        mock_validate_date.assert_called_once_with(invalid_input)

    @patch('cli.prompt.validate.goal')
    @patch('cli.prompt.get_goal')
    @patch('cli.prompt.get_goal_end_date')
    @patch('cli.prompt.add_goal_to_database')
    def test_valid_goal_adds_to_database(
            self, mock_add_goal_to_db, mock_get_date, mock_get_goal, mock_validate_goal, mock_input
    ):
        goal_number = 10
        goal_start_date = str(datetime.datetime.today().date())
        goal_end_date = "2498-10-05"

        mock_get_goal.return_value = 10
        mock_get_date.return_value = "2498-10-05"
        goal = Goal(goal_number, goal_start_date, goal_end_date)
        mock_validate_goal.return_value = goal

        prompt.add_goal()
        self.assertTrue(mock_add_goal_to_db.called)
        self.assertIn(goal, *mock_add_goal_to_db.call_args)

    @unittest.skip("First find a way to delete the test database automatically after you're done")
    @patch('prompt.get_goal')
    @patch('prompt.get_goal_end_date')
    def test_add_goal_prompt_adds_goal_to_database(self, mock_get_end_date, mock_get_goal, mock_input):
        mock_get_goal.return_value = 20
        mock_get_end_date.return_value = validate.get_future_date("2489-10-05")
        prompt.add_goal(db_name="test.db")
        goal_db = goals.Goals("test.db")
        self.assertTrue(goal_db.active_goal_exists())
        # Delete the database
        db_file_location = os.path.dirname(__file__)


if __name__ == '__main__':
    unittest.main()

    """Integration test"""
