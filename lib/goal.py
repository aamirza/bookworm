"""Goal is a class representing the user's book reading goal"""

import datetime
import time


class DatetimeConversionError(Exception):
    """Raised when there is an error assigning a date to the Goal."""
    pass


class Goal:
    """Represents the user's book reading goal and various calculations related to it."""
    def __init__(self, num_books, start_date, end_date):
        self._num_books = num_books
        self._start_date = self._convert_to_date(start_date)
        self._end_date = self._convert_to_date(end_date)
        self._start_date_before_end_date()

    def __eq__(self, other):
        if isinstance(other, Goal):
            equal_start_date = self.start_date == other.start_date
            equal_end_date = self.end_date == other.end_date
            equal_num_books = self.num_books == other.num_books
            if equal_end_date and equal_start_date and equal_num_books:
                return True
        return False

    def _start_date_before_end_date(self):
        """Ensure that the goal start date is not after the goal end date."""
        if self.start_date >= self.end_date:
            raise ValueError("Start date needs to be before end date")

    @staticmethod
    def _convert_to_date(value) -> datetime.date:
        """Convert myriad date and time formate to a Date object."""
        assert type(value) in (str, datetime.date, datetime.datetime, int), \
            "Date must be a datetime, date or string object."
        if isinstance(value, str):
            date = datetime.datetime.strptime(value, "%Y-%m-%d").date()
        elif isinstance(value, datetime.datetime):
            date = value.date()
        elif isinstance(value, datetime.date):
            date = value
        elif isinstance(value, int):
            date = datetime.datetime.fromtimestamp(value).date()
        else:
            raise DatetimeConversionError("Couldn't convert date.")
        return date

    ### GETTERS AND SETTERS ###

    @property
    def num_books(self):
        return self._num_books

    @num_books.setter
    def num_books(self, value):
        try:
            if value >= 0:
                self._num_books = value
            else:
                raise ValueError("The goal value should be higher than 0.")
        except TypeError:
            raise TypeError("Goal value must be an integer greater than 0.")

    @property
    def start_date(self):
        return self._start_date

    @start_date.setter
    def start_date(self, value):
        start_date = self._convert_to_date(value)
        try:
            if start_date <= self.end_date:
                pass
            else:
                raise ValueError("Start date cannot be after end date.")
        except TypeError:
            # End date not set
            pass

        if start_date <= datetime.datetime.today().date():
            self._start_date = start_date
        else:
            raise ValueError("Start date cannot be in the future.")

    @property
    def end_date(self):
        return self._end_date

    @end_date.setter
    def end_date(self, value):
        end_date = self._convert_to_date(value)
        try:
            if end_date < self.start_date:
                raise ValueError("End date cannot be before start date.")
        except TypeError:
            # Start date not set yet
            pass

        self._end_date = end_date

    @property
    def total_duration(self) -> int:
        """How long the goal is in terms of days"""
        return (self.end_date - self.start_date).days

    @property
    def ideal_books_per_day(self) -> float:
        """The ideal pace to be working on the goal, in number of books per day."""
        return self.num_books / self.total_duration

    @property
    def days_since_start(self) -> int:
        """How many days it has been since the goal was started."""
        return (datetime.datetime.today().date() - self.start_date).days

    @property
    def min_ideal_books_complete(self):
        """Ideally, how many books you should have completed, if you went at the ideal pace."""
        return self.ideal_books_per_day * self.days_since_start

    def message(self):
        """Your goal stated in a message i.e. 'Read 50 books by January 1, 2021."""
        verbose_end_date = datetime.date.strftime(self.end_date, "%B %-d, %Y")  # In format "Month DD, YYYY"
        return f"Read {self.num_books} books by {verbose_end_date}"
