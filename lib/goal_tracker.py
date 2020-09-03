import datetime
from typing import Union

from goal import Goal
from ibook import iBook
from book import Book

# TODO: Make this database friendly
# TODO: Fix type hints

Date = Union[str, datetime.datetime, datetime.date, None]
today = datetime.datetime.today().date()


class GoalTracker:
    def __init__(self, book_goal: int = 0, start_date: Date = today,
                 end_date: Date = today):
        self.goal = Goal(book_goal, start_date, end_date)
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

    @property
    def _incomplete_books(self):
        return [book for book in self.books if not book.is_complete]

    @property
    def book_goal(self):
        return self.goal.num_books

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
        return self.book_goal / self.goal.total_duration

    @property
    def ideal_books_complete(self) -> float:
        """How many books you should have read by now."""
        return self.ideal_pace * self.goal.days_since_start

    @property
    def num_books_ahead_of_schedule(self) -> float:
        """
        Returns how many books ahead (if positive) or behind (if negative)
        schedule you are.
        """
        return (self._total_books_complete_and_uncomplete -
                self.goal.min_ideal_books_complete)

    @property
    def ahead_of_schedule(self) -> bool:
        return self.num_books_ahead_of_schedule >= 0

    @property
    def shelf_is_empty(self) -> bool:
        return len(self.books) == 0

    @property
    def _num_books_required_to_advance_one_day(self) -> float:
        return (self.goal.ideal_books_per_day -
                (self._total_books_complete_and_uncomplete %
                 self.goal.ideal_books_per_day))

    def minimum_pages_needed(self, book: Book, *,
                             force_next_day: bool = False):
        '''
        The minimum number of pages you should read to catch up to your
        goal.
        '''
        if not self.ahead_of_schedule and not force_next_day:
            num_books_to_read = abs(self.num_books_ahead_of_schedule)
        else:
            num_books_to_read = self._num_books_required_to_advance_one_day

        entire_book = book.total_pages
        if 0 <= num_books_to_read < 1:
            percent_of_book_to_complete = (num_books_to_read +
                                           book.percent_complete)
            if percent_of_book_to_complete >= 1:
                return entire_book
            else:
                return book.total_pages * round(percent_of_book_to_complete, 2)
        elif num_books_to_read >= 1:
            return entire_book
