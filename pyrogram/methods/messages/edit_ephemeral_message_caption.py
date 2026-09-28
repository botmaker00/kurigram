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
from pyrogram import enums, types


class EditEphemeralMessageCaption:
    async def edit_ephemeral_message_caption(
        self: "pyrogram.Client",
        chat_id: Union[int, str],
        receiver_user_id: int,
        ephemeral_message_id: int,
        caption: Optional[str] = None,
        parse_mode: Optional["enums.ParseMode"] = None,
        caption_entities: Optional[List["types.MessageEntity"]] = None,
        show_caption_above_media: Optional[bool] = None,
        reply_markup: Optional["types.InlineKeyboardMarkup"] = None,
    ) -> bool:
        """Edit the caption of an ephemeral message.

        Note that it is not guaranteed that the user will receive the message edit event,
        especially if they are offline. On success, True is returned.

        Parameters:
            chat_id (``int`` | ``str``):
                Unique identifier for the target chat or username of the target supergroup.

            receiver_user_id (``int``):
                Identifier of the user who received the message.

            ephemeral_message_id (``int``):
                Identifier of the ephemeral message to edit.

            caption (``str``, *optional*):
                New caption of the message, 0-1024 characters after entities parsing.

            parse_mode (:obj:`~pyrogram.enums.ParseMode`, *optional*):
                Mode for parsing entities in the message caption.

            caption_entities (List of :obj:`~pyrogram.types.MessageEntity`, *optional*):
                Special entities that appear in the caption.

            show_caption_above_media (``bool``, *optional*):
                Pass True, if the caption must be shown above the message media.

            reply_markup (:obj:`~pyrogram.types.InlineKeyboardMarkup`, *optional*):
                An inline keyboard markup.

        Returns:
            ``bool``: True on success.
        """
        r = await self.edit_message_caption(
            chat_id=chat_id,
            message_id=ephemeral_message_id,
            caption=caption,
            parse_mode=parse_mode,
            caption_entities=caption_entities,
            show_caption_above_media=show_caption_above_media,
            reply_markup=reply_markup,
        )
        return bool(r)
