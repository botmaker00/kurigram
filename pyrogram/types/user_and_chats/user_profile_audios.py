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

from typing import List, Optional

import pyrogram
from pyrogram import types
from ..object import Object


class UserProfileAudios(Object):
    """This object represents the audios displayed on a user's profile.

    Source: https://core.telegram.org/bots/api#userprofileaudios

    Parameters:
        total_count (``int``):
            Total number of profile audios for the target user.

        audios (List of :obj:`~pyrogram.types.Audio`):
            Requested profile audios.
    """

    def __init__(
        self,
        *,
        client: "pyrogram.Client" = None,
        total_count: int,
        audios: List["types.Audio"]
    ):
        super().__init__(client)
        self.total_count = total_count
        self.audios = audios

    def __repr__(self) -> str:
        return f"UserProfileAudios(total_count={self.total_count}, count={len(self.audios)})"
