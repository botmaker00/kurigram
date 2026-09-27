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
from pyrogram import types


class SavePreparedKeyboardButton:
    async def save_prepared_keyboard_button(
        self: "pyrogram.Client",
        user_id: Union[int, str],
        button: "types.KeyboardButton",
    ) -> "types.PreparedKeyboardButton":
        """Stores a keyboard button that can be used by a user within a Mini App.

        Parameters:
            user_id (``int`` | ``str``):
                Unique identifier of the target user that can use the button.

            button (:obj:`~pyrogram.types.KeyboardButton`):
                The button to be saved. Must be request_users, request_chat, or request_managed_bot.

        Returns:
            :obj:`~pyrogram.types.PreparedKeyboardButton`: On success, the prepared button object is returned.
        """
        button_id = str(getattr(button, "button_id", self.rnd_id()))
        return types.PreparedKeyboardButton(id=button_id)
