import datetime
from typing import Union

from ibook import iBook
from book import Book


# TODO: Make this database friendly
# TODO: Fix type hints

date_type = Union[str, datetime.datetime, datetime.date, None]
todays_date = datetime.datetime.today().date()

class GoalTracker:
    def __init__(self, book_goal: int = 0,
                 start_date: date_type = todays_date,
                 end_date: date_type = todays_date):
        self._book_goal = book_goal
        self._start_date = self._convert_to_date(start_date)
        self._end_date = self._convert_to_date(end_date)
        self.books = []

        # to track whether the database should be updated
        self._update_database = True

    def __iadd__(self, value: iBook):
        self.add_new_book(value)
        return self

    def add_new_book(self, book: iBook):
        assert isinstance(book, iBook), "The book you are adding should be" \
                                        "of type iBook"
        self._update_database = True
        self.books.append(book)

    @staticmethod
    def _convert_to_date(value) -> datetime.date:
        assert type(value) in (str, datetime.date, datetime.datetime), \
            "Date must be a datetime, date or string object."
        if isinstance(value, str):
            date = datetime.datetime.strptime(value, "%Y-%m-%d").date()
        elif isinstance(value, datetime.datetime):
            date = value.date()
        elif isinstance(value, datetime.date):
            date = value
        return date

    @property
    def _incomplete_books(self):
        return [book for book in self.books if not book.is_complete]

    @property
    def book_goal(self):
        return self._book_goal

    @book_goal.setter
    def book_goal(self, value):
        try:
            if value >= 0:
                self._book_goal = value
            else:
                raise ValueError("The goal value should be higher than 0.")
        except TypeError:
            raise TypeError("Goal value must be an integer greater than 0.")

    @property
    def start_date(self):
        return self._start_date

    @start_date.setter
    def start_date(self, value):
        dt = self._convert_to_date(value)
        try:
            if dt > self.end_date:
                raise ValueError("Start date cannot be after end date.")
        except TypeError:
            pass

        if dt > datetime.datetime.today().date():
            raise ValueError("Start date cannot be in the future.")
        else:
            self._start_date = dt

    @property
    def end_date(self):
        return self._end_date

    @end_date.setter
    def end_date(self, value):
        dt = self._convert_to_date(value)
        try:
            if dt < self.start_date:
                raise ValueError("End date cannot be before start date.")
        except TypeError:
            pass

        self._end_date = dt

    @property
    def _total_books_complete_and_uncomplete(self) -> float:
        """
        Calculates the number of books complete, and counts unfinished books
        as partially complete
        """
        progress = 0
        for book in self.books:
            progress += book.percent_complete
        return progress

    @property
    def total_progress(self):
        return self._total_books_complete_and_uncomplete / self.book_goal

    @property
    def num_books_complete(self):
        return len([book for book in self.books if book.is_complete])

    @property
    def ideal_pace(self):
        return self.book_goal / (self.end_date - self.start_date).days

    @property
    def days_passed_since_start(self) -> int:
        return (datetime.datetime.today().date() - self.start_date).days

    @property
    def ideal_books_complete(self) -> float:
        """
        How many books you should have read by now.
        """
        return self.ideal_pace * self.days_passed_since_start

    @property
    def num_books_ahead_of_schedule(self) -> float:
        """
        Returns how many books ahead (if positive) or behind (if negative)
        schedule you are.
        """
        return self._total_books_complete_and_uncomplete - \
               self.ideal_books_complete

    @property
    def ahead_of_schedule(self) -> bool:
        return self.num_books_ahead_of_schedule >= 0

    @property
    def shelf_is_empty(self) -> bool:
        return len(self.books) == 0

    @property
    def _num_books_required_to_advance_one_day(self) -> float:
        return self.ideal_pace - \
               (self._total_books_complete_and_uncomplete % self.ideal_pace)

    def minimum_pages_needed(self, book: Book, *,
                             force_next_day: bool = False):
        '''
        The minimum number of pages you should read to catch up to your
        goal.
        '''
        if self.ahead_of_schedule or force_next_day:
            books_needed = self._num_books_required_to_advance_one_day
        else:
            books_needed = abs(self.num_books_ahead_of_schedule)

        if books_needed >= 1:
            return book.total_pages
        elif books_needed >= 0:
            percent_of_book_to_complete = round(
                books_needed + book.percent_complete, 2)
            if percent_of_book_to_complete >= 1:
                return book.total_pages
            else:
                return book.total_pages * percent_of_book_to_complete
