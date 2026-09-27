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


class UniqueGiftBackdropColors(Object):
    """Colors of the backdrop of a unique gift.

    Source: https://core.telegram.org/bots/api#uniquegiftbackdropcolors
    """

    def __init__(
        self,
        *,
        center_color: int,
        edge_color: int,
        symbol_color: int,
        text_color: int
    ):
        super().__init__()
        self.center_color = center_color
        self.edge_color = edge_color
        self.symbol_color = symbol_color
        self.text_color = text_color


class UniqueGiftBackdrop(Object):
    """Backdrop of a unique gift.

    Source: https://core.telegram.org/bots/api#uniquegiftbackdrop
    """

    def __init__(
        self,
        *,
        name: str,
        colors: UniqueGiftBackdropColors,
        rarity_per_mille: int
    ):
        super().__init__()
        self.name = name
        self.colors = colors
        self.rarity_per_mille = rarity_per_mille


class UniqueGiftModel(Object):
    """Model of a unique gift.

    Source: https://core.telegram.org/bots/api#uniquegiftmodel
    """

    def __init__(
        self,
        *,
        name: str,
        sticker: "types.Sticker" = None,
        rarity_per_mille: int
    ):
        super().__init__()
        self.name = name
        self.sticker = sticker
        self.rarity_per_mille = rarity_per_mille


class UniqueGiftSymbol(Object):
    """Symbol shown on the pattern of a unique gift.

    Source: https://core.telegram.org/bots/api#uniquegiftsymbol
    """

    def __init__(
        self,
        *,
        name: str,
        sticker: "types.Sticker" = None,
        rarity_per_mille: int
    ):
        super().__init__()
        self.name = name
        self.sticker = sticker
        self.rarity_per_mille = rarity_per_mille


class UniqueGiftColors(Object):
    """Color scheme for name, message replies, and link previews based on a unique gift.

    Source: https://core.telegram.org/bots/api#uniquegiftcolors
    """

    def __init__(
        self,
        *,
        model_custom_emoji_id: str,
        symbol_custom_emoji_id: str,
        light_theme_main_color: int,
        light_theme_other_colors: List[int],
        dark_theme_main_color: int,
        dark_theme_other_colors: List[int]
    ):
        super().__init__()
        self.model_custom_emoji_id = model_custom_emoji_id
        self.symbol_custom_emoji_id = symbol_custom_emoji_id
        self.light_theme_main_color = light_theme_main_color
        self.light_theme_other_colors = light_theme_other_colors
        self.dark_theme_main_color = dark_theme_main_color
        self.dark_theme_other_colors = dark_theme_other_colors


class UniqueGift(Object):
    """Describes a unique gift upgraded from a regular gift.

    Source: https://core.telegram.org/bots/api#uniquegift
    """

    def __init__(
        self,
        *,
        gift_id: str,
        base_name: str,
        name: str,
        number: int,
        model: UniqueGiftModel,
        symbol: UniqueGiftSymbol,
        backdrop: UniqueGiftBackdrop,
        is_premium: Optional[bool] = None,
        is_burned: Optional[bool] = None,
        is_from_blockchain: Optional[bool] = None,
        colors: Optional[UniqueGiftColors] = None,
        publisher_chat: Optional["types.Chat"] = None
    ):
        super().__init__()
        self.gift_id = gift_id
        self.base_name = base_name
        self.name = name
        self.number = number
        self.model = model
        self.symbol = symbol
        self.backdrop = backdrop
        self.is_premium = is_premium
        self.is_burned = is_burned
        self.is_from_blockchain = is_from_blockchain
        self.colors = colors
        self.publisher_chat = publisher_chat

    def __repr__(self) -> str:
        return f"UniqueGift(name={self.name!r}, number={self.number})"


