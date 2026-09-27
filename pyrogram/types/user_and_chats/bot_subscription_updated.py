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
from pyrogram import types
from ..object import Object


class BotSubscriptionUpdated(Object):
    """Contains information about changes to a user payment subscription toward the current bot.

    Parameters:
        user (:obj:`~pyrogram.types.User`):
            User who subscribed for payments toward the bot.

        invoice_payload (``str``):
            Bot-specified invoice payload.

        state (``str``):
            The new state of the subscription. Currently, it can be one of 'canceled' if the user canceled
            the subscription, 'active' if the user re-enabled a previously canceled subscription,
            or 'failed' if payment for the subscription failed.
    """

    def __init__(
        self,
        *,
        client: "pyrogram.Client" = None,
        user: "types.User" = None,
        invoice_payload: str = "",
        state: str = "",
    ):
        super().__init__(client)

        self.user = user
        self.invoice_payload = invoice_payload
        self.state = state
