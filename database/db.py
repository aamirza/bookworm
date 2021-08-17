"""
Base class for interacting with the database.
"""

import datetime
import os
import sqlite3
import time

DB_ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
SHELF_DB_PATH = os.path.join(DB_ROOT_DIR, 'shelf.db')


class db:
    """Base class for the database interface."""
    def __init__(self, db_name=SHELF_DB_PATH):
        self.conn: sqlite3.Connection = sqlite3.connect(db_name)
        self.c: sqlite3.Cursor = self.conn.cursor()
        with self.conn:
            self.create_tables()

    def __del__(self):
        self.c.close()
        self.conn.commit()
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
            id              integer     PRIMARY KEY AUTOINCREMENT,
            format_name     text        NOT NULL UNIQUE
        );""")

        self.c.execute("""
        INSERT OR IGNORE INTO formats (id, format_name)
        VALUES 
            (0, "BOOK"), 
            (1, "EBOOK"), 
            (2, "AUDIOBOOK")
        ;""")

        self.c.execute("""
        CREATE TABLE IF NOT EXISTS books (
            id              integer     PRIMARY KEY AUTOINCREMENT,
            format_id       integer     NOT NULL,
            title           text        NOT NULL UNIQUE,
            total_pages     integer     NOT NULL,
            FOREIGN KEY (format_id)
                REFERENCES formats(id)
        );""")

        self.c.execute("""
        CREATE TABLE IF NOT EXISTS goals (
            id          integer     PRIMARY KEY AUTOINCREMENT,
            book_goal   integer     NOT NULL,
            start_date  integer     NOT NULL DEFAULT (strftime('%s', 'now')),
            end_date    integer     NOT NULL,
            active      integer     NOT NULL DEFAULT 1
            CHECK (start_date < end_date),
            CHECK (book_goal > 0),
            CHECK (active BETWEEN 0 and 1)
        );""")


        self.c.execute("""
        CREATE TABLE IF NOT EXISTS goalbooks (
            goal_id     integer,
            book_id     integer,
            pages_read  integer     NOT NULL DEFAULT 0,
            start_date  integer     NOT NULL DEFAULT (strftime('%s', 'now')),
            end_date    integer,
            FOREIGN KEY (goal_id) 
                REFERENCES goals(goal_id)
                ON DELETE CASCADE,
            FOREIGN KEY (book_id) 
                REFERENCES books(book_id)
                ON DELETE CASCADE,
            PRIMARY KEY (goal_id, book_id)
        );""")

    @staticmethod
    def _date_to_unix_timestamp(date: datetime.date):
        """To store datetimes as UNIX timestamps in the database."""
        return time.mktime(date.timetuple())

    def active_goal_exists(self):
        self.c.execute("""
        SELECT *
        FROM goals
        WHERE active = 1 AND end_date > ?
        """, (time.time(),))
        return len(self.c.fetchall()) == 1

    def get_all_tables(self) -> list:
        tables = self.c.execute(
            "SELECT name FROM sqlite_master WHERE type='table';")
        return [table[0] for table in tables]