class GiftInfo(Object):
    """Describes a service message about a regular gift that was sent or received.

    Source: https://core.telegram.org/bots/api#giftinfo
    """

    def __init__(
        self,
        *,
        gift: "types.Gift",
        owned_gift_id: Optional[str] = None,
        convert_star_count: Optional[int] = None,
        prepaid_upgrade_star_count: Optional[int] = None,
        is_upgrade: Optional[bool] = None,
        can_be_upgraded: Optional[bool] = None,
        text: Optional[str] = None,
        entities: Optional[List["types.MessageEntity"]] = None,
        is_private: Optional[bool] = None
    ):
        super().__init__()
        self.gift = gift
        self.owned_gift_id = owned_gift_id
        self.convert_star_count = convert_star_count
        self.prepaid_upgrade_star_count = prepaid_upgrade_star_count
        self.is_upgrade = is_upgrade
        self.can_be_upgraded = can_be_upgraded
        self.text = text
        self.entities = entities
        self.is_private = is_private


class OwnedGift(Object):
    """Base class for gifts received and owned by a user or chat.

    Source: https://core.telegram.org/bots/api#ownedgift
    """

    def __init__(self, type: str):
        super().__init__()
        self.type = type


class OwnedGiftRegular(OwnedGift):
    """Regular gift owned by a user or chat.

    Source: https://core.telegram.org/bots/api#ownedgiftregular
    """

    def __init__(
        self,
        *,
        gift: "types.Gift",
        send_date: Union[int, datetime],
        sender_user: Optional["types.User"] = None,
        text: Optional[str] = None,
        entities: Optional[List["types.MessageEntity"]] = None,
        is_private: Optional[bool] = None,
        is_saved: Optional[bool] = None,
        can_be_upgraded: Optional[bool] = None,
        was_refunded: Optional[bool] = None,
        convert_star_count: Optional[int] = None,
        prepaid_upgrade_star_count: Optional[int] = None,
        transfer_star_count: Optional[int] = None,
        export_date: Optional[Union[int, datetime]] = None
    ):
        super().__init__(type="regular")
        self.gift = gift
        self.send_date = send_date
        self.sender_user = sender_user
        self.text = text
        self.entities = entities
        self.is_private = is_private
        self.is_saved = is_saved
        self.can_be_upgraded = can_be_upgraded
        self.was_refunded = was_refunded
        self.convert_star_count = convert_star_count
        self.prepaid_upgrade_star_count = prepaid_upgrade_star_count
        self.transfer_star_count = transfer_star_count
        self.export_date = export_date


class OwnedGiftUnique(OwnedGift):
    """Unique gift received and owned by a user or chat.

    Source: https://core.telegram.org/bots/api#ownedgiftunique
    """

    def __init__(
        self,
        *,
        gift: UniqueGift,
        send_date: Union[int, datetime],
        sender_user: Optional["types.User"] = None,
        is_saved: Optional[bool] = None,
        can_be_transferred: Optional[bool] = None,
        transfer_star_count: Optional[int] = None,
        export_date: Optional[Union[int, datetime]] = None
    ):
        super().__init__(type="unique")
        self.gift = gift
        self.send_date = send_date
        self.sender_user = sender_user
        self.is_saved = is_saved
        self.can_be_transferred = can_be_transferred
        self.transfer_star_count = transfer_star_count
        self.export_date = export_date


class OwnedGifts(Object):
    """Contains the list of gifts received and owned by a user or chat.

    Source: https://core.telegram.org/bots/api#ownedgifts
    """

    def __init__(
        self,
        *,
        total_count: int,
        gifts: List[Union[OwnedGiftRegular, OwnedGiftUnique, OwnedGift]]
    ):
        super().__init__()
        self.total_count = total_count
        self.gifts = gifts


class Gifts(Object):
    """Represents a list of gifts.

    Source: https://core.telegram.org/bots/api#gifts
    """

    def __init__(self, *, gifts: List["types.Gift"]):
        super().__init__()
        self.gifts = gifts
