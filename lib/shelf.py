"""Shelf class, to be used with the BOOKS table in the database"""
from typing import List

from ibook import iBook


class Shelf:
    def __init__(self, books=None):
        """Shelf class, to be used with the BOOKS table in the database"""
        if books:
            self.books = books
        else:
            self.books = []

    def __iadd(self, other):
        self.add_book(other)

    def add_book(self, book: iBook):
        assert isinstance(book, iBook), "The book you are adding should be" \
                                        "of type iBook"
        self.books.append(book)

    @property
    def incomplete_books(self):
        return [book for book in self.books if not book.is_complete]

    def num_books_read_and_partially_read(self):
        """
        Calculates the number of books complete, and counts unfinished books
        as partially complete
        """
        progress = 0
        for book in self.books:
            progress += book.percent_complete
        return progress