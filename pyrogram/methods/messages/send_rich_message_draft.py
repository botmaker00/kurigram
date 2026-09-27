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
from pyrogram import raw, types


class SendRichMessageDraft:
    async def send_rich_message_draft(
        self: "pyrogram.Client",
        chat_id: Union[int, str],
        draft_id: int,
        rich_message: Union["types.InputRichMessage", str, "raw.base.InputRichMessage"],
        message_thread_id: Optional[int] = None,
        can_stop: Optional[bool] = None,
        keep_on_stop: Optional[bool] = None,
    ) -> bool:
        """Stream a partial rich message to a user while the message is being generated.

        Parameters:
            chat_id (``int`` | ``str``):
                Unique identifier for the target private chat.

            draft_id (``int``):
                Unique identifier of the message draft; must be non-zero.

            rich_message (:obj:`~pyrogram.types.InputRichMessage` | ``str``):
                The partial message to be streamed.

            message_thread_id (``int``, *optional*):
                Unique identifier for the target message thread.

            can_stop (``bool``, *optional*):
                Pass True if the user can stop the generation of the message draft.

            keep_on_stop (``bool``, *optional*):
                Pass True if the message draft must not be hidden when the user stops the generation.

        Returns:
            ``bool``: On success, True is returned.
        """
        raw_rich = rich_message
        is_rtl = None
        skip_entity_detection = None
        if isinstance(rich_message, types.InputRichMessage):
            is_rtl = rich_message.is_rtl
            skip_entity_detection = rich_message.skip_entity_detection
            if rich_message.markdown:
                raw_rich = rich_message.markdown
            elif rich_message.html:
                raw_rich = rich_message.html
            else:
                raw_rich = rich_message

        return await self.send_message_draft(
            chat_id=chat_id,
            draft_id=draft_id,
            rich_message=raw_rich,
            message_thread_id=message_thread_id,
            is_rtl=is_rtl,
            skip_entity_detection=skip_entity_detection,
            can_stop=can_stop,
            keep_on_stop=keep_on_stop,
        )
