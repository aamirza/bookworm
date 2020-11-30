import argparse

import validate


def parse(args):
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
    parser.add_argument("total_pages", type=validate.book_pages, default=100,
                        nargs="?",
                        help="How many pages a book has. It can be an integer"
                             ", or in the format H:MM:SS. Ignored if adding "
                             "an ebook.")
    book_args = parser.parse_args(args)