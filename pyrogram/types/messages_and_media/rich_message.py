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

    async def write(self, client: "pyrogram.Client" = None) -> "raw.base.InputRichFile":
        from pyrogram import raw
        import asyncio
        m = self.media
        if hasattr(m, "write") and not isinstance(m, (raw.core.TLObject, raw.base.InputPhoto, raw.base.InputDocument, raw.base.InputRichFile)):
            res = m.write(client)
            if asyncio.iscoroutine(res):
                res = await res
            m = res
        if isinstance(m, raw.base.InputPhoto):
            return raw.types.InputRichFilePhoto(id=self.id, photo=m)
        if isinstance(m, raw.base.InputDocument):
            return raw.types.InputRichFileDocument(id=self.id, document=m)
        if isinstance(m, raw.base.InputRichFile):
            return m
        if hasattr(m, "file_id") or "photo" in type(m).__name__.lower():
            return raw.types.InputRichFilePhoto(
                id=self.id,
                photo=raw.types.InputPhoto(id=getattr(m, "id", 0) or 0, access_hash=0, file_reference=b"")
            )
        return raw.types.InputRichFileDocument(
            id=self.id,
            document=raw.types.InputDocument(id=getattr(m, "id", 0) or 0, access_hash=0, file_reference=b"")
        )

    @staticmethod
    def read(b: Any, client: "pyrogram.Client" = None) -> Optional["InputRichMessageMedia"]:
        if b is None:
            return None
        if isinstance(b, InputRichMessageMedia):
            return b
        from pyrogram import raw
        if isinstance(b, raw.types.InputRichFilePhoto):
            return InputRichMessageMedia(id=b.id, media=b.photo)
        if isinstance(b, raw.types.InputRichFileDocument):
            return InputRichMessageMedia(id=b.id, media=b.document)
        if isinstance(b, dict):
            return InputRichMessageMedia(id=b.get("id", ""), media=b.get("media"))
        return InputRichMessageMedia(id=str(getattr(b, "id", "")), media=b)


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

        raw_photos = []
        raw_docs = []
        raw_files = []
        if self.media:
            for item in self.media:
                if isinstance(item, InputRichMessageMedia):
                    m_val = item.media
                    m_id = item.id
                    if hasattr(m_val, "write") and not isinstance(m_val, (raw.core.TLObject, raw.base.InputPhoto, raw.base.InputDocument, raw.base.InputRichFile)):
                        res = m_val.write(client)
                        if asyncio.iscoroutine(res):
                            res = await res
                        m_val = res
                    if isinstance(m_val, raw.base.InputPhoto):
                        raw_photos.append(m_val)
                        raw_files.append(raw.types.InputRichFilePhoto(id=m_id, photo=m_val))
                    elif isinstance(m_val, raw.base.InputDocument):
                        raw_docs.append(m_val)
                        raw_files.append(raw.types.InputRichFileDocument(id=m_id, document=m_val))
                    elif isinstance(m_val, raw.types.InputRichFilePhoto):
                        raw_files.append(m_val)
                        raw_photos.append(m_val.photo)
                    elif isinstance(m_val, raw.types.InputRichFileDocument):
                        raw_files.append(m_val)
                        raw_docs.append(m_val.document)
                    else:
                        if hasattr(m_val, "file_id") or "photo" in type(m_val).__name__.lower():
                            p_obj = raw.types.InputPhoto(id=getattr(m_val, "id", 0) or 0, access_hash=0, file_reference=b"")
                            raw_photos.append(p_obj)
                            raw_files.append(raw.types.InputRichFilePhoto(id=m_id, photo=p_obj))
                        else:
                            d_obj = raw.types.InputDocument(id=getattr(m_val, "id", 0) or 0, access_hash=0, file_reference=b"")
                            raw_docs.append(d_obj)
                            raw_files.append(raw.types.InputRichFileDocument(id=m_id, document=d_obj))
                elif isinstance(item, raw.types.InputRichFilePhoto):
                    raw_files.append(item)
                    raw_photos.append(item.photo)
                elif isinstance(item, raw.types.InputRichFileDocument):
                    raw_files.append(item)
                    raw_docs.append(item.document)
                elif isinstance(item, raw.base.InputPhoto):
                    raw_photos.append(item)
                elif isinstance(item, raw.base.InputDocument):
                    raw_docs.append(item)
                elif hasattr(item, "write"):
                    res = item.write(client)
                    if asyncio.iscoroutine(res):
                        res = await res
                    if isinstance(res, raw.types.InputRichFilePhoto):
                        raw_files.append(res)
                        raw_photos.append(res.photo)
                    elif isinstance(res, raw.types.InputRichFileDocument):
                        raw_files.append(res)
                        raw_docs.append(res.document)
                    elif isinstance(res, raw.base.InputPhoto):
                        raw_photos.append(res)
                    elif isinstance(res, raw.base.InputDocument):
                        raw_docs.append(res)

        if self.markdown:
            return raw.types.InputRichMessageMarkdown(
                markdown=self.markdown,
                rtl=self.is_rtl,
                noautolink=self.skip_entity_detection,
                files=raw_files if raw_files else None,
            )
        if self.html:
            return raw.types.InputRichMessageHTML(
                html=self.html,
                rtl=self.is_rtl,
                noautolink=self.skip_entity_detection,
                files=raw_files if raw_files else None,
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
            photos=raw_photos,
            documents=raw_docs,
            users=[],
        )

    @staticmethod
    def read(b: Any, client: "pyrogram.Client" = None) -> "InputRichMessage":
        from pyrogram import raw, types
        if isinstance(b, raw.types.InputRichMessageMarkdown):
            media_items = []
            for f in (getattr(b, "files", []) or []):
                media_items.append(InputRichMessageMedia.read(f, client))
            return InputRichMessage(
                markdown=b.markdown,
                is_rtl=b.rtl,
                skip_entity_detection=b.noautolink,
                media=media_items if media_items else None,
            )
        if isinstance(b, raw.types.InputRichMessageHTML):
            media_items = []
            for f in (getattr(b, "files", []) or []):
                media_items.append(InputRichMessageMedia.read(f, client))
            return InputRichMessage(
                html=b.html,
                is_rtl=b.rtl,
                skip_entity_detection=b.noautolink,
                media=media_items if media_items else None,
            )
        if isinstance(b, raw.types.InputRichMessage):
            parsed_blocks = [types.RichBlock._parse(client, blk) for blk in b.blocks]
            media_items = []
            for p in (getattr(b, "photos", []) or []):
                media_items.append(InputRichMessageMedia(id=str(getattr(p, "id", "")), media=p))
            for d in (getattr(b, "documents", []) or []):
                media_items.append(InputRichMessageMedia(id=str(getattr(d, "id", "")), media=d))
            return InputRichMessage(
                blocks=parsed_blocks,
                media=media_items if media_items else None,
                is_rtl=b.rtl,
                skip_entity_detection=b.noautolink,
            )
        if isinstance(b, dict):
            media_val = b.get("media")
            parsed_media = [InputRichMessageMedia.read(m, client) for m in media_val] if media_val else None
            return InputRichMessage(
                html=b.get("html"),
                markdown=b.get("markdown"),
                is_rtl=b.get("is_rtl"),
                skip_entity_detection=b.get("skip_entity_detection"),
                blocks=b.get("blocks"),
                media=parsed_media,
            )
        return InputRichMessage(markdown=str(b))


InputRichMessageContent = InputRichMessage

