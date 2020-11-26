import argparse
import unittest

from cli import parser


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
        self.assertEqual(2, exit_obj.exception.code)

    def test_goalParser_showHelp(self):
        args = ['python3', 'add_goal', '-h']
        with self.assertRaises(SystemExit) as exit_obj:
            parser.goal_parser(args[2:])
        self.assertEqual(0, exit_obj.exception.code)

    def test_goalParser_validGoal(self):
        pass

    # A test for when you have a goal in the database, but no books

    # A test for when you have no goal in the database, but try to add a book

    # A test for when you have a goal, add a book and it gives a recommendation

    # A test for when you add two goals to the database


if __name__ == '__main__':
    unittest.main()
