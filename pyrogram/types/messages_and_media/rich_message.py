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

    @staticmethod
    def _parse(
        client: "pyrogram.Client" = None,
        rich_message: Any = None,
    ) -> Optional["RichMessage"]:
        if not rich_message:
            return None

        if isinstance(rich_message, RichMessage):
            return rich_message

        blocks = []
        raw_blocks = getattr(rich_message, "blocks", None) or (
            rich_message.get("blocks") if isinstance(rich_message, dict) else None
        )
        if raw_blocks:
            for b in raw_blocks:
                parsed_block = types.RichBlock._parse(client, b) if hasattr(types.RichBlock, "_parse") else b
                blocks.append(parsed_block)

        is_rtl = getattr(rich_message, "is_rtl", None) or (
            rich_message.get("is_rtl") if isinstance(rich_message, dict) else None
        )

        return RichMessage(
            client=client,
            blocks=blocks,
            is_rtl=is_rtl,
        )

    def write(self, client: "pyrogram.Client" = None) -> "raw.base.RichMessage":
        from pyrogram import raw
        raw_blocks = []
        if self.blocks:
            for b in self.blocks:
                if hasattr(b, "write"):
                    raw_blocks.append(b.write(client))
                else:
                    raw_blocks.append(b)
        return raw.types.RichMessage(
            blocks=raw_blocks,
            photos=[],
            documents=[],
            rtl=self.is_rtl,
            part=None,
        )

    @staticmethod
    def read(b: Any, client: "pyrogram.Client" = None) -> "RichMessage":
        return RichMessage._parse(client, b)


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
        text: str = "",
        *,
        url: Optional[str] = None,
        callback_data: Optional[str] = None,
    ):
        super().__init__()

        self.text = text
        self.url = url
        self.callback_data = callback_data

    def write(self, client=None) -> "raw.base.KeyboardButton":
        from pyrogram import raw
        if self.url:
            return raw.types.KeyboardButtonUrl(text=self.text, url=self.url)
        if self.callback_data:
            return raw.types.KeyboardButtonCallback(
                text=self.text,
                data=self.callback_data.encode() if isinstance(self.callback_data, str) else self.callback_data
            )
        return raw.types.KeyboardButton(text=self.text)

    @staticmethod
    def _parse(client: "pyrogram.Client" = None, b: Any = None) -> Optional["RichMessageButton"]:
        if not b:
            return None
        if isinstance(b, RichMessageButton):
            return b
        from pyrogram import raw
        if isinstance(b, raw.types.KeyboardButtonUrl):
            return RichMessageButton(text=b.text, url=b.url)
        if isinstance(b, raw.types.KeyboardButtonCallback):
            data_str = b.data.decode(errors="ignore") if isinstance(b.data, bytes) else str(b.data)
            return RichMessageButton(text=b.text, callback_data=data_str)
        if isinstance(b, raw.types.KeyboardButton):
            return RichMessageButton(text=b.text)
        if isinstance(b, dict):
            return RichMessageButton(
                text=b.get("text", ""),
                url=b.get("url"),
                callback_data=b.get("callback_data"),
            )
        return RichMessageButton(text=str(getattr(b, "text", b)))

    @staticmethod
    def read(b: Any, client: "pyrogram.Client" = None) -> Optional["RichMessageButton"]:
        return RichMessageButton._parse(client, b)


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

    async def write(self, client: "pyrogram.Client" = None) -> "raw.base.InputRichMessage":
        from pyrogram import raw
        import asyncio
        if self.markdown:
            return raw.types.InputRichMessageMarkdown(
                markdown=self.markdown,
                rtl=self.is_rtl,
                noautolink=self.skip_entity_detection,
            )
        if self.html:
            return raw.types.InputRichMessageHTML(
                html=self.html,
                rtl=self.is_rtl,
                noautolink=self.skip_entity_detection,
            )
        raw_blocks = []
        if self.blocks:
            for b in self.blocks:
                if hasattr(b, "write"):
                    res = b.write(client)
                    if asyncio.iscoroutine(res):
                        res = await res
                    raw_blocks.append(res)
                else:
                    raw_blocks.append(b)
        return raw.types.InputRichMessage(
            blocks=raw_blocks,
            rtl=self.is_rtl,
            noautolink=self.skip_entity_detection,
            photos=[],
            documents=[],
            users=[],
        )

    @staticmethod
    def read(b: Any, client: "pyrogram.Client" = None) -> "InputRichMessage":
        from pyrogram import raw, types
        if isinstance(b, raw.types.InputRichMessageMarkdown):
            return InputRichMessage(
                markdown=b.markdown,
                is_rtl=b.rtl,
                skip_entity_detection=b.noautolink,
            )
        if isinstance(b, raw.types.InputRichMessageHTML):
            return InputRichMessage(
                html=b.html,
                is_rtl=b.rtl,
                skip_entity_detection=b.noautolink,
            )
        if isinstance(b, raw.types.InputRichMessage):
            parsed_blocks = [types.RichBlock._parse(client, blk) for blk in b.blocks]
            return InputRichMessage(
                blocks=parsed_blocks,
                is_rtl=b.rtl,
                skip_entity_detection=b.noautolink,
            )
        if isinstance(b, dict):
            return InputRichMessage(
                html=b.get("html"),
                markdown=b.get("markdown"),
                is_rtl=b.get("is_rtl"),
                skip_entity_detection=b.get("skip_entity_detection"),
                blocks=b.get("blocks"),
            )
        return InputRichMessage(markdown=str(b))


InputRichMessageContent = InputRichMessage

