import argparse
import unittest

from cli import parser


class TestParser(unittest.TestCase):

    # A test for when you don't have a goal in the database
    def test_NoGoal_showsHelpMessage(self):
        self.assertEqual(argparse.Namespace(command='add_goal'),
                         parser.parse_args(['add_goal']))

    def test_addValidGoal(self):
        pass

    # A test for when you have a goal in the database, but no books

    # A test for when you have no goal in the database, but try to add a book

    # A test for when you have a goal, add a book and it gives a recommendation

    # A test for when you add two goals to the database


if __name__ == '__main__':
    unittest.main()
