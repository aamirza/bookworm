"""The GoalTracker class links a user's goal to their book reading progress."""

import datetime
from typing import Union

from lib.book import Book
from lib.audiobookseconds import AudiobookSeconds
from lib.goal import Goal
from lib.ibook import iBook
from lib.format import Format
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
        """Add a book to the shelf."""
        self.shelf.add_book(value)
        return self

    @property
    def total_progress(self) -> float:
        """Percent progress you have made towards completing your goal."""
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
        """Return true or false based on whether you are ahead of schedule on completing your goal."""
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
        """The minimum number of pages you should read to catch up to your goal's ideal pace."""
        # Check whether the user is calculating the minimum pages needed to make one day's worth of progress, or the
        # pages needed to catch up to their goal.
        if not (self.ahead_of_schedule or force_next_day):
            num_books_to_read = abs(self.num_books_ahead_of_schedule)
        else:
            num_books_to_read = self._num_books_required_to_advance_one_day

        entire_book = book.total_pages
        minimum_pages_to_read = book.pages_read

        if num_books_to_read >= 1:
            # The user needs to read the entire book if they are one or more books behind on their goal.
            minimum_pages_to_read = entire_book
        elif num_books_to_read < 1:
            # If the user is less than one book behind on their goal, they may only need to read a portion of the book.
            pages_to_read = book.total_pages * num_books_to_read
            minimum_pages_to_read = book.pages_read + pages_to_read
            if minimum_pages_to_read > entire_book:
                minimum_pages_to_read = entire_book

        if book.format == Format.AUDIOBOOK:
            # If it's an Audiobook, return results in Audiobook seconds.
            minimum_pages_to_read = AudiobookSeconds(int(minimum_pages_to_read)
                                                     )

        return round(minimum_pages_to_read)

    def minimum_page_recommendations(self, *, force_next_day: bool = False,
                                     show_completed_books=False):
        """Using the books in the shelf, give a recommendation on how much to read of each book to stay on track
        towards the goal."""
        for index, book in enumerate(self.shelf):
            if book.is_complete and not show_completed_books:
                continue

            recommendation = str(self.minimum_pages_needed(book, force_next_day=force_next_day))
            pages_read = str(book.pages_read)

            if book.format == Format.EBOOK:
                # Add a percentage sign if ebook
                recommendation += "%"
                pages_read += "%"
            elif book.format == Format.BOOK:
                # Prepend "page " to page number
                recommendation = "page " + recommendation
                pages_read = "page " + pages_read
            yield f"{book.id}. {book.title} – You need to read from " \
                  f"{pages_read} to {recommendation} today."

    def days_ahead_message(self):
        """A message that indicates how far ahead or behind the user is on their goal. e.g. 'You are 5 days ahead'"""
        pace_message = f"You are {self.days_ahead} day"
        if self.days_ahead != 1:
            pace_message += "s"
        pace_message += " ahead" if self.days_ahead > 0 else " behind"
        return pace_message

    @property
    def days_successfully_complete(self) -> float:
        """How much of the goal has been completed in terms (units) of days."""
        return (self.shelf.num_books_read_and_partially_read
                / self.goal.ideal_books_per_day)

    @property
    def days_ahead(self):
        """How many days ahead (if positive) or behind (if negative) the user is on their goal."""
        days_ahead = (self.days_successfully_complete -
                      self.goal.days_since_start)
        return round(days_ahead, 3)
