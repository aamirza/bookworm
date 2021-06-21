import unittest

from lib.ibook import PagesReadError
from lib.audiobook import Audiobook
from lib.audiobookseconds import TimeFormatError

"""
Makes tests for:

"""


class MyTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.audiobook = Audiobook("Something from Audible", "1:43:44",
                                   "21:22:38")

    def test_pagesRead_timeString_convertsToSeconds(self):
        self.assertEqual(self.audiobook.pages_read, 6224)

    def test_totalPages_timeString_convertsToSeconds(self):
        self.assertEqual(self.audiobook.total_pages, 76958)

    def test_pagesReadStr_returnsString(self):
        self.assertEqual(str(self.audiobook.pages_read), "1:43:44")

    def test_totalPagesStr_returnsString(self):
        self.assertEqual(str(self.audiobook.total_pages), "21:22:38")

    def test_invalidTimeFormat_raisesError(self):
        with self.assertRaisesRegex(TimeFormatError,
                                    "Audiobook length format should be in "
                                    "H:M:S or M:S"):
            Audiobook("How to write time", "14:2:14", "19:22:14")

    def test_init_timeReadLongerThanLength_raisesAssertionError(self):
        with self.assertRaisesRegex(PagesReadError,
                                    "Total pages cannot be less than pages "
                                    "read."):
            newAudiobook = Audiobook("Bending space and time",
                                     "13:21:41",
                                     "11:50:33")

    def test_repr_isFormattedProperly(self):
        self.assertEqual(
            'Audiobook(Something from Audible, 1:43:44, 21:22:38)',
            repr(self.audiobook))


if __name__ == '__main__':
    unittest.main()
