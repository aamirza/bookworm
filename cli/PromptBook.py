import datetime

from cli.option import Prompt


class PromptBook(Prompt):
    def __init__(self):
        super().__init__()
        self.books = []
        self._goal = 0
        self._start_date = None
        self._end_date = None
        self._current_day = datetime.datetime.today()  # for testing purposes

    # Belongs in database
    def __iadd__(self, value):
        self.books.append(value)
        return self

    # Belongs in database
    def __len__(self):
        return len(self.books)

    # Most likely belongs in database
    def __getitem__(self, item):
        return self.books[item]

    # Belongs in database
    @property
    def _incomplete_books(self):
        return [book for book in self.books if not book.is_complete]

    @property
    def goal(self):
        return self._goal

    @goal.setter
    def goal(self, value):
        try:
            if value >= 0:
                self._goal = value
            else:
                raise ValueError("The goal value should be higher than 0.")
        except TypeError:
            raise TypeError("Goal value must be an integer greater than 0.")

    @property
    def start_date(self):
        return self._start_date

    @start_date.setter
    def start_date(self, value):
        dt = self.extract_date(value)

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
        dt = self.extract_date(value)

        try:
            if dt < self.start_date:
                raise ValueError("End date cannot be before start date.")
        except TypeError:
            pass

        self._end_date = dt

    @property
    def _total_books_complete(self):
        """
        Calculates the number of books complete, and counts unfinished books
        as partially complete

        :return: (float)
        """
        progress = 0
        for book in self.books:
            progress += book.percent_complete
        return progress

    @property
    def total_progress(self):
        return self._total_books_complete / self.goal

    @property
    def books_complete(self):
        return len([book for book in self.books if book.is_complete])

    @property
    def recommended_pace(self):
        return self.goal / (self.end_date - self.start_date).days

    @property
    def days_complete(self):
        """
        Divide the total of books complete by the daily recommended pace
        to return how much of the goal has been completed in terms (units)
        of days.

        :return: float
        """
        return self._total_books_complete / self.recommended_pace

    @property
    def days_passed(self):
        return (datetime.datetime.today().date() - self.start_date).days

    @property
    def minimum_books(self):
        """
        Recommended pace times days passed returns how many books you should
        have read by now.
        :return: float
        """
        return self.recommended_pace * self.days_passed

    @property
    def books_ahead(self):
        """
        Returns how many books ahead of (if positive) or behind (if negative)
        schedule you are.
        :return: float
        """
        return self._total_books_complete - self.minimum_books

    @staticmethod
    def extract_date(value):
        if type(value) not in (str, datetime.date, datetime.datetime):
            raise ValueError("Date must be a datetime, date or string object.")
        elif isinstance(value, str):
            dt = datetime.datetime.strptime(value, "%Y-%m-%d").date()
        elif isinstance(value, datetime.datetime):
            dt = value.date()
        elif isinstance(value, datetime.date):
            dt = value
        return dt

    def is_book_list_empty(self):
        return len(self.books) == 0

    def add_book(self):
        pass

    def list_books(self):
        pass

    def update_book(self):
        pass

    def delete_book(self):
        pass

    def days_ahead(self, *, current_date=None, start_date=None, end_date=None):
        dt_from_str = lambda str: datetime.datetime.strptime(str, "%Y-%m-%d")
        current_date = datetime.datetime.today().date() if current_date is \
                                                           None else \
            dt_from_str(
            current_date).date()
        start_date = datetime.datetime(current_date.year, 1,
                                       1).date() if start_date is None else \
            dt_from_str(
            start_date).date()
        end_date = datetime.datetime(current_date.year, 12,
                                     31).date() if end_date is None else \
            dt_from_str(
            end_date).date()
        days_passed = (current_date - start_date).days
        days_ahead = self.days_complete - days_passed
        return round(days_ahead)

    def minimum_pages(self, book, force_next_day=False):
        """
        A test that calculates how many pages of your book you need to read
        based on how far behind you are. If you are ahead, maybe it should
        default to one day ahead? There should be an option for that.

        So how do we calculate how many pages we need to read? Say you had
        a book that you were 0% complete with. You're reading 183 books
        this year, and you're on day 0. You obviously need to finish half of
        it...

        Each book should count as 1 unit, regardless of how many pages. You
        do this by using percentages isntead of pages read/need to read. So
        we are 0% done with this book, we need to finish 50% of it, to count
        as 0.5 books / 183 books. We're going to sum up the percentage complete
        of each book (_total_pages_complete), take that as percentage of books
        we need to read (total_progress).

        In short, TOTAL's minimum progress minus TOTAL's total progress

        This is total progress required. To convert it to how many books
        you need to road, you need to multiply it by the goal. This is how much
        more of the book you need to read. Anything more than 1 means
        complete the book. A number like 0.5 means you need to read 50% more
        of the book you already have. Confusing,  I know.

        In short, take TOTAL's progress required multiply it by TOTAL's goal.
        In short, take TOTAL's books needed to read and add it to BOOK's
        per cent complete. This is how much more of the book you need to read.

        """
        books_needed = self.books_ahead
        if books_needed > 0 or force_next_day:
            books_needed = -1 * (self.recommended_pace - (
                        self._total_books_complete % self.recommended_pace))

        if books_needed <= -1:
            return book.total_pages
        elif books_needed <= 0:
            percent_needed = round(abs(books_needed) + book.percent_complete,
                                   2)
            if percent_needed > 1:
                return book.total_pages
            else:
                return book.total_pages * percent_needed
