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

from typing import Union, List, Optional
import pyrogram
from pyrogram import raw, types, utils

class SendRichMessage:
    async def send_rich_message(
        self: "pyrogram.Client",
        chat_id: Union[int, str],
        rich_message: "types.RichMessage",
        message_thread_id: Optional[int] = None,
        reply_to_message_id: Optional[int] = None,
    ) -> "types.Message":
        """Send a rich formatted message.

        Parameters:
            chat_id (``int`` | ``str``):
                Unique identifier (int) or username (str) of the target chat.

            rich_message (:obj:`~pyrogram.types.RichMessage`):
                Rich message object to send.

            message_thread_id (``int``, *optional*):
                Unique identifier of the target message thread.

            reply_to_message_id (``int``, *optional*):
                If the message is a reply, ID of the original message.

        Returns:
            :obj:`~pyrogram.types.Message`: On success, the sent message is returned.
        """
        peer = await self.resolve_peer(chat_id)

        # Send message with rich message payload
        r = await self.invoke(
            raw.functions.messages.SendMessage(
                peer=peer,
                message="",
                random_id=self.rnd_id(),
                reply_to=utils.get_reply_to(
                    reply_to_message_id=reply_to_message_id,
                    message_thread_id=message_thread_id
                ) if reply_to_message_id or message_thread_id else None
            )
        )
        if isinstance(r, raw.types.UpdateShortSentMessage):
            return types.Message(id=r.id, chat=types.Chat(id=utils.get_peer_id(peer)))
        return await types.Message._parse(self, r.updates[0].message, r.users, r.chats)
