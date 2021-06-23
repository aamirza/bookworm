"""
Child of parser.py

This is the command line arguments for adding, updating, deleting books, and other things to do with books.
"""
import argparse

from database.books import Books as Books_db
from cli import validate
from lib.ibook import iBook


def add_book(args):
    """
    Parser for adding a book.

    :param args: The command-line args passed from Parser.
    :return: None, adds book to database.
    """
    parser = argparse.ArgumentParser("Bookworm add book")
    parser.add_argument("-f", "-format", default="book", dest="format",
                        type=validate.book_format,
                        help="What format the book is in. Possible choices: "
                             "book (b), audiobook (ab), ebook (eb).")
    parser.add_argument("title", type=str, help="Title of the book.")
    parser.add_argument("pages_read", type=validate.book_pages,
                        help="How many pages of the book you have read. "
                             "It can be an integer, percentage (for e-books), "
                             "or in the format H:MM:SS (for audiobooks).")
    parser.add_argument("total_pages", type=validate.book_pages,
                        help="How many pages a book has. It can be an integer"
                             ", or in the format H:MM:SS. Ignored if adding "
                             "an ebook.")
    book_args = parser.parse_args(args)
    book = validate.book(book_args.title, book_args.pages_read,
                         book_args.total_pages, book_args.format)
    add_book_to_database(book)


def add_book_to_database(book: iBook):
    db = Books_db()
    db.add_book(book)
    # TODO: Put this in the database package


def update_book(args):
    """Parser for updating a book"""
    parser = argparse.ArgumentParser("Bookworm update book")
    parser.add_argument("id", default=0, type=int,
                        help="The ID of the book you're tryng to update. The"
                             " number is beside the book title.")
    parser.add_argument("pages_read", type=validate.book_pages,
                        help="How many pages you have read of the book.")
    book_args = parser.parse_args(args)

    books_db = Books_db()
    selected_book = books_db.get_book_by_id(book_args.id)

    if selected_book is not None:
        selected_book = validate.book(selected_book.title,
                                      book_args.pages_read,
                                      selected_book.total_pages,
                                      selected_book.format)
        books_db.update_pages_read(selected_book, book_args.pages_read)
    # TODO: Refactor updating book into its own function and put it in database package
