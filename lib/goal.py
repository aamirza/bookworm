import datetime


class InternalError(Exception):
    pass


class Goal:
    def __init__(self, num_books, start_date, end_date):
        self._num_books = num_books
        self._start_date = self._convert_to_date(start_date)
        self._end_date = self._convert_to_date(end_date)

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
        else:
            raise InternalError("Couldn't convert date.")
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
        return (self.end_date - self.start_date).days

    @property
    def ideal_books_per_day(self) -> float:
        return self.num_books / self.total_duration

    @property
    def days_since_start(self) -> int:
        return (datetime.datetime.today().date() - self.start_date).days

    @property
    def min_ideal_books_complete(self):
        return self.ideal_books_per_day * self.days_since_start
