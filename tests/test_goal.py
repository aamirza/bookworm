from freezegun import freeze_time
import datetime
from unittest import TestCase, mock

import goal
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
        self.goal = goal.GoalTracker()

    def test_convertToDate_invalidType_raisesError(self):
        with self.assertRaisesRegex(AssertionError, "Date must be a "):
            self.goal._convert_to_date(15728)

    def test_convertToDate_datetime_convertsToDate(self):
        self.assertEqual(
            datetime.date(2003, 5, 12),
            self.goal._convert_to_date(datetime.datetime(2003, 5, 12))
        )

    def test_convertToDate_dateString_convertsToDate(self):
        self.assertEqual(
            datetime.date(2003, 5, 12),
            self.goal._convert_to_date("2003-05-12")
        )

    def test_convertToDate_date_convertsToDate(self):
        self.assertEqual(
            datetime.date(2003, 5, 12),
            self.goal._convert_to_date(datetime.date(2003, 5, 12))
        )

    @freeze_time("2020-01-01")
    def test_setStartDate_futureStartDate_returnsError(self):
        self.goal.end_date = "2602-01-13"
        with self.assertRaisesRegex(ValueError,
                                    "Start date cannot be in the future."):
            self.goal.start_date = "2589-01-12"

    def test_setStartDate_dateString_isConvertedToDate(self):
        self.goal.start_date = "2018-01-01"
        self.assertEqual(datetime.date(2018, 1, 1), self.goal.start_date)

    def test_setStartDate_datetime_isConvertedToDate(self):
        self.goal.start_date = datetime.datetime.today()
        self.assertEqual(datetime.datetime.today().date(),
                         self.goal.start_date)

    def test_setStartDate_setToAfterEndDate_raisesError(self):
        self.goal.end_date = "2473-02-26"
        with self.assertRaisesRegex(ValueError,
                                    "Start date cannot be after end date."):
            self.goal.start_date = "2501-01-29"

    def test_setEndDate_beforeStartDate_returnsError(self):
        self.goal.start_date = "2020-03-12"
        with self.assertRaisesRegex(ValueError,
                                    "End date cannot be before start date."):
            self.goal.end_date = "2020-03-10"

    def test_idealPace(self):
        self.goal.book_goal = 366
        self.goal.start_date = "2020-01-01"
        self.goal.end_date = "2021-01-01"
        self.assertEqual(1, self.goal.ideal_pace)

    def test_incompleteBooks(self):
        book1 = Book("A complete book", 100, 100)
        book2 = Book("An incomplete book", 120, 184)
        book3 = audiobook.Audiobook("An incomplete audiobook", "5:23:12",
                                    "7:12:11")
        book4 = audiobook.Audiobook("A complete audibook", "9:14:23",
                                    "9:14:23")
        self.goal += book1
        self.goal += book2
        self.goal += book3
        self.goal += book4
        self.assertEqual(2, len(self.goal._incomplete_books))
        self.assertEqual([book2, book3], self.goal._incomplete_books)

    def test_isHabitListEmpty_returnFalse(self):
        self.assertTrue(self.goal.shelf_is_empty)

    def test_isHabitListEmpty_returnTrue(self):
        self.goal += Book("A new book", 100, 300)
        self.assertFalse(self.goal.shelf_is_empty)

    def test_goalSetter_newNumber_setsGoal(self):
        self.goal.book_goal = 50
        self.assertEqual(50, self.goal.book_goal)

    def test_goalSetter_negativeNumber_raisesError(self):
        with self.assertRaisesRegex(ValueError,
                                    "The goal value should be higher than 0."):
            self.goal.book_goal = -1

    def test_totalProgress_returnsPercentageComplete(self):
        self.goal.book_goal = 50
        self.goal += Book("A complete book", 100, 100)
        self.goal += Book("A half complete book", 50, 100)
        self.assertEqual(0.03, self.goal.total_progress)

    def test_booksComplete_returnsNumberOfBooksComplete(self):
        self.goal += Book("A complete book", 100, 100)
        self.goal += Book("An incomplete book", 50, 100)
        self.goal += Book("Another complete book", 100, 100)

        self.assertEqual(2, self.goal.num_books_complete)

    def test_minimumPages_incompleteBook_shouldBeFinished(self):
        self.goal.book_goal = 366
        self.goal.start_date = "2020-01-01"
        self.goal.end_date = "2021-01-01"
        self.goal += Book("Please finish this book", 0, 200)
        self.assertEqual(200,
                         self.goal.minimum_pages_needed(self.goal.books[0]))

    @freeze_time("2020-01-02")
    def test_minimumPages_incompleteAudiobook_shouldBeHalfFinished(self):
        self.goal.book_goal = 183
        self.goal.start_date = "2020-01-01"
        self.goal.end_date = "2021-01-01"
        self.goal += audiobook.Audiobook("Please finish half this book",
                                         "0:00:00", "20:00:00")
        self.assertEqual(36000,
                         self.goal.minimum_pages_needed(self.goal.books[0]))

    @freeze_time("2020-01-02")
    def test_minimumPages_beingAhead_returnsProgressForOneDay(self):
        self.goal.book_goal = 183
        self.goal.start_date = "2020-01-01"
        self.goal.end_date = "2021-01-01"
        self.goal += Book("A complete book", 100, 100)
        self.goal += Book("An incomplete book", 7, 50)
        self.assertEqual(25,
                         self.goal.minimum_pages_needed(self.goal.books[1]))

    def test_minimumPages_nextDayProgress_returnsProgressForOneDay(self):
        self.goal.book_goal = 183
        self.goal.start_date = "2020-01-01"
        self.goal.end_date = "2021-01-01"
        self.goal += Book("1 book finished", 100, 100)
        self.goal += Book("Next book unfinished", 237, 700)
        self.assertEqual(350, self.goal.minimum_pages_needed(
            self.goal.books[1], force_next_day=True))
