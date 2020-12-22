"""
AudiobookSeconds is a class that handles conversion from time represented
in HH:MM:SS to integer seconds so that mathematical calculations can be made.
"""

import re


class TimeFormatError(Exception):
    """Time format must be H:M:S or M:S"""
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

    def __round__(self):
        return AudiobookSeconds(round(self.seconds))

    @staticmethod
    def is_valid_time_format(string):
        """Checks if string is in the format HH:MM:SS or MM:SS"""
        valid_time_format = r'^(\d{1,2}:)?([0-5]\d):?([0-5]\d)$'
        return re.match(valid_time_format, string)

    @staticmethod
    def padded_time(hours, minutes, seconds):
        """Adds zeroes to time format HH:MM:SS where necessary.

        >>> AudiobookSeconds.padded_time(2, 3, 5)
        '2:03:05'
        """
        minutes = f"0{minutes}" if minutes < 10 else f"{minutes}"
        seconds = f"0{seconds}" if seconds < 10 else f"{seconds}"
        return f"{hours}:{minutes}:{seconds}"

    @classmethod
    def convert_string_to_seconds(cls, time_string):
        """Convert time in format HH:MM:SS or MM:SS into integer seconds"""
        if cls.is_valid_time_format(time_string):
            time_units = [int(x) for x in time_string.split(":")]
            # if hours are missing, set hours to 0
            if len(time_units) < 3: time_units.index(0, 0)

            hours, minutes, seconds = time_units[0], time_units[1], time_units[
                2]
            return (hours * 3600) + (minutes * 60) + seconds
        else:
            raise TimeFormatError(
                "Audiobook length format should be in H:M:S or M:S")

    @classmethod
    def covert_seconds_to_string(cls, seconds):
        hours = int(seconds / 3600)
        minutes = int((seconds / 60) % 60)
        seconds = seconds % 60
        return cls.padded_time(hours, minutes, seconds)
