from freezegun import freeze_time
import datetime
from unittest import TestCase, mock

import goal_tracker
from goal import Goal
from lib import book, audiobook
from book import Book

"""
Test naming convention:
test_nameOfTestedFeature_expectedInput/testState_expectedBehaviour
"""

# TODO: Write these tests
"""

"""


class TestGoalTracker(TestCase):
    def setUp(self) -> None:
        self.tracker = goal_tracker.GoalTracker()

    def test_convertToDate_invalidType_raisesError(self):
        with self.assertRaisesRegex(AssertionError, "Date must be a "):
            Goal._convert_to_date(15728)

    def test_convertToDate_datetime_convertsToDate(self):
        self.assertEqual(
            datetime.date(2003, 5, 12),
            Goal._convert_to_date(datetime.datetime(2003, 5, 12))
        )

    def test_convertToDate_dateString_convertsToDate(self):
        self.assertEqual(
            datetime.date(2003, 5, 12),
            Goal._convert_to_date("2003-05-12")
        )

    def test_convertToDate_date_convertsToDate(self):
        self.assertEqual(
            datetime.date(2003, 5, 12),
            Goal._convert_to_date(datetime.date(2003, 5, 12))
        )

    @freeze_time("2020-01-01")
    def test_setStartDate_futureStartDate_returnsError(self):
        self.tracker.goal.end_date = "2602-01-13"
        with self.assertRaisesRegex(ValueError,
                                    "Start date cannot be in the future."):
            self.tracker.goal.start_date = "2589-01-12"

    def test_setStartDate_dateString_isConvertedToDate(self):
        self.tracker.goal.start_date = "2018-01-01"
        self.assertEqual(datetime.date(2018, 1, 1),
                         self.tracker.goal.start_date)

    def test_setStartDate_datetime_isConvertedToDate(self):
        self.tracker.goal.start_date = datetime.datetime.today()
        self.assertEqual(datetime.datetime.today().date(),
                         self.tracker.goal.start_date)

    def test_setStartDate_setToAfterEndDate_raisesError(self):
        self.tracker.goal.end_date = "2473-02-26"
        with self.assertRaisesRegex(ValueError,
                                    "Start date cannot be after end date."):
            self.tracker.goal.start_date = "2501-01-29"

    def test_setEndDate_beforeStartDate_returnsError(self):
        self.tracker.goal.start_date = "2020-03-12"
        with self.assertRaisesRegex(ValueError,
                                    "End date cannot be before start date."):
            self.tracker.goal.end_date = "2020-03-10"

    def test_idealPace(self):
        self.tracker.goal.num_books = 366
        self.tracker.goal.start_date = "2020-01-01"
        self.tracker.goal.end_date = "2021-01-01"
        self.assertEqual(1, self.tracker.goal.ideal_books_per_day)

    def test_incompleteBooks(self):
        book1 = Book("A complete book", 100, 100)
        book2 = Book("An incomplete book", 120, 184)
        book3 = audiobook.Audiobook("An incomplete audiobook", "5:23:12",
                                    "7:12:11")
        book4 = audiobook.Audiobook("A complete audibook", "9:14:23",
                                    "9:14:23")
        self.tracker += book1
        self.tracker += book2
        self.tracker += book3
        self.tracker += book4
        self.assertEqual(2, self.tracker.shelf.num_incomplete_books)
        self.assertEqual([book2, book3], self.tracker.shelf.incomplete_books)

    def test_isBookListIsEmpty_returnFalse(self):
        self.assertTrue(self.tracker.shelf_is_empty)

    def test_isBookListEmpty_returnTrue(self):
        self.tracker += Book("A new book", 100, 300)
        self.assertFalse(self.tracker.shelf_is_empty)

    def test_goalSetter_newNumber_setsGoal(self):
        self.tracker.goal.num_books = 50
        self.assertEqual(50, self.tracker.goal.num_books)

    def test_goalSetter_negativeNumber_raisesError(self):
        with self.assertRaisesRegex(ValueError,
                                    "The goal value should be higher than 0."):
            self.tracker.goal.num_books = -1

    def test_totalProgress_returnsPercentageComplete(self):
        self.tracker.goal.num_books = 50
        self.tracker += Book("A complete book", 100, 100)
        self.tracker += Book("A half complete book", 50, 100)
        self.assertEqual(0.03, self.tracker.total_progress)

    def test_booksComplete_returnsNumberOfBooksComplete(self):
        self.tracker += Book("A complete book", 100, 100)
        self.tracker += Book("An incomplete book", 50, 100)
        self.tracker += Book("Another complete book", 100, 100)

        self.assertEqual(2, self.tracker.shelf.num_complete_books)

    def test_minimumPages_incompleteBook_shouldBeFinished(self):
        self.tracker.goal.num_books = 366
        self.tracker.goal.start_date = "2020-01-01"
        self.tracker.goal.end_date = "2021-01-01"
        self.tracker += Book("Please finish this book", 0, 200)
        self.assertEqual(200,
                         self.tracker.minimum_pages_needed(
                             self.tracker.shelf.books[0]))

    @freeze_time("2020-01-02")
    def test_minimumPages_incompleteAudiobook_shouldBeHalfFinished(self):
        self.tracker.goal.num_books = 183
        self.tracker.goal.start_date = "2020-01-01"
        self.tracker.goal.end_date = "2021-01-01"
        self.tracker += audiobook.Audiobook("Please finish half this book",
                                         "0:00:00", "20:00:00")
        self.assertEqual(36000,
                         self.tracker.minimum_pages_needed(
                             self.tracker.shelf.books[0]))

    @freeze_time("2020-01-02")
    def test_minimumPages_beingAhead_returnsProgressForOneDay(self):
        self.tracker.goal.num_books = 183
        self.tracker.goal.start_date = "2020-01-01"
        self.tracker.goal.end_date = "2021-01-01"
        self.tracker += Book("A complete book", 100, 100)
        self.tracker += Book("An incomplete book", 7, 50)
        self.assertEqual(25,
                         self.tracker.minimum_pages_needed(
                             self.tracker.shelf.books[1]))

    def test_minimumPages_nextDayProgress_returnsProgressForOneDay(self):
        self.tracker.goal.num_books = 183
        self.tracker.goal.start_date = "2020-01-01"
        self.tracker.goal.end_date = "2021-01-01"
        self.tracker += Book("1 book finished", 100, 100)
        self.tracker += Book("Next book unfinished", 237, 700)
        self.assertEqual(350, self.tracker.minimum_pages_needed(
            self.tracker.shelf.books[1], force_next_day=True))
