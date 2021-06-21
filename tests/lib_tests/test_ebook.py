import unittest

from lib.ebook import Ebook, InvalidPercentageError

"""
Naming convention: test_functionName_input/TestState_expectedResult
"""


class MyTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.ebook = Ebook("What a wonderful world", 73)

    def test_pagesRead_getsPagesRead(self) -> None:
        self.assertEqual(73, self.ebook.pages_read)

    def test_percentComplete(self) -> None:
        self.assertEqual(0.73, self.ebook.percent_complete)

    def test_setTotalPages_raisesInvalidPercentageError(self):
        with self.assertRaisesRegex(InvalidPercentageError,
                                    "E-Book total pages cannot be any number "
                                    "other than 100 per cent"):
            self.ebook.total_pages = 122

    def test_setPagesRead_moreThan100Pages_raisesInvalidPercentageError(self):
        with self.assertRaisesRegex(ValueError,
                                    "What a wonderful world is only 100 pages"
                                    " long, your value should be less than "
                                    "that."):
            self.ebook.pages_read = 107


if __name__ == '__main__':
    unittest.main()
