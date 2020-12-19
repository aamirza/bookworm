import unittest

from cli import option


class TestOption(unittest.TestCase):
    def setUp(self) -> None:
        self.options = option.OptionList()
        self.add_book = option.Option("Add book",
                                      "Add a book to your shelf",
                                      None)
        self.update_book = option.Option("Update book",
                                         "Update your book progress",
                                         None)

    def test_promptOption_emptyList(self):
        self.assertFalse(self.options.options_available)
        self.options.add_option(self.add_book)
        self.assertTrue(self.options.options_available)

    def test_promptOption_IndexedOptions_printsOptions(self):
        self.options.add_option(self.add_book)
        self.options.add_option(self.update_book)
        self.assertEqual(self.options.indexed_list(),
                         "[1] Add book\n[2] Update book\n")

    def test_promptOption_emptyIndexedOptions_raisesError(self):
        with self.assertRaisesRegex(option.NoOptionsAvailableError,
                                    "There are no options in OptionsList"):
            self.options.indexed_list()

    def test_optionsIndex_startsAtOne(self):
        self.options.add_option(self.add_book)
        self.options.add_option(self.update_book)
        self.assertEqual(self.add_book, self.options[1])

    def test_optionsIndex_noZeroIndex(self):
        self.options.add_option(self.add_book)
        with self.assertRaises(IndexError):
            self.options[0]

if __name__ == '__main__':
    unittest.main()
