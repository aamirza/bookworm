"""
The Audiobook class is for representing books whose length is measured
in seconds.
"""

import datetime
from typing import Union, Optional

from audiobookseconds import AudiobookSeconds
from lib.ibook import iBook
from format import Format


class Audiobook(iBook):
    def __init__(self,
                 title: str,
                 time_listened: Union[int, str],
                 total_time: Union[int, str],
                 start_date: Optional[datetime.datetime] = datetime.datetime.
                 today(),
                 id_num: Optional[int] = 0
                 ):
        super().__init__(Format.AUDIOBOOK, title,
                         AudiobookSeconds(time_listened),
                         AudiobookSeconds(total_time), start_date, id_num)

    def __repr__(self):
        """Overridden so that pages read is shown in HH:MM:SS format."""
        return f"{__class__.__name__}({self.title}, {self.pages_read}, " \
               f"{self.total_pages})"
