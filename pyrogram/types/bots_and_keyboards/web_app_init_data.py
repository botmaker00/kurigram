#  Kurigram - Telegram MTProto API Client Library for Python
#  Copyright (C) 2017-present Dan <https://github.com/delivrance>
#
#  This file is part of Kurigram.
#
#  Kurigram is free software: you can redistribute it and/or modify
#  it under the terms of the GNU Lesser General Public License as published
#  by the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  Kurigram is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU Lesser General Public License for more details.
#
#  You should have received a copy of the GNU Lesser General Public License
#  along with Kurigram.  If not, see <http://www.gnu.org/licenses/>.

from datetime import datetime
from typing import Optional, Union, Any

from pyrogram import types, utils
from ..object import Object


class WebAppInitData(Object):
    """Contains data that is passed to a Web App when it is opened.

    Parameters:
        query_id (``str``, *optional*):
            A unique identifier for the Web App session, required for sending messages via answerWebAppQuery.

        user (:obj:`~pyrogram.types.User`, *optional*):
            An object containing data about the current user.

        receiver (:obj:`~pyrogram.types.User`, *optional*):
            An object containing data about the chat partner of the current user.

        chat (:obj:`~pyrogram.types.Chat`, *optional*):
            An object containing data about the chat where the bot was launched via the attachment menu.

        chat_type (``str``, *optional*):
            Type of the chat from which the Web App was opened.

        chat_instance (``str``, *optional*):
            Global identifier, uniquely corresponding the chat from which the Web App was opened.

        start_param (``str``, *optional*):
            The value of the startattach parameter, passed via link.

        can_send_after (``int``, *optional*):
            Time in seconds, after which a message can be sent via the answerWebAppQuery method.

        auth_date (:py:obj:`~datetime.datetime`, *optional*):
            Unix time when the form was opened.

        hash (``str``, *optional*):
            A signature of all other fields to verify their authenticity.

        signature (``str``, *optional*):
            A signature of all other fields to verify their authenticity.

        chat_join_request_query_id (``str``, *optional*):
            A unique identifier of the chat join request query, if the Web App was opened from a chat join request.
    """

    def __init__(
        self,
        *,
        query_id: Optional[str] = None,
        user: Optional["types.User"] = None,
        receiver: Optional["types.User"] = None,
        chat: Optional["types.Chat"] = None,
        chat_type: Optional[str] = None,
        chat_instance: Optional[str] = None,
        start_param: Optional[str] = None,
        can_send_after: Optional[int] = None,
        auth_date: Optional[Union[datetime, int]] = None,
        hash: Optional[str] = None,
        signature: Optional[str] = None,
        chat_join_request_query_id: Optional[str] = None,
    ):
        super().__init__()

        self.query_id = query_id
        self.user = user
        self.receiver = receiver
        self.chat = chat
        self.chat_type = chat_type
        self.chat_instance = chat_instance
        self.start_param = start_param
        self.can_send_after = can_send_after
        self.auth_date = utils.timestamp_to_datetime(auth_date) if isinstance(auth_date, int) else auth_date
        self.hash = hash
        self.signature = signature
        self.chat_join_request_query_id = chat_join_request_query_id

    @staticmethod
    def _parse(client=None, data=None):
        if not data:
            return None
        if isinstance(data, WebAppInitData):
            return data
        if isinstance(data, dict):
            return WebAppInitData(
                query_id=data.get("query_id"),
                user=types.User._parse(client, data["user"]) if "user" in data else None,
                receiver=types.User._parse(client, data["receiver"]) if "receiver" in data else None,
                chat=types.Chat._parse_chat(client, data["chat"]) if "chat" in data else None,
                chat_type=data.get("chat_type"),
                chat_instance=data.get("chat_instance"),
                start_param=data.get("start_param"),
                can_send_after=data.get("can_send_after"),
                auth_date=data.get("auth_date"),
                hash=data.get("hash"),
                signature=data.get("signature"),
                chat_join_request_query_id=data.get("chat_join_request_query_id"),
            )
        return None

    @staticmethod
    def read(b, client=None):
        return WebAppInitData._parse(client, b)
