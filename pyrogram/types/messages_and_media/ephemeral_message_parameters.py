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

from typing import Optional

import pyrogram
from ..object import Object


class EphemeralMessageParameters(Object):
    """Describes parameters of an ephemeral message.

    Parameters:
        receiver_user_id (``int``, *optional*):
            Unique identifier of the user who will receive the message; for group and supergroup chats only.
            It is not guaranteed that the user will receive the message, especially if they are offline.

        callback_query_id (``str``, *optional*):
            Identifier of the callback query which triggered the message if any.

        replace_callback_query_message (``bool``, *optional*):
            Pass True to replace the message to which the callback query was attached with the ephemeral message.
    """

    def __init__(
        self,
        *,
        receiver_user_id: Optional[int] = None,
        callback_query_id: Optional[str] = None,
        replace_callback_query_message: Optional[bool] = None,
    ):
        super().__init__()

        self.receiver_user_id = receiver_user_id
        self.callback_query_id = callback_query_id
        self.replace_callback_query_message = replace_callback_query_message
