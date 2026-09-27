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

from typing import Any, List, Optional, Union

import pyrogram
from pyrogram import types
from ..object import Object


class RichMessage(Object):
    """Rich formatted message.

    Parameters:
        blocks (List of :obj:`~pyrogram.types.RichBlock`):
            Content of the message.

        is_rtl (``bool``, *optional*):
            True, if the rich message must be shown right-to-left.
    """

    def __init__(
        self,
        *,
        client: "pyrogram.Client" = None,
        blocks: List["types.RichBlock"] = None,
        is_rtl: Optional[bool] = None,
    ):
        super().__init__(client)

        self.blocks = blocks or []
        self.is_rtl = is_rtl


class RichMessageButton(Object):
    """Describes a button in a rich formatted message.

    Parameters:
        text (``str``):
            Label text on the button.

        url (``str``, *optional*):
            HTTP or tg:// URL to be opened when the button is pressed.

        callback_data (``str``, *optional*):
            Data to be sent in a callback query to the bot when the button is pressed, 1-64 bytes.
    """

    def __init__(
        self,
        *,
        text: str,
        url: Optional[str] = None,
        callback_data: Optional[str] = None,
    ):
        super().__init__()

        self.text = text
        self.url = url
        self.callback_data = callback_data


class InputRichMessageMedia(Object):
    """Describes a media element embedded in an outgoing rich message.

    Parameters:
        id (``str``):
            Unique identifier of the media used in a tg://photo?id=, tg://video?id=, or tg://audio?id= link.
            1-64 characters, only A-Z, a-z, 0-9, _ and - are allowed.

        media (:obj:`~pyrogram.types.InputMedia` or ``str``):
            The media to be sent.
    """

    def __init__(
        self,
        *,
        id: str,
        media: Any,
    ):
        super().__init__()

        self.id = id
        self.media = media


class InputRichMessage(Object):
    """Describes an outgoing rich message.

    Parameters:
        html (``str``, *optional*):
            HTML-formatted text to be parsed into rich blocks.

        markdown (``str``, *optional*):
            Markdown-formatted text to be parsed into rich blocks.

        is_rtl (``bool``, *optional*):
            Pass True if the rich message must be shown right-to-left.

        skip_entity_detection (``bool``, *optional*):
            Pass True to skip entity detection for links, mentions, etc.

        blocks (List of :obj:`~pyrogram.types.InputRichBlock`, *optional*):
            List of rich blocks to be sent.

        media (List of :obj:`~pyrogram.types.InputRichMessageMedia`, *optional*):
            List of embedded media objects.
    """

    def __init__(
        self,
        *,
        html: Optional[str] = None,
        markdown: Optional[str] = None,
        is_rtl: Optional[bool] = None,
        skip_entity_detection: Optional[bool] = None,
        blocks: Optional[List["types.InputRichBlock"]] = None,
        media: Optional[List[InputRichMessageMedia]] = None,
    ):
        super().__init__()

        self.html = html
        self.markdown = markdown
        self.is_rtl = is_rtl
        self.skip_entity_detection = skip_entity_detection
        self.blocks = blocks
        self.media = media
