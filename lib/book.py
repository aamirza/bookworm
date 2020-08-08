import datetime

from ibook import iBook, Format


class Book(iBook):
    def __init__(self,
                 title: str,
                 pages_read: int,
                 total_pages: int,
                 start_date: datetime.datetime = datetime.datetime.today()):
        super().__init__(Format.BOOK, title, pages_read, total_pages,
                         start_date)
