import argparse
import unittest

from lib.ebook import Ebook
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

    def test_bookPages_validAudiobook_returnsSeconds(self):
        self.assertEqual(validate.book_pages("2:21:03"), 8463)

    def test_bookPages_invalidAudiobook_raisesError(self):
        with self.assertRaisesRegex(argparse.ArgumentTypeError,
                                    "is not a valid page format. It must be"):
            validate.book_pages("2:21")

    def test_bookPages_validPages_returnsPages(self):
        self.assertEqual(validate.book_pages('211'), 211)

    def test_book_pagesReadMoreThanTotalPages_raisesError(self):
        with self.assertRaisesRegex(argparse.ArgumentTypeError,
                                    "Pages read cannot be more than total"):
            book = validate.book("A valid book", 583, 491)

    def test_book_totalPagesModifiedForEbook_returns100(self):
        book = validate.book("A valid book", 74, 491, book_format="ebook")
        self.assertEqual(book.total_pages, 100)

    def test_book_returnsBook(self):
        book = validate.book("A valid book", 74, 491, book_format="ebook")
        self.assertTrue(isinstance(book, Ebook))


if __name__ == '__main__':
    unittest.main()
