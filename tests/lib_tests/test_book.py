from unittest import TestCase

from lib.book import Book
from lib.audiobook import Audiobook

"""
Naming convention: test_functionName_input/TestState_expectedResult
"""

"""
Alright! So I don't need to redo the book file at all. 
"""


class TestBook(TestCase):
    def setUp(self) -> None:
        self.book = Book("A really good book", 100, 300)

    def test_str_returnsBookTitle(self):
        self.assertEqual(str(self.book), "A really good book")

    def test_percentComplete_returnsFloat(self):
        self.assertEqual(self.book.percent_complete, 1 / 3)

    def test_isComplete_bookNotComplete_returnsFalse(self):
        self.assertFalse(self.book.is_complete)

    def test_isComplete_bookComplete_returnsTrue(self):
        self.book.pages_read = 300
        self.assertTrue(self.book.is_complete)

    def test_setPagesComplete_pagesCompleteMoreThanTotalPages_raisesError(
            self):
        with self.assertRaisesRegex(
                ValueError,
                f"{str(self.book)} is only {self.book.total_pages} pages long,"
                f" your value should be less than that."):
            self.book.pages_read = 301

    def test_setPagesRead_negativePages_raisesError(self):
        with self.assertRaisesRegex(ValueError,
                                    f"Pages complete can't be negative"):
            self.book.pages_read = -1

    def test_percentComplete_bookComplete_returns100(self):
        self.book.pages_read = 300
        self.assertEqual(self.book.percent_complete, 1)

    def test_setComplete_completesBook(self):
        self.book.complete()
        self.assertTrue(self.book.is_complete)

    def test_repr_isFormattedProperly(self):
        self.assertEqual('Book(A really good book, 100, 300)',
                         repr(self.book))

    def test_eq_booksWithSameTitleAndFormat_areTheSameBook(self):
        book1 = Book("This is a book", 1, 100)
        book2 = Book("This is a book", 5, 29)
        book3 = Audiobook("This is a book", 1, 100)
        self.assertEqual(book1, book2)
        self.assertNotEqual(book1, book3)

    def test_contains_title_isInBook(self):
        self.assertIn("A book", Book("A book", 0, 100))

    def test_contains_title_isInListOfBooks(self):
        book_list = [Book("My first book", 0, 100),
                     Book("My second book", 0, 120)]
        self.assertIn("My first book", book_list)
