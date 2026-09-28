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

from typing import Any, Optional

import pyrogram
from pyrogram import types
from ..object import Object


class MessageGenerationStopped(Object):
    """Describes an update about a stopped message generation.

    Parameters:
        chat (:obj:`~pyrogram.types.Chat`):
            Chat where the message generation was stopped.

        draft_id (``int``):
            Unique identifier of the message draft that was stopped.

        message_thread_id (``int``, *optional*):
            Identifier of the message thread.
    """

    def __init__(
        self,
        *,
        client: "pyrogram.Client" = None,
        chat: "types.Chat" = None,
        draft_id: int = 0,
        message_thread_id: Optional[int] = None,
    ):
        super().__init__(client)

        self.chat = chat
        self.draft_id = draft_id
        self.message_thread_id = message_thread_id

    @staticmethod
    def _parse(
        client: "pyrogram.Client" = None,
        update: Optional[Any] = None,
        users: Optional[dict] = None,
        chats: Optional[dict] = None,
    ) -> Optional["MessageGenerationStopped"]:
        if update is None:
            return None
        if isinstance(update, MessageGenerationStopped):
            return update
        from pyrogram import types
        chat_val = None
        draft_id = getattr(update, "draft_id", 0) or 0
        thread_id = getattr(update, "top_msg_id", None) or getattr(update, "message_thread_id", None)
        peer = getattr(update, "peer", None)
        if peer and chats:
            peer_id = getattr(peer, "channel_id", None) or getattr(peer, "chat_id", None) or getattr(peer, "user_id", None)
            if peer_id and peer_id in chats:
                chat_val = types.Chat._parse_chat(client, chats[peer_id])
        if not chat_val and isinstance(update, dict):
            c_dict = update.get("chat")
            chat_val = types.Chat._parse_chat(client, c_dict) if c_dict else None
            draft_id = update.get("draft_id", 0)
            thread_id = update.get("message_thread_id")
        return MessageGenerationStopped(
            client=client,
            chat=chat_val,
            draft_id=draft_id,
            message_thread_id=thread_id,
        )

    @staticmethod
    def read(b: Any, client: "pyrogram.Client" = None) -> Optional["MessageGenerationStopped"]:
        return MessageGenerationStopped._parse(client, b)
