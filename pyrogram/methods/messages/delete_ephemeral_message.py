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

from typing import Union

import pyrogram


class DeleteEphemeralMessage:
    async def delete_ephemeral_message(
        self: "pyrogram.Client",
        chat_id: Union[int, str],
        receiver_user_id: int,
        ephemeral_message_id: int,
    ) -> bool:
        """Delete an ephemeral message.

        Note that it is not guaranteed that the user will receive the message deletion event,
        especially if they are offline. Returns True on success.

        Parameters:
            chat_id (``int`` | ``str``):
                Unique identifier for the target chat or username of the target supergroup.

            receiver_user_id (``int``):
                Identifier of the user who received the message.

            ephemeral_message_id (``int``):
                Identifier of the ephemeral message to delete.

        Returns:
            ``bool``: True on success.
        """
        r = await self.delete_messages(
            chat_id=chat_id,
            message_ids=ephemeral_message_id,
            revoke=True,
        )
        return bool(r)
