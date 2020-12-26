"""
iBook is an abstract base class for classes such as Book, Audiobook, and Ebook.

Book: Books with length measured by pages.
Audiobook: Books with length measured by time (seconds)
Ebook: Books with length measured by percent complete.
"""

from __future__ import annotations
from abc import ABC
import datetime
from typing import Union

from audiobookseconds import AudiobookSeconds
from format import Format


class iBook(ABC):
    def __init__(self,
                 book_format: Format,
                 title: str,
                 pages_read: Union[int, AudiobookSeconds] = 0,
                 total_pages: Union[int, AudiobookSeconds] = 0,
                 start_date: datetime.datetime = datetime.datetime.today(),
                 id_num: int = 0
                 ) -> None:
        """
        :param book_format: Format of either Book, Ebook or Audiobook
        :param title: Title of the book
        :param pages_read: How many pages of the book that have been read
        :param total_pages:  How many pages the book has
        :param start_date: When the book was started or created
        :param id_num: #ID, used for database sorting. Defaults to 0 for none.
        """
        # TODO: Turn into proper error
        assert total_pages >= pages_read, \
            "Total pages cannot be less than pages read."

        self.format = Format(book_format)
        self.title = title
        self._pages_read = pages_read
        self._total_pages = total_pages
        self.start_date = start_date
        self.id = id_num

    def __str__(self) -> str:
        return self.title

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.title}, {self.pages_read}, " \
               f"{self.total_pages})"

    def __eq__(self, other):
        """
        For iBooks: if title and format are same, then book is same. '
        For strings: If title is same, then book is same.
        """
        if isinstance(other, iBook):
            return self.title == other.title and self.format == other.format
        else:
            return other == self.title

    def __contains__(self, title):
        """For getting the book in a list of books via the title."""
        return title in self.title

    @property
    def percent_complete(self) -> float:
        return self.pages_read / self.total_pages

    @property
    def is_complete(self) -> bool:
        return self.pages_read == self.total_pages

    @property
    def pages_read(self) -> int:
        return self._pages_read

    @pages_read.setter
    def pages_read(self, pages_read: int) -> None:
        if pages_read < 0:
            raise ValueError("Pages complete can't be negative")
        elif pages_read > self.total_pages:
            raise ValueError(f'{str(self)} is only {self.total_pages} pages '
                             f'long, your value should be less than that.')
        else:
            self._pages_read = pages_read

    @property
    def total_pages(self) -> int:
        return self._total_pages

    @total_pages.setter
    def total_pages(self, pages: int) -> None:
        self._total_pages = pages

    def complete(self) -> None:
        self.pages_read = self.total_pages
