"""Enum class for book formats (books, ebooks, audiobooks, etc.)"""

from enum import Enum


class Format(Enum):
    """Represents the various formats that a book can come in."""
    BOOK = 0
    EBOOK = 1
    AUDIOBOOK = 2
