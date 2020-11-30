import argparse
import unittest

from cli import validate


class ValidationTestCase(unittest.TestCase):
    def test_addGoal_addingNegativeInteger_raisesError(self):
        with self.assertRaisesRegex(argparse.ArgumentTypeError,
                                    "-2 is not a goal"):
            validate.goal_number('-2')

    def test_addGoal_addingNonInteger_raisesError(self):
        with self.assertRaisesRegex(argparse.ArgumentTypeError,
                                    "ha is not a valid integer"):
            validate.goal_number('ha')

    def test_addGoal_addingZero_RaisesError(self):
        with self.assertRaisesRegex(argparse.ArgumentTypeError,
                                    "0 is not a goal"):
            validate.goal_number('0')

    def test_addGoal_startDateAfterEndDate_RaisesError(self):
        with self.assertRaisesRegex(argparse.ArgumentTypeError,
                                    "Start date must come before end date."):
            validate.goal('20', '2156-09-11', '2156-09-11')

    def test_getDate_rubbishValue_raisesError(self):
        with self.assertRaisesRegex(argparse.ArgumentTypeError,
                                    "Date format must be in YYYY-MM-DD"):
            validate.get_date("march 22")

    def test_getDate_pastDate_raisesError(self):
        with self.assertRaisesRegex(argparse.ArgumentTypeError,
                                    "The date must be in the future."):
            validate.get_date("2020-07-12", in_the_future=True)


if __name__ == '__main__':
    unittest.main()
