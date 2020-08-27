from freezegun import freeze_time
import unittest

from audiobook import Audiobook, AudiobookSeconds
from goal_tracker import GoalTracker
from book import Book
from database.shelf import Shelf, BookNotFoundError
from ebook import Ebook

"""
Test naming convention:
test_nameOfTestedFeature_expectedInput/testState_expectedBehaviour
"""


class TestDatabase(unittest.TestCase):
    def setUp(self) -> None:
        self.shelf = Shelf(":memory:")

    def test_createTables_searchDatabases_GetsAllDatabases(self) -> None:
        self.assertEqual(['formats', 'sqlite_sequence', 'books', 'goals'],
                         self.shelf.get_all_tables())

    def test_addBook_addingBookObject_addsToDatabase(self) -> None:
        book = Book("This is a book", 147, 506)
        ebook = Ebook("And another book", 55)
        audiobook = Audiobook("An audiobook", "1:15:23", "6:33:24")
        self.shelf.add_book(book)
        self.shelf.add_book(ebook)
        self.shelf.add_book(audiobook)
        all_books = self.shelf.get_all_books()
        self.assertEqual([book, ebook, audiobook], all_books)

    def test_addBook_addingNonBook_returnsAssertionError(self):
        with self.assertRaisesRegex(AssertionError, "The book you pass"):
            self.shelf.add_book("This isn't a book object")

    def test_getBook_nonBook_returnsAssertionError(self):
        with self.assertRaisesRegex(AssertionError, "get_book()"):
            self.shelf.get_book(125)

    def test_updateBook_updatingPages_updatesInDatabase(self):
        book = Book("You should read this book today", 120, 582)
        self.shelf.add_book(book)
        self.assertEqual([book], self.shelf.get_all_books())
        self.shelf.update_book(book, pages_read=192)
        self.assertEqual(192, self.shelf.get_book(book).pages_read)

    def test_updateBook_updatingBookNotInDatabase_raisesError(self):
        book1 = Book("This is my first book", 0, 42)
        self.shelf.add_book(book1)
        book2 = Book("This is my second book", 0, 1200)
        with self.assertRaisesRegex(BookNotFoundError,
                                    "The book you are trying"):
            self.shelf.update_book(book2, pages_read=100)

    def test_updateBook_updateAudiobookSeconds_updatesAudiobookSeconds(self):
        audiobook = Audiobook("A relaxing book", "2:27:41", "19:21:34")
        self.shelf.add_book(audiobook)
        self.shelf.update_book(audiobook,
                               pages_read=AudiobookSeconds("4:51:26"))

    def test_getBook_bookObject_getsBookFromDatabase(self):
        book1 = Book("This is a book", 100, 200)
        self.shelf.add_book(book1)
        self.assertEqual(book1, self.shelf.get_book(book1))

    def test_hasBook_bookInDatabase_returnsTrue(self):
        book1 = Book("A book on my shelf", 50, 100)
        self.shelf.add_book(book1)
        self.assertTrue(self.shelf.has_book(book1))
        self.assertTrue(self.shelf.has_book("A book on my shelf"))

    def test_hasBook_nonexistantBook_returnsFalse(self):
        self.assertFalse(self.shelf.has_book("This book is fake"))

    def test_removeBook_invalidInput_raisesAssertionError(self):
        book = Audiobook("A relaxing book", "2:38:41", "5:15:22")
        self.shelf.add_book(book)
        with self.assertRaisesRegex(AssertionError, "Book must either be a "):
            self.shelf.remove_book(42)

    def test_removeBook_nonexistantBook_raisesError(self):
        book = Ebook("Pride and Prejudice", 28)
        with self.assertRaisesRegex(BookNotFoundError, "The book Pride and "
                                                       "Prejudice"):
            self.shelf.remove_book(book)

    def test_removeBook_deletesBookFromShelf(self):
        book = Audiobook("A relaxing book", "2:38:41", "5:15:22")
        self.shelf.add_book(book)
        self.shelf.remove_book(book)
        self.assertFalse(self.shelf.has_book(book))

    @freeze_time("2020-07-31")
    def test_addGoal_addsGoalToDatabase(self):
        goal = GoalTracker(50, "2020-01-01", "2020-12-31")
        self.shelf.add_goal(goal)
        self.assertEqual([goal], self.shelf.get_current_goals())


if __name__ == '__main__':
    unittest.main()
