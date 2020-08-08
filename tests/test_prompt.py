from unittest import TestCase

from cli import PromptBook

"""
Test naming convention:
test_nameOfTestedFeature_expectedInput/testState_expectedBehaviour
"""

# TODO: Write these tests
"""
* Create a SQL database to store books
* Be able to create, read, update and delete books.
** With Python mocking that should be easiers 

We're going to be using SQLite to store our books. Ready? 
I say don't worry too much about testing, although we could watch videos about
that somewhere.
"""


class TestPrompt(TestCase):
    def setUp(self) -> None:
        self.prompt = PromptBook.PromptBook()

    def test_getOptions_returnsIndexedOptions(self):
        # CRUD: Create, read, update, delete
        self.prompt.options = [
            ["Add book", self.prompt.add_book],
            ["List all books", self.prompt.list_books],
            ["Update reading progress", self.prompt.update_book],
            ["Delete book", self.prompt.delete_book]
        ]
        self.assertEqual("\n[1] Add book\n[2] List all books\n"
                         "[3] Update reading progress\n[4] Delete book\n",
                         self.prompt.get_options())

    def test_getOptions_emptyOptionList_returnsMessage(self):
        self.prompt.options = []
        self.assertEqual("You have no options!", self.prompt.get_options())

    def test_runOption_passingAnIndex_runsOptionsFunction(self):
        self.prompt.options = [
            ["Add book", self.prompt.add_book],
            ["List all books", self.prompt.list_books],
            ["Update reading progress", self.prompt.update_book],
            ["Delete book", self.prompt.delete_book]
        ]
        self.assertEqual(self.prompt.list_books, self.prompt.run_option(1))
