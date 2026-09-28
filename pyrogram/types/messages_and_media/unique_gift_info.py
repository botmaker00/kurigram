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

from datetime import datetime
from typing import Any, List, Optional

import pyrogram
from pyrogram import raw, types
from ..object import Object


class UniqueGiftInfo(Object):
    """Describes a service message about a unique gift that was sent or received.

    Parameters:
        gift (:obj:`~pyrogram.types.Gift`, *optional*):
            Information about the gift.

        origin (``str``, *optional*):
            Origin of the gift. Currently, either 'upgrade' for gifts upgraded from regular gifts,
            'transfer' for gifts transferred from other users or channels, 'resale' for gifts bought
            from other users, 'gifted_upgrade' for upgrades purchased after the gift was sent,
            or 'offer' for gifts bought or sold through gift purchase offers.

        last_resale_currency (``str``, *optional*):
            For gifts bought from other users, the currency in which the payment for the gift was done.
            Currently, one of 'XTR' for Telegram Stars or 'TON' for TON grams.

        last_resale_amount (``int``, *optional*):
            For gifts bought from other users, the price paid for the gift in either Telegram Stars or nanograms.

        owned_gift_id (``str``, *optional*):
            Unique identifier of the received gift for the bot; only present for gifts received on behalf of business accounts.

        transfer_star_count (``int``, *optional*):
            Number of Telegram Stars that must be paid to transfer the gift; omitted if the bot cannot transfer the gift.

        next_transfer_date (:py:obj:`~datetime.datetime`, *optional*):
            Point in time when the gift can be transferred. If it is in the past, then the gift can be transferred now.

        text (``str``, *optional*):
            Text that was attached to the gift.

        entities (List of :obj:`~pyrogram.types.MessageEntity`, *optional*):
            Special entities that appear in the text.

        is_private (``bool``, *optional*):
            True, if the gift is private.

        last_resale_star_count (``int``, *optional*):
            For gifts bought from other users, the price paid for the gift (deprecated).
    """

    def __init__(
        self,
        *,
        client: "pyrogram.Client" = None,
        gift: Optional["types.Gift"] = None,
        origin: Optional[str] = None,
        last_resale_currency: Optional[str] = None,
        last_resale_amount: Optional[int] = None,
        owned_gift_id: Optional[str] = None,
        transfer_star_count: Optional[int] = None,
        next_transfer_date: Optional[datetime] = None,
        text: Optional[str] = None,
        entities: Optional[List["types.MessageEntity"]] = None,
        is_private: Optional[bool] = None,
        last_resale_star_count: Optional[int] = None,
    ):
        super().__init__(client)

        self.gift = gift
        self.origin = origin
        self.last_resale_currency = last_resale_currency
        self.last_resale_amount = last_resale_amount
        self.owned_gift_id = owned_gift_id
        self.transfer_star_count = transfer_star_count
        self.next_transfer_date = next_transfer_date
        self.text = text
        self.entities = entities
        self.is_private = is_private
        self.last_resale_star_count = last_resale_star_count

    @staticmethod
    def _parse(
        client: "pyrogram.Client" = None,
        action: Optional[Any] = None,
    ) -> Optional["UniqueGiftInfo"]:
        if not action:
            return None
        if isinstance(action, UniqueGiftInfo):
            return action

        if isinstance(action, raw.types.MessageActionStarGiftUnique):
            origin = "transfer"
            if action.upgrade:
                origin = "upgrade"
            elif action.from_offer:
                origin = "offer"
            elif action.resale_amount:
                origin = "resale"
            elif action.prepaid_upgrade:
                origin = "gifted_upgrade"
            elif action.transferred:
                origin = "transfer"

            last_resale_currency = None
            last_resale_amount = None
            if action.resale_amount:
                last_resale_amount = getattr(action.resale_amount, "amount", None)
                last_resale_currency = "XTR"

            next_transfer_date = None
            if action.can_transfer_at:
                from pyrogram import utils
                next_transfer_date = utils.timestamp_to_datetime(action.can_transfer_at)

            owned_gift_id = str(action.saved_id) if action.saved_id is not None else None

            gift_obj = getattr(action, "gift", None)
            parsed_gift = types.Gift._parse(client, gift_obj) if hasattr(types.Gift, "_parse") else gift_obj

            return UniqueGiftInfo(
                client=client,
                gift=parsed_gift,
                origin=origin,
                last_resale_currency=last_resale_currency,
                last_resale_amount=last_resale_amount,
                owned_gift_id=owned_gift_id,
                transfer_star_count=action.transfer_stars,
                next_transfer_date=next_transfer_date,
                is_private=getattr(action.gift, "is_private", False) if hasattr(action, "gift") else False,
                last_resale_star_count=last_resale_amount,
            )

        if isinstance(action, dict):
            return UniqueGiftInfo(
                client=client,
                gift=action.get("gift"),
                origin=action.get("origin"),
                last_resale_currency=action.get("last_resale_currency"),
                last_resale_amount=action.get("last_resale_amount"),
                owned_gift_id=action.get("owned_gift_id"),
                transfer_star_count=action.get("transfer_star_count"),
                next_transfer_date=action.get("next_transfer_date"),
                text=action.get("text"),
                entities=action.get("entities"),
                is_private=action.get("is_private"),
                last_resale_star_count=action.get("last_resale_star_count"),
            )
        return None

    @staticmethod
    def read(b: Any, client: "pyrogram.Client" = None) -> "UniqueGiftInfo":
        return UniqueGiftInfo._parse(client, b)
