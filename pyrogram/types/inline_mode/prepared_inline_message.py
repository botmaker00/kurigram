#  Pyrogram - Telegram MTProto API Client Library for Python
#  Copyright (C) 2017-present Dan <https://github.com/delivrance>
#
#  This file is part of Pyrogram.
#
#  Pyrogram is free software: you can redistribute it and/or modify
#  it under the terms of the GNU Lesser General Public License as published
#  by the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  Pyrogram is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU Lesser General Public License for more details.
#
#  You should have received a copy of the GNU Lesser General Public License
#  along with Pyrogram.  If not, see <http://www.gnu.org/licenses/>.

from datetime import datetime
from typing import Union

from ..object import Object


class PreparedInlineMessage(Object):
    """Describes an inline message to be sent by a user of a Mini App.

    Source: https://core.telegram.org/bots/api#preparedinlinemessage

    Parameters:
        id (``str``):
            Unique identifier of the prepared message.

        expiration_date (``int`` | :py:obj:`~datetime.datetime`):
            Expiration date of the prepared message.
    """

    def __init__(self, id: str, expiration_date: Union[int, datetime]):
        super().__init__()
        self.id = str(id)
        self.expiration_date = expiration_date

    def __repr__(self) -> str:
        return f"PreparedInlineMessage(id={self.id!r}, expiration_date={self.expiration_date!r})"
