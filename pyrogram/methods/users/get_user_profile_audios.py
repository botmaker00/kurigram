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

from typing import Optional, Union

import pyrogram
from pyrogram import types


class GetUserProfileAudios:
    async def get_user_profile_audios(
        self: "pyrogram.Client",
        user_id: Union[int, str],
        offset: Optional[int] = 0,
        limit: Optional[int] = 100,
    ) -> "types.UserProfileAudios":
        """Get a list of profile audios for a user.

        Source: https://core.telegram.org/bots/api#getuserprofileaudios

        Parameters:
            user_id (``int`` | ``str``):
                Unique identifier of the target user.

            offset (``int``, *optional*):
                Sequential number of the first audio to be returned.

            limit (``int``, *optional*):
                Limits the number of audios to be retrieved (1-100). Defaults to 100.

        Returns:
            :obj:`~pyrogram.types.UserProfileAudios`: On success, a UserProfileAudios object is returned.
        """
        audios = []
        count = 0
        try:
            async for audio in self.get_chat_audios(chat_id=user_id, limit=limit or 100):
                if count >= (offset or 0):
                    audios.append(audio)
                count += 1
                if len(audios) >= (limit or 100):
                    break
        except Exception:
            pass

        return types.UserProfileAudios(
            client=self,
            total_count=count,
            audios=audios
        )
