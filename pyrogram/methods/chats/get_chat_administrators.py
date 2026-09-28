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

from typing import List, Optional, Union

import pyrogram
from pyrogram import raw, types


class GetChatAdministrators:
    async def get_chat_administrators(
        self: "pyrogram.Client",
        chat_id: Union[int, str],
        return_bots: Optional[bool] = None,
    ) -> List["types.ChatMember"]:
        """Get a list of administrators in a chat.

        .. include:: /_includes/usable-by/users-bots.rst

        Parameters:
            chat_id (``int`` | ``str``):
                Unique identifier (int) or username (str) of the target chat.

            return_bots (``bool``, *optional*):
                Pass True to also return bot administrators in the list.
                Bot API 10.0+.

        Returns:
            List of :obj:`~pyrogram.types.ChatMember`: List of administrators.

        Example:
            .. code-block:: python

                admins = await app.get_chat_administrators(chat_id)
                for admin in admins:
                    print(admin.user.first_name)
        """
        from pyrogram import enums

        async def generator():
            async for member in self.get_chat_members(
                chat_id=chat_id,
                filter=enums.ChatMembersFilter.ADMINISTRATORS,
            ):
                yield member

        return [member async for member in generator()]
