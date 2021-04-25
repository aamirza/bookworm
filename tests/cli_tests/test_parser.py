import argparse
import datetime
import unittest
from unittest import mock

import book_parser
import goal_parser
import recommendation
from book import Book
from cli import parser
from goal import Goal
from goal_tracker import GoalTracker
from database.goals import NoGoalCreatedError
from shelf import Shelf

SUCCESS_CODE = 0
INVALID_INPUT_CODE = 2

class TestParser(unittest.TestCase):

    # A test for when you don't have a goal in the database
    def test_parseCommand_validCommand_returnsCommand(self):
        args = ['python3', 'add_goal']
        command = parser.parse_command(args[1:])
        self.assertEqual(command, 'add_goal')

    def test_parseCommand_invalidCommand_exitsProgram(self):
        args = ['python3', 'add_movie']
        with self.assertRaises(SystemExit) as exit_obj:
            parser.parse_command(args[1:])
        self.assertEqual(INVALID_INPUT_CODE, exit_obj.exception.code)

    def test_goalParser_showHelp(self):
        args = ['python3', 'add_goal', '-h']
        with self.assertRaises(SystemExit) as exit_obj:
            goal_parser.add_goal(args[2:])
        self.assertEqual(SUCCESS_CODE, exit_obj.exception.code)

    def test_goalParser_invalidGoal(self):
        args = ['python3', 'add_goal', '50', '2020-05-05']
        with self.assertRaises(SystemExit) as exit_obj:
            parser.main(args)
        self.assertEqual(INVALID_INPUT_CODE, exit_obj.exception.code)

    def test_bookParser_invalidFormat(self):
        args = ['python3', 'add_book', '-f', 'hbook', 'valid title', '221',
                '500']
        with self.assertRaises(SystemExit) as exit_obj:
            book_parser.add_book(args[2:])
        self.assertEqual(INVALID_INPUT_CODE, exit_obj.exception.code)

    def test_bookParser_invalidPages(self):
        args = ['python3', 'add_book', 'valid title', 'a221', '500']
        with self.assertRaises(SystemExit) as exit_obj:
            book_parser.add_book(args[2:])
        self.assertEqual(INVALID_INPUT_CODE, exit_obj.exception.code)

    def test_booksCompleteMessage_oneBookComplete(self):
        complete_book = Book("A complete book", 100, 100)
        shelf = Shelf([complete_book])
        goal = Goal("50", "2283-01-14", "2401-01-01")
        tracker = GoalTracker(goal, shelf)
        self.assertEqual("You have completed 1 book so far.",
                         recommendation.num_of_books_complete_message(tracker))

    def test_booksCompleteMessage_zeroBooksComplete(self):
        shelf = Shelf()
        goal = Goal("50", "2283-01-14", "2401-01-01")
        tracker = GoalTracker(goal, shelf)
        self.assertEqual("You have completed 0 books so far.",
                         recommendation.num_of_books_complete_message(tracker))

    def test_booksCompleteMessage_twoBooksComplete(self):
        complete_book = Book("A complete book", 100, 100)
        another_complete_book = Book("Another one", 100, 100)
        shelf = Shelf()
        goal = Goal("50", "2283-01-14", "2401-01-01")
        tracker = GoalTracker(goal, shelf)
        tracker.shelf.add_book(complete_book)
        tracker.shelf.add_book(another_complete_book)
        self.assertEqual("You have completed 2 books so far.",
                         recommendation.num_of_books_complete_message(tracker))

    @mock.patch('parser.recommendation.print_books')
    @mock.patch('parser.prompt.add_goal')
    def test_no_goal_initialized_launches_prompt_to_add_goal(self, mock_prompt, mock_recommendation):
        def raise_error(*args, **kwargs):
            raise NoGoalCreatedError

        mock_recommendation.side_effect = raise_error

        with self.assertRaises(NoGoalCreatedError):
            parser.main(['python3'])
        self.assertTrue(mock_prompt.called)


if __name__ == '__main__':
    unittest.main()
