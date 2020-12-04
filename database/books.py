import datetime
import sqlite3
import time
from typing import List, Union, Optional

from database.db import db
from database.goals import NoGoalCreatedError
from lib.ibook import iBook, Format
from lib.book import Book
from lib.audiobook import Audiobook
from lib.ebook import Ebook


class BookNotFoundError(Exception):
    pass


class Books(db):
    def __init__(self, db_name="") -> None:
        if db_name:
            super().__init__(db_name)
        else:
            super().__init__()

    def _book_constructor(self,
                          format: Union[Format, int],
                          title: str,
                          pages_read: int,
                          total_pages: int,
                          start_date: Optional[
                              Union[datetime.datetime, int]] = None,
                          id_num: Optional[int] = 0):
        book_format = Format(format)
        if book_format == Format.BOOK:
            return Book(title, pages_read, total_pages, start_date,
                        id_num=id_num)
        elif book_format == Format.EBOOK:
            return Ebook(title, pages_read, start_date, id_num=id_num)
        elif book_format == Format.AUDIOBOOK:
            return Audiobook(title, pages_read, total_pages, start_date,
                             id_num=id_num)

    def _extract_title(self, book: Union[str, iBook]):
        return book if isinstance(book, str) else book.title

    def _add_book(self, title: str, total_pages: int, format: int, ) -> None:
        """Add a book to the database"""
        with self.conn:
            self.c.execute("""
            INSERT INTO books (title, total_pages, format_id) 
            VALUES (?, ?, ?);
            """, (title, int(total_pages), format))

    def _add_goal_book(self, title, pages_read, start_date):
        with self.conn:
            self.c.execute("""
            INSERT INTO goalbooks (goal_id, book_id, pages_read, start_date)
            VALUES ((SELECT id FROM goals WHERE active = 1),
            (SELECT id FROM books WHERE title = ?), 
            ?, ?)
            """, (title, int(pages_read), start_date))

    def add_book(self, book: iBook) -> None:
        assert isinstance(book, iBook), "The book you pass into add_book() " \
                                        "should be of type iBook."
        if self.active_goal_exists():
            self._add_book(book.title, book.total_pages, book.format.value)
            self._add_goal_book(book.title, book.pages_read, book.start_date)
        else:
            raise NoGoalCreatedError("You must have a goal before you can add"
                                     " a book to the database.")

    def get_book(self, book: Union[iBook, str]) -> iBook:
        """Get a book from the database"""
        assert isinstance(book, str) or isinstance(book, iBook), \
            "get_book() accepts only either a string or an iBook type object" \
            " as an argument."

        title = self._extract_title(book)
        self.c.execute("""
        SELECT b.format_id, b.title, gb.pages_read, b.total_pages, 
        gb.start_date 
        FROM books b JOIN goalbooks gb
        ON (id = book_id)
        WHERE title=?
        """, (title,))
        book = self.c.fetchone()
        return None if book is None else self._book_constructor(*book)

    def get_book_by_id(self, id):
        self.c.execute("""
        SELECT b.format_id, b.title, gb.pages_read, b.total_pages, 
        gb.start_date, b.id
        FROM books b JOIN goalbooks gb
        ON (id = book_id)
        WHERE (b.id = ? 
               AND gb.goal_id = (SELECT goal_id FROM goals WHERE active=1))
        """, (id,))
        book = self.c.fetchone()
        return None if book is None else self._book_constructor(*book)

    def get_all_books(self):
        """"Get all books from the database"""
        self.c.execute("""
        SELECT b.format_id, b.title, gb.pages_read, b.total_pages, 
        gb.start_date, b.id 
        FROM books b JOIN goalbooks gb
        ON (id = book_id)
        WHERE (gb.goal_id = (SELECT goal_id FROM goals WHERE active=1))
        ORDER BY b.id
        """)
        books = [self._book_constructor(*book) for book in self.c.fetchall()]
        return books

    def update_pages_read(self, book: Union[iBook, str], pages_read):
        if not self.has_book(book):
            raise BookNotFoundError('The book you are trying to update ' \
                                    'was not found in the database.')
        if isinstance(book, str):
            book = self.get_book(book)

        with self.conn:
            self.c.execute("""
            UPDATE goalbooks
            SET pages_read = ?
            WHERE (book_id = (SELECT id FROM books WHERE title = ?))
            """, (int(pages_read), book.title))

    def update_book(self, book: Union[iBook, str], *,
                    title: Optional[str] = None,
                    total_pages: Optional[int] = None
                    ) -> iBook:
        # TODO: Needs to be broken up. Pages read separate from title/total pages
        """
        Update a book in the database by passing either its title or
        the book object itself.
        """
        if not self.has_book(book):
            raise BookNotFoundError('The book you are trying to update '
                                    'was not found in the database.')
        # If book title is passed, get the book object
        if isinstance(book, str):
            book = self.get_book(book)

        # Get attributes that need to be updated
        new_title = book.title if title is None else title
        new_total_pages = book.total_pages if total_pages is None else \
            total_pages

        self.c.execute("""
        UPDATE books 
        SET title = ?, total_pages = ? 
        WHERE title = ?
        """, (new_title, int(new_total_pages), book.title)
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
