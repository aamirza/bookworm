import unittest

from audiobook import Audiobook
from book import Book
from shelf import Shelf


class ShelfTests(unittest.TestCase):
    def setUp(self):
        self.shelf = Shelf()
        self.book1 = Book("A complete book", 100, 100)
        self.book2 = Book("An incomplete book", 120, 184)
        self.book3 = Audiobook("An incomplete audiobook", "5:23:12",
                               "7:12:11")
        self.book4 = Audiobook("A complete audiobook", "9:14:23",
                               "9:14:23")

    def add_all_books_to_shelf(self):
        self.shelf.add_book(self.book1)
        self.shelf.add_book(self.book2)
        self.shelf.add_book(self.book3)
        self.shelf.add_book(self.book4)

    def test_shelfContainsBook(self):
        self.add_all_books_to_shelf()
        self.assertTrue(self.shelf.contains("A complete audiobook"))

    def test_shelfIndexOfBook(self):
        self.add_all_books_to_shelf()
        self.assertEqual(0, self.shelf.index("A complete book"))

    def test_shelf_incompleteBooks(self):
        self.assertEqual(0, len(self.shelf.incomplete_books))
        self.add_all_books_to_shelf()
        self.assertEqual(2, self.shelf.num_incomplete_books)

    def test_shelf_completeBooks(self):
        self.assertEqual(0, len(self.shelf.complete_books))
        self.add_all_books_to_shelf()
        self.assertEqual(2, len(self.shelf.complete_books))


if __name__ == '__main__':
    unittest.main()
