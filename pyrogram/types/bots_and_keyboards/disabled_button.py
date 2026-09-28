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
from pyrogram import raw
from ..object import Object


class DisabledButton(Object):
    """Describes a disabled button in an inline keyboard.

    Source: https://core.telegram.org/bots/api#disabledbutton

    Parameters:
        text (``str``, *optional*):
            Label text on the button.
    """

    def __init__(self, text: str = ""):
        super().__init__()
        self.text = text

    async def write(self, client: "pyrogram.Client" = None) -> "raw.base.KeyboardButton":
        return raw.types.KeyboardButton(text=self.text)

    @staticmethod
    def read(b: "raw.base.KeyboardButton") -> "DisabledButton":
        return DisabledButton(text=getattr(b, "text", ""))
