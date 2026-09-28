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
from pyrogram import enums, raw, types


class EditEphemeralMessageText:
    async def edit_ephemeral_message_text(
        self: "pyrogram.Client",
        chat_id: Union[int, str],
        receiver_user_id: int,
        ephemeral_message_id: int,
        text: Optional[str] = None,
        rich_message: Optional[Union["types.InputRichMessage", str, "raw.base.InputRichMessage"]] = None,
        parse_mode: Optional["enums.ParseMode"] = None,
        entities: Optional[List["types.MessageEntity"]] = None,
        link_preview_options: Optional["types.LinkPreviewOptions"] = None,
        reply_markup: Optional["types.InlineKeyboardMarkup"] = None,
    ) -> bool:
        """Edit an ephemeral text message.

        Note that it is not guaranteed that the user will receive the message edit event,
        especially if they are offline. On success, True is returned.

        Parameters:
            chat_id (``int`` | ``str``):
                Unique identifier for the target chat or username of the target supergroup.

            receiver_user_id (``int``):
                Identifier of the user who received the message.

            ephemeral_message_id (``int``):
                Identifier of the ephemeral message to edit.

            text (``str``, *optional*):
                New text of the message, 1-4096 characters after entity parsing.
                Exactly one of text or rich_message must be specified.

            rich_message (:obj:`~pyrogram.types.InputRichMessage` | ``str``, *optional*):
                Describes the new rich formatted message.
                Exactly one of text or rich_message must be specified.

            parse_mode (:obj:`~pyrogram.enums.ParseMode`, *optional*):
                Mode for parsing entities in the message text.

            entities (List of :obj:`~pyrogram.types.MessageEntity`, *optional*):
                Special entities that appear in message text.

            link_preview_options (:obj:`~pyrogram.types.LinkPreviewOptions`, *optional*):
                Link preview generation options for the message.

            reply_markup (:obj:`~pyrogram.types.InlineKeyboardMarkup`, *optional*):
                An inline keyboard markup.

        Returns:
            ``bool``: True on success.
        """
        r = await self.edit_message_text(
            chat_id=chat_id,
            message_id=ephemeral_message_id,
            text=text,
            parse_mode=parse_mode,
            entities=entities,
            link_preview_options=link_preview_options,
            reply_markup=reply_markup,
            rich_message=rich_message,
        )
        return bool(r)
