from __future__ import annotations
from abc import ABC, abstractmethod
import datetime
from enum import Enum


class Format(Enum):
    BOOK = 0
    EBOOK = 1
    AUDIOBOOK = 2


class iBook(ABC):
    def __init__(self,
                 book_format: Format,
                 title: str,
                 pages_read: int = 0,
                 total_pages: int = 0,
                 start_date: datetime.datetime = datetime.datetime.today()
                 ) -> None:
        assert total_pages >= pages_read, \
            "Total pages cannot be less than pages read."

        self.format = Format(book_format)
        self.title = title
        self._pages_read = pages_read
        self._total_pages = total_pages
        self.start_date = start_date

    def __str__(self) -> str:
        return self.title

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.title}, {self.pages_read}, " \
               f"{self.total_pages})"

    def __eq__(self, other):
        if isinstance(other, iBook):
            return self.title == other.title and self.format == other.format
        else:
            return other == self.title

    def __contains__(self, item):
        return item in self.title

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
    def total_pages(self, value: int) -> None:
        self._total_pages = value

    def complete(self) -> None:
        self.pages_read = self.total_pages