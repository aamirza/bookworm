import datetime
import sqlite3
import time


class db:
    def __init__(self, db_name="shelf.db"):
        self.conn: sqlite3.Connection = sqlite3.connect(db_name)
        self.c: sqlite3.Cursor = self.conn.cursor()
        self.create_tables()

    def __del__(self):
        self.c.close()
        self.conn.close()

    def create_tables(self) -> None:
        '''
        Tables to create:
            * Formats
            * Books
            * Goals (start date, end date, book goal, active)
        '''

        self.c.execute("""
        CREATE TABLE IF NOT EXISTS formats (
            id          integer     PRIMARY KEY AUTOINCREMENT,
            format      text        NOT NULL UNIQUE
        );""")

        self.c.execute("""
        INSERT OR IGNORE INTO formats (id, format)
        VALUES 
            (0, "BOOK"), 
            (1, "EBOOK"), 
            (2, "AUDIOBOOK")
        ;""")

        self.c.execute("""
        CREATE TABLE IF NOT EXISTS books (
            book_id     integer     PRIMARY KEY AUTOINCREMENT,
            format      integer     NOT NULL,
            title       text        NOT NULL UNIQUE,
            pages_read  integer     DEFAULT 0,
            total_pages integer     NOT NULL,
            start_date  integer     NOT NULL DEFAULT (strftime('%s', 'now')),
            FOREIGN KEY (format)
                REFERENCES formats (id),
            CHECK (pages_read <= total_pages) 
        );""")

        self.c.execute("""
        CREATE TABLE IF NOT EXISTS goals (
            goal_id     integer     PRIMARY KEY AUTOINCREMENT,
            book_goal   integer     NOT NULL,
            start_date  integer     NOT NULL DEFAULT (strftime('%s', 'now')),
            end_date    integer     NOT NULL,
            creation_time integer   NOT NULL DEFAULT (strftime('%s', 'now'))
            CHECK (start_date < end_date),
            CHECK (book_goal > 0)
        );""")

        self.c.execute("""
        CREATE TABLE IF NOT EXISTS goalbooks (
            goal_id     integer     PRIMARY KEY,
            book_id     integer     PRIMARY KEY,
            pages_read  integer     NOT NULL DEFAULT 0,
            completion  integer     NOT NULL,
            FOREIGN KEY (goal_id) 
                REFERENCES goals(goal_id)
                ON DELETE CASCADE,
            FOREIGN KEY (book_id) 
                REFERENCES books(book_id)
                ON DELETE CASCADE,
            PRIMARY KEY (goal_id,book_id)
        );""")

    @staticmethod
    def _date_to_unix_timestamp(date: datetime.date):
        """To store datetimes as UNIX timestamps in the database."""
        return time.mktime(date.timetuple())
