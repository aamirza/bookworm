"""Shelf class, to be used with the BOOKS table in the database. It is a container for the books the user has read or
is reading."""
import collections
from typing import List

from lib.ibook import iBook


class Shelf(collections.abc.Sequence):
    def __init__(self, books=None):
        """Shelf class, to be used with the BOOKS table in the database"""
        if books:
            self.books = books
        else:
            self.books = []

    def __iadd__(self, other):
        self.add_book(other)

    def __getitem__(self, item):
        return self.books[item]

    def __len__(self):
        return len(self.books)

    def contains(self, item):
        return self.__contains__(item)

    def add_book(self, book: iBook):
        assert isinstance(book, iBook), "The book you are adding should be" \
                                        " of type iBook"
        self.books.append(book)

    @property
    def is_empty(self):
        return len(self) == 0

    @property
    def incomplete_books(self):
        return [book for book in self if not book.is_complete]

    @property
    def complete_books(self):
        return [book for book in self.books if book.is_complete]

    @property
    def num_complete_books(self):
        return len(self.complete_books)

    @property
    def num_incomplete_books(self):
        return len(self.incomplete_books)

    @property
    def num_books_read_and_partially_read(self):
        """
        Calculates the number of books complete, and counts unfinished books
        as partially complete
        """
        progress = 0
        for book in self.books:
            progress += book.percent_complete
        return progress
