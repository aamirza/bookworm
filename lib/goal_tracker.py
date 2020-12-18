import datetime
from typing import Union

from lib.book import Book
from lib.audiobook import AudiobookSeconds
from lib.goal import Goal
from lib.ibook import iBook
from format import Format
from lib.shelf import Shelf


Date = Union[str, datetime.datetime, datetime.date, None]
today = datetime.datetime.today().date()
year_from_now = datetime.datetime(today.year + 1, today.month,
                                  today.day).date()


class GoalTracker:
    def __init__(self, goal: Goal, shelf: Shelf):
        self.goal = goal
        self.shelf = shelf

    def __iadd__(self, value: iBook):
        self.shelf.add_book(value)
        return self

    @property
    def total_progress(self):
        return (self.shelf.num_books_read_and_partially_read
                / self.goal.num_books)

    @property
    def num_books_ahead_of_schedule(self) -> float:
        """
        Returns how many books ahead (if positive) or behind (if negative)
        schedule you are.
        """
        return (self.shelf.num_books_read_and_partially_read -
                self.goal.min_ideal_books_complete)

    @property
    def ahead_of_schedule(self) -> bool:
        return self.num_books_ahead_of_schedule >= 0

    @property
    def shelf_is_empty(self) -> bool:
        return self.shelf.is_empty

    @property
    def _num_books_required_to_advance_one_day(self) -> float:
        return (self.goal.ideal_books_per_day -
                (self.shelf.num_books_read_and_partially_read %
                 self.goal.ideal_books_per_day))

    def minimum_pages_needed(self, book: Book, *,
                             force_next_day: bool = False):
        '''
        The minimum number of pages you should read to catch up to your
        goal.
        '''
        if not (self.ahead_of_schedule or force_next_day):
            num_books_to_read = abs(self.num_books_ahead_of_schedule)
        else:
            num_books_to_read = self._num_books_required_to_advance_one_day

        entire_book = book.total_pages
        minimum_pages_to_read = book.pages_read

        if num_books_to_read >= 1:
            minimum_pages_to_read = entire_book
        elif num_books_to_read < 1:
            minimum_pages_to_read += book.total_pages * num_books_to_read

        if book.format == Format.AUDIOBOOK:
            minimum_pages_to_read = AudiobookSeconds(
                int(minimum_pages_to_read))
        return round(minimum_pages_to_read)

    def minimum_page_recommendations(self, *, force_next_day: bool = False):
        for index, book in enumerate(self.shelf):
            recommendation = str(self.minimum_pages_needed(book))
            pages_read = str(book.pages_read)
            if book.format == Format.EBOOK:
                # Add a percentage sign if ebook
                recommendation += "%"
                pages_read += "%"
            yield f"{book.id}. {book.title} – You need to read from " \
                  f"{pages_read} to {recommendation} today."

    def days_ahead_message(self):
        pace_message = f"You are {self.days_ahead} day"
        if self.days_ahead != 1:
            pace_message += "s"
        pace_message += " ahead" if self.days_ahead > 0 else " behind"
        return pace_message

    @property
    def days_successfully_complete(self) -> float:
        """
        How much of the goal has been completed in terms (units)
        of days.
        """
        return (self.shelf.num_books_read_and_partially_read
                / self.goal.ideal_books_per_day)

    @property
    def days_ahead(self):
        days_ahead = (self.days_successfully_complete -
                      self.goal.days_since_start)
        return round(days_ahead)
