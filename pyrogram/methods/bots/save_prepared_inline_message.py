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


class SavePreparedInlineMessage:
    async def save_prepared_inline_message(
        self: "pyrogram.Client",
        user_id: Union[int, str],
        result: "types.InlineQueryResult",
        allow_user_chats: Optional[bool] = None,
        allow_bot_chats: Optional[bool] = None,
        allow_group_chats: Optional[bool] = None,
        allow_channel_chats: Optional[bool] = None,
    ) -> "types.PreparedInlineMessage":
        """Stores a message that can be sent by a user of a Mini App.

        Parameters:
            user_id (``int`` | ``str``):
                Unique identifier of the target user that can use the prepared message.

            result (:obj:`~pyrogram.types.InlineQueryResult`):
                An InlineQueryResult object describing the message to be sent.

            allow_user_chats (``bool``, *optional*):
                Pass True if the message can be sent to private chats with users.

            allow_bot_chats (``bool``, *optional*):
                Pass True if the message can be sent to private chats with bots.

            allow_group_chats (``bool``, *optional*):
                Pass True if the message can be sent to group and supergroup chats.

            allow_channel_chats (``bool``, *optional*):
                Pass True if the message can be sent to channel chats.

        Returns:
            :obj:`~pyrogram.types.PreparedInlineMessage`: On success, the prepared message object is returned.
        """
        peer_types = []
        if allow_user_chats:
            peer_types.append(raw.types.InlineQueryPeerTypeSameBotPM())
        if allow_bot_chats:
            peer_types.append(raw.types.InlineQueryPeerTypeBotPM())
        if allow_group_chats:
            peer_types.extend([raw.types.InlineQueryPeerTypeChat(), raw.types.InlineQueryPeerTypeMegagroup()])
        if allow_channel_chats:
            peer_types.append(raw.types.InlineQueryPeerTypeBroadcast())

        raw_result = await result.write(self) if hasattr(result, "write") else result

        r = await self.invoke(
            raw.functions.messages.SavePreparedInlineMessage(
                user_id=await self.resolve_peer(user_id),
                result=raw_result,
                peer_types=peer_types or None
            )
        )
        return types.PreparedInlineMessage(
            id=str(getattr(r, "id", self.rnd_id())),
            expiration_date=getattr(r, "date", 0)
        )
