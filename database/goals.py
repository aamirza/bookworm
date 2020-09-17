from database.db import db


class Goals(db):
    def __init__(self, db_name="shelf.py"):
        super().__init__(db_name)
