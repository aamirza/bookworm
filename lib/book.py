"""The Book class is for representing books whose length is measured in
numbered pages."""

import datetime
from typing import Optional

from lib.ibook import iBook
from format import Format


class Book(iBook):
    def __init__(self,
                 title: str,
                 pages_read: int,
                 total_pages: int,
                 start_date: datetime.datetime = datetime.datetime.today(),
                 id_num: Optional[int] = 0):
        super().__init__(Format.BOOK, title, pages_read, total_pages,
                         start_date, id_num)
