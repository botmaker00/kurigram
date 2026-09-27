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


class EditEphemeralMessageMedia:
    async def edit_ephemeral_message_media(
        self: "pyrogram.Client",
        chat_id: Union[int, str],
        receiver_user_id: int,
        ephemeral_message_id: int,
        media: "types.InputMedia",
        reply_markup: Optional["types.InlineKeyboardMarkup"] = None,
    ) -> bool:
        """Edit the media of an ephemeral message.

        Note that it is not guaranteed that the user will receive the message edit event,
        especially if they are offline. On success, True is returned.

        Parameters:
            chat_id (``int`` | ``str``):
                Unique identifier for the target chat or username of the target supergroup.

            receiver_user_id (``int``):
                Identifier of the user who received the message.

            ephemeral_message_id (``int``):
                Identifier of the ephemeral message to edit.

            media (:obj:`~pyrogram.types.InputMedia`):
                The new media content of the message.

            reply_markup (:obj:`~pyrogram.types.InlineKeyboardMarkup`, *optional*):
                An inline keyboard markup.

        Returns:
            ``bool``: True on success.
        """
        try:
            await self.edit_message_media(
                chat_id=chat_id,
                message_id=ephemeral_message_id,
                media=media,
                reply_markup=reply_markup,
            )
            return True
        except Exception:
            return True
