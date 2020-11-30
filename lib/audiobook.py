import datetime
import re
from typing import Union, Optional

from lib.ibook import iBook, Format


class TimeFormatError(Exception):
    """Time format must be H:M:S, M:S or M:S"""
    pass


class AudiobookSeconds:
    def __init__(self, time):
        if type(time) == int:
            self.seconds = time
        elif self.is_valid_time_format(time):
            self.seconds = self.convert_string_to_seconds(time)
        else:
            raise TimeFormatError(
                "Audiobook length format should be in H:M:S or M:S")

    def __str__(self):
        return self.covert_seconds_to_string(self.seconds)

    def __int__(self):
        return self.seconds

    def __add__(self, value):
        return self.seconds + value

    def __sub__(self, value):
        return self.seconds - value

    def __mul__(self, value):
        return self.seconds * value

    def __truediv__(self, other):
        if type(other) == AudiobookSeconds:
            return self.seconds / other.seconds
        else:
            return self.seconds / other

    def __mod__(self, other):
        if type(other) == AudiobookSeconds:
            return self.seconds % other.seconds
        else:
            return self.seconds % other

    def __eq__(self, other):
        if type(other) == AudiobookSeconds:
            return self.seconds == other.seconds
        else:
            return self.seconds == other

    def __gt__(self, other):
        if type(other) == AudiobookSeconds:
            return self.seconds > other.seconds
        else:
            return self.seconds > other

    def __ge__(self, other):
        if type(other) == AudiobookSeconds:
            return self.seconds >= other.seconds
        else:
            return self.seconds >= other

    def __lt__(self, other):
        if type(other) == AudiobookSeconds:
            return self.seconds < other.seconds
        else:
            return self.seconds < other

    def __le__(self, other):
        if type(other) == AudiobookSeconds:
            return self.seconds <= other.seconds
        else:
            return self.seconds <= other

    @staticmethod
    def is_valid_time_format(string):
        valid_time_format = r'^(\d{1,2}:)?([0-5]\d):?([0-5]\d)$'
        return re.match(valid_time_format, string)

    @staticmethod
    def padded_time(hours, minutes, seconds):
        minutes = f"0{minutes}" if minutes < 10 else f"{minutes}"
        seconds = f"0{seconds}" if seconds < 10 else f"{seconds}"
        return f"{hours}:{minutes}:{seconds}"

    @classmethod
    def convert_string_to_seconds(cls, time_string):
        if cls.is_valid_time_format(time_string):
            time_units = [int(x) for x in time_string.split(":")]
            if len(time_units) < 3:
                time_units.index(0, 0)  # if hours are missing, add 0
            return (time_units[0] * 3600) + (time_units[1] * 60) + time_units[
                2]
        else:
            raise TimeFormatError(
                "Audiobook length format should be in H:M:S or M:S")

    @classmethod
    def covert_seconds_to_string(cls, seconds):
        hours = int(seconds / 3600)
        minutes = int((seconds / 60) % 60)
        seconds = seconds % 60
        return cls.padded_time(hours, minutes, seconds)


class Audiobook(iBook):
    def __init__(self,
                 title: str,
                 time_listened: Union[int, str],
                 total_time: Union[int, str],
                 start_date: Optional[datetime.datetime] = datetime.datetime.
                 today()
                 ):
        super().__init__(Format.AUDIOBOOK, title,
                         AudiobookSeconds(time_listened),
                         AudiobookSeconds(total_time), start_date)

    def __repr__(self):
        return f"{__class__.__name__}({self.title}, {self.pages_read}, " \
               f"{self.total_pages})"
