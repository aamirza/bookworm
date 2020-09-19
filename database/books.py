import datetime
import sqlite3
import time
from typing import List, Union, Optional

from database.db import db
from goal_tracker import GoalTracker
from ibook import iBook, Format
from book import Book
from audiobook import Audiobook
from ebook import Ebook

"""
What will the database output?
---> List of all books.
---> List of books that are within goal date.
---> List of complete/incomplete books.
---> List of all books with index

How will it relate to the goal tracker?
---> The goal tracker will dump its goal here
---> The goal tracker will get list of books from here
---> All other calculations are local
"""


# Remember that validation is left to PromptHabit, so don't worry about it here

class BookNotFoundError(Exception):
    pass


class Shelf(db):
    def __init__(self, db_name="shelf.db") -> None:
        super().__init__(db_name)

    def _book_constructor(self,
                          format: Union[Format, int],
                          title: str,
                          pages_read: int,
                          total_pages: int,
                          start_date: Optional[
                              Union[datetime.datetime, int]] = None):
        book_format = Format(format)
        if book_format == Format.BOOK:
            return Book(title, pages_read, total_pages, start_date)
        elif book_format == Format.EBOOK:
            return Ebook(title, pages_read, start_date)
        elif book_format == Format.AUDIOBOOK:
            return Audiobook(title, pages_read, total_pages, start_date)

    def _extract_title(self, book: Union[str, iBook]):
        return book if isinstance(book, str) else book.title

    def get_all_tables(self) -> list:
        tables = self.c.execute(
            "SELECT name FROM sqlite_master WHERE type='table';")
        return [table[0] for table in tables]

    def _add_book(self, title: str, pages_read: int, total_pages: int,
                  format: int, start_date: int) -> None:
        """Add a book to the database"""
        with self.conn:
            self.c.execute("""
            INSERT INTO books 
            (title, pages_read, total_pages, format, start_date) 
            VALUES (?, ?, ?, ?, ?);
            """, (title, int(pages_read), int(total_pages), format, start_date)
                           )

    def add_book(self, book: iBook) -> None:
        assert isinstance(book, iBook), "The book you pass into add_book() " \
                                        "should be of type iBook."
        self._add_book(book.title, book.pages_read, book.total_pages,
                       book.format.value, book.start_date)

    def get_book(self, book: Union[iBook, str]) -> iBook:
        """Get a book from the database"""
        assert isinstance(book, str) or isinstance(book, iBook), \
            "get_book() accepts only either a string or an iBook type object" \
            " as an argument."
        title = self._extract_title(book)
        self.c.execute("""
        SELECT format, title, pages_read, total_pages, start_date 
        FROM books WHERE title=?
        """, (title,))
        book = self.c.fetchone()
        return None if book is None else self._book_constructor(*book)

    def get_all_books(self):
        """"Get all books from the database"""
        self.c.execute("""
        SELECT format, title, pages_read, total_pages,  start_date FROM books 
        ORDER BY book_id
        """)
        books = [self._book_constructor(*book) for book in self.c.fetchall()]
        return books

    def update_book(self, book: Union[iBook, str], *,
                    title: Optional[str] = None,
                    pages_read: Optional[int] = None,
                    total_pages: Optional[int] = None
                    ) -> iBook:
        """
        Update a book in the database by passing either its title or
        the book object itself.
        """
        if not self.has_book(book):
            raise BookNotFoundError('The book you are trying to update ' \
                                    'must already be in the database.')
        # If book title is passed, get the book object
        if isinstance(book, str):
            book = self.get_book(book)

        # Get attributes that need to be updated
        new_title = book.title if title is None else title
        new_pages_read = book.pages_read if pages_read is None else pages_read
        new_total_pages = book.total_pages if total_pages is None else \
            total_pages

        self.c.execute("""
        UPDATE books 
        SET title = ?, pages_read = ?, total_pages = ? 
        WHERE title = ?
        """, (new_title, int(new_pages_read), int(new_total_pages), book.title)
                       )

        # Return updated book object
        if new_title != book.title:
            # If the title has changed, return new title
            return self.get_book(new_title)
        else:
            return self.get_book(book)

    def has_book(self, book: Union[iBook, str]) -> bool:
        return self.get_book(book) is not None

    def remove_book(self, book: Union[str, iBook]) -> None:
        assert isinstance(book, iBook) or isinstance(book, str), \
            "Book must either be a str (title) or type iBook"
        if not self.has_book(book):
            raise BookNotFoundError(f"The book {book} was not found on your "
                                    f"shelf")
        title = self._extract_title(book)
        self.c.execute("""
        DELETE FROM books WHERE title = ?
        """, (title,))

    def get_current_goals(self):
        self.c.execute("""
        SELECT book_goal, start_date, end_date
        FROM goals
        """)
        return self.c.fetchall()
