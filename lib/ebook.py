from __future__ import annotations
import datetime
from typing import Optional

from lib.ibook import iBook, Format


class InvalidPercentageError(Exception):
    pass


class Ebook(iBook):
    Percent: int

    def __init__(self,
                 title: str,
                 pages_read: Percent,
                 start_date: datetime.datetime = datetime.datetime.today(),
                 id_num: Optional[int] = 0
                 ) -> None:
        super().__init__(Format.EBOOK, title, pages_read, 100, start_date,
                         id_num)

    @iBook.total_pages.getter
    def total_pages(self) -> Percent:
        return self._total_pages

    @iBook.total_pages.setter
    def total_pages(self, value: Percent) -> None:
        if value != 100:
            raise InvalidPercentageError("E-Book total pages cannot be any "
                                         "number other than 100 per cent")
        self._total_pages = 100
