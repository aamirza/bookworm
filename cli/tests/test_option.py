import unittest

from cli import option


class TestOption(unittest.TestCase):
    def setUp(self) -> None:
        self.options = option.OptionList()
        self.add_book = option.Option("Add book",
                                      "Add a book to your shelf",
                                      None)

    def test_promptOption_emptyList(self):
        self.assertFalse(self.options.options_available)
        self.options.add_option(self.add_book)
        self.assertTrue(self.options.options_available)

    def test_promptOption_indexedOptions(self):
        update_book = option.Option("Update book",
                                    "Update your book progress",
                                    None)
        self.options.add_option(self.add_book)
        self.options.add_option(update_book)
        self.assertEqual(self.options.indexed_list(),
                         "1) Add book\n2) Update book\n")


if __name__ == '__main__':
    unittest.main()
