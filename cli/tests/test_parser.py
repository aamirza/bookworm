import argparse
import datetime
import unittest

import goal_parser
from cli import parser

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
            goal_parser.parse(args[2:])
        self.assertEqual(SUCCESS_CODE, exit_obj.exception.code)

    def test_goalParser_invalidGoal(self):
        args = ['python3', 'add_goal', '50', '2020-05-05']
        with self.assertRaises(SystemExit) as exit_obj:
            parser.main(args)
        self.assertEqual(INVALID_INPUT_CODE, exit_obj.exception.code)




    # A test for when you have a goal in the database, but no books

    # A test for when you have no goal in the database, but try to add a book

    # A test for when you have a goal, add a book and it gives a recommendation

    # A test for when you add two goals to the database


if __name__ == '__main__':
    unittest.main()
