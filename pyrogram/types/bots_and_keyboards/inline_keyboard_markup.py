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

from typing import List

import pyrogram
from pyrogram import raw
from pyrogram import types
from ..object import Object


class InlineKeyboardMarkup(Object):
    """An inline keyboard that appears right next to the message it belongs to.

    Parameters:
        inline_keyboard (List of List of :obj:`~pyrogram.types.InlineKeyboardButton`):
            List of button rows, each represented by a List of InlineKeyboardButton objects.

        force_reply (:obj:`~pyrogram.types.ForceReply`, *optional*):
            Instructions to force a reply from the user.
    """

    def __init__(
        self,
        inline_keyboard: List[List["types.InlineKeyboardButton"]],
        force_reply: "types.ForceReply" = None
    ):
        super().__init__()

        self.inline_keyboard = inline_keyboard
        self.force_reply = force_reply

    @staticmethod
    def read(o):
        inline_keyboard = []

        for i in o.rows:
            row = []

            for j in i.buttons:
                row.append(types.InlineKeyboardButton.read(j))

            inline_keyboard.append(row)

        force_reply = None
        raw_force = getattr(o, "force_reply", None)
        if raw_force is not None:
            if isinstance(raw_force, raw.types.ReplyKeyboardForceReply):
                force_reply = types.ForceReply.read(raw_force)
            elif isinstance(raw_force, types.ForceReply):
                force_reply = raw_force

        return InlineKeyboardMarkup(
            inline_keyboard=inline_keyboard,
            force_reply=force_reply
        )

    async def write(self, client: "pyrogram.Client" = None):
        rows = []

        for r in self.inline_keyboard:
            buttons = []

            for b in r:
                buttons.append(await b.write(client))

            rows.append(raw.types.KeyboardButtonRow(buttons=buttons))

        if self.force_reply:
            raise NotImplementedError("force_reply on InlineKeyboardMarkup requires a newer TL layer")
        return raw.types.ReplyInlineMarkup(rows=rows)

        # There seems to be a Python issues with nested async comprehensions.
        # See: https://bugs.python.org/issue33346
        #
        # return raw.types.ReplyInlineMarkup(
        #     rows=[raw.types.KeyboardButtonRow(
        #         buttons=[await j.write(client) for j in i]
        #     ) for i in self.inline_keyboard]
        # )
