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
from typing import List, Optional, Union

import pyrogram
from pyrogram import types
from ..object import Object


class TransactionPartner(Object):
    """Base class for transaction partner objects.

    Source: https://core.telegram.org/bots/api#transactionpartner
    """

    def __init__(self, type: str):
        super().__init__()
        self.type = type


class TransactionPartnerUser(TransactionPartner):
    """Describes a transaction with a user.

    Source: https://core.telegram.org/bots/api#transactionpartneruser
    """

    def __init__(
        self,
        *,
        user: "types.User",
        invoice_payload: Optional[str] = None,
        subscription_period: Optional[int] = None,
        paid_media: Optional[List["types.PaidMedia"]] = None,
        paid_media_payload: Optional[str] = None,
        gift: Optional["types.Gift"] = None
    ):
        super().__init__(type="user")
        self.user = user
        self.invoice_payload = invoice_payload
        self.subscription_period = subscription_period
        self.paid_media = paid_media
        self.paid_media_payload = paid_media_payload
        self.gift = gift


class TransactionPartnerChat(TransactionPartner):
    """Describes a transaction with a chat.

    Source: https://core.telegram.org/bots/api#transactionpartnerchat
    """

    def __init__(
        self,
        *,
        chat: "types.Chat",
        gift: Optional["types.Gift"] = None
    ):
        super().__init__(type="chat")
        self.chat = chat
        self.gift = gift


class TransactionPartnerAffiliateProgram(TransactionPartner):
    """Describes the affiliate program that sponsored the transaction.

    Source: https://core.telegram.org/bots/api#transactionpartneraffiliateprogram
    """

    def __init__(
        self,
        *,
        commission_per_mille: int,
        sponsor_chat: Optional["types.Chat"] = None
    ):
        super().__init__(type="affiliate_program")
        self.commission_per_mille = commission_per_mille
        self.sponsor_chat = sponsor_chat


class TransactionPartnerFragment(TransactionPartner):
    """Describes a transaction with Fragment.

    Source: https://core.telegram.org/bots/api#transactionpartnerfragment
    """

    def __init__(
        self,
        *,
        withdrawal_state: Optional["types.RevenueWithdrawalState"] = None
    ):
        super().__init__(type="fragment")
        self.withdrawal_state = withdrawal_state


class TransactionPartnerTelegramAds(TransactionPartner):
    """Describes a transaction with Telegram Ads.

    Source: https://core.telegram.org/bots/api#transactionpartnertelegramads
    """

    def __init__(self):
        super().__init__(type="telegram_ads")


class TransactionPartnerTelegramApi(TransactionPartner):
    """Describes a transaction with Telegram API (for example, Bot API paid requests).

    Source: https://core.telegram.org/bots/api#transactionpartnertelegramapi
    """

    def __init__(self, *, request_count: int):
        super().__init__(type="telegram_api")
        self.request_count = request_count


class TransactionPartnerOther(TransactionPartner):
    """Describes a transaction with an unknown party.

    Source: https://core.telegram.org/bots/api#transactionpartnerother
    """

    def __init__(self):
        super().__init__(type="other")


class StarTransaction(Object):
    """Describes a Telegram Star transaction.

    Source: https://core.telegram.org/bots/api#startransaction
    """

    def __init__(
        self,
        *,
        id: str,
        amount: int,
        date: Union[int, datetime],
        nanostar_amount: Optional[int] = None,
        source: Optional[TransactionPartner] = None,
        receiver: Optional[TransactionPartner] = None
    ):
        super().__init__()
        self.id = id
        self.amount = amount
        self.date = date
        self.nanostar_amount = nanostar_amount
        self.source = source
        self.receiver = receiver

    def __repr__(self) -> str:
        return f"StarTransaction(id={self.id!r}, amount={self.amount})"


class StarTransactions(Object):
    """Contains a list of Telegram Star transactions.

    Source: https://core.telegram.org/bots/api#startransactions
    """

    def __init__(self, *, transactions: List[StarTransaction]):
        super().__init__()
        self.transactions = transactions

    def __repr__(self) -> str:
        return f"StarTransactions(count={len(self.transactions)})"
