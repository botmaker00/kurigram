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
from pyrogram import raw, types


class GetStarTransactions:
    async def get_star_transactions(
        self: "pyrogram.Client",
        offset: Optional[str] = "",
        limit: Optional[int] = 100,
    ) -> "types.StarTransactions":
        """Returns the bot's Telegram Star transactions in chronological order.

        Parameters:
            offset (``str``, *optional*):
                Number of transactions to skip in the response.

            limit (``int``, *optional*):
                The maximum number of transactions to be retrieved (1-100). Defaults to 100.

        Returns:
            :obj:`~pyrogram.types.StarTransactions`: On success, the transactions object is returned.
        """
        r = await self.invoke(
            raw.functions.payments.GetStarsTransactions(
                peer=raw.types.InputPeerSelf(),
                offset=str(offset or ""),
                limit=limit or 100
            )
        )
        transactions = []
        for t in getattr(r, "history", []):
            transactions.append(
                types.StarTransaction(
                    id=str(getattr(t, "id", "")),
                    amount=getattr(t, "stars", 0),
                    date=getattr(t, "date", 0),
                    nanostar_amount=getattr(t, "nanostar_amount", None)
                )
            )
        return types.StarTransactions(transactions=transactions)
