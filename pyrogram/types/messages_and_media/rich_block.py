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
from pyrogram import enums, types
from ..object import Object


class RichBlockCaption(Object):
    """Caption of a rich formatted block."""

    def __init__(
        self,
        *,
        text: "types.RichText",
        credit: Optional["types.RichText"] = None,
    ):
        super().__init__()
        self.text = text
        self.credit = credit


class RichBlockTableCell(Object):
    """Cell in a rich formatted table."""

    def __init__(
        self,
        *,
        align: str,
        valign: str,
        text: Optional["types.RichText"] = None,
        is_header: Optional[bool] = None,
        colspan: Optional[int] = None,
        rowspan: Optional[int] = None,
    ):
        super().__init__()
        self.align = align
        self.valign = valign
        self.text = text
        self.is_header = is_header
        self.colspan = colspan
        self.rowspan = rowspan


class RichBlockListItem(Object):
    """Item of a rich list."""

    def __init__(
        self,
        *,
        label: str,
        blocks: List["RichBlock"],
        has_checkbox: Optional[bool] = None,
        is_checked: Optional[bool] = None,
        value: Optional[int] = None,
        type: Optional[str] = None,
    ):
        super().__init__()
        self.label = label
        self.blocks = blocks
        self.has_checkbox = has_checkbox
        self.is_checked = is_checked
        self.value = value
        self.type = type


class InputRichBlockListItem(Object):
    """Item of an input rich list."""

    def __init__(
        self,
        *,
        blocks: List["InputRichBlock"],
        has_checkbox: Optional[bool] = None,
        is_checked: Optional[bool] = None,
        value: Optional[int] = None,
        type: Optional[str] = None,
    ):
        super().__init__()
        self.blocks = blocks
        self.has_checkbox = has_checkbox
        self.is_checked = is_checked
        self.value = value
        self.type = type


class RichBlock(Object):
    """Base class for rich blocks."""

    def __init__(
        self,
        *,
        client: "pyrogram.Client" = None,
        type: "enums.RichBlockType",
    ):
        super().__init__(client)
        self.type = type

    @staticmethod
    def _parse(
        client: "pyrogram.Client" = None,
        rich_block: Any = None,
    ) -> Optional["RichBlock"]:
        if not rich_block:
            return None
        if isinstance(rich_block, RichBlock):
            return rich_block
        return None


class RichBlockAnchor(RichBlock):
    def __init__(self, *, client: "pyrogram.Client" = None, name: str):
        super().__init__(client=client, type=enums.RichBlockType.ANCHOR)
        self.name = name


class RichBlockAnimation(RichBlock):
    def __init__(
        self,
        *,
        client: "pyrogram.Client" = None,
        animation: "types.Animation",
        has_spoiler: Optional[bool] = None,
        caption: Optional[RichBlockCaption] = None,
    ):
        super().__init__(client=client, type=enums.RichBlockType.ANIMATION)
        self.animation = animation
        self.has_spoiler = has_spoiler
        self.caption = caption


class RichBlockAudio(RichBlock):
    def __init__(
        self,
        *,
        client: "pyrogram.Client" = None,
        audio: "types.Audio",
        caption: Optional[RichBlockCaption] = None,
    ):
        super().__init__(client=client, type=enums.RichBlockType.AUDIO)
        self.audio = audio
        self.caption = caption


class RichBlockBlockQuotation(RichBlock):
    def __init__(
        self,
        *,
        client: "pyrogram.Client" = None,
        blocks: List[RichBlock],
        credit: Optional["types.RichText"] = None,
    ):
        super().__init__(client=client, type=enums.RichBlockType.BLOCK_QUOTATION)
        self.blocks = blocks
        self.credit = credit


class RichBlockButtons(RichBlock):
    def __init__(
        self,
        *,
        client: "pyrogram.Client" = None,
        buttons: List[List["types.RichMessageButton"]],
        align: Optional[str] = None,
    ):
        super().__init__(client=client, type=enums.RichBlockType.BUTTONS)
        self.buttons = buttons
        self.align = align


class RichBlockCollage(RichBlock):
    def __init__(
        self,
        *,
        client: "pyrogram.Client" = None,
        blocks: List[RichBlock],
        caption: Optional[RichBlockCaption] = None,
    ):
        super().__init__(client=client, type=enums.RichBlockType.COLLAGE)
        self.blocks = blocks
        self.caption = caption


class RichBlockDetails(RichBlock):
    def __init__(
        self,
        *,
        client: "pyrogram.Client" = None,
        summary: "types.RichText",
        blocks: List[RichBlock],
        is_open: Optional[bool] = None,
    ):
        super().__init__(client=client, type=enums.RichBlockType.DETAILS)
        self.summary = summary
        self.blocks = blocks
        self.is_open = is_open


class RichBlockDivider(RichBlock):
    def __init__(self, *, client: "pyrogram.Client" = None):
        super().__init__(client=client, type=enums.RichBlockType.DIVIDER)


class RichBlockDocument(RichBlock):
    def __init__(
        self,
        *,
        client: "pyrogram.Client" = None,
        document: "types.Document",
        caption: Optional[RichBlockCaption] = None,
    ):
        super().__init__(client=client, type=enums.RichBlockType.DOCUMENT)
        self.document = document
        self.caption = caption


class RichBlockExpandableBlockQuotation(RichBlock):
    def __init__(
        self,
        *,
        client: "pyrogram.Client" = None,
        blocks: List[RichBlock],
        credit: Optional["types.RichText"] = None,
    ):
        super().__init__(client=client, type=enums.RichBlockType.EXPANDABLE_BLOCK_QUOTATION)
        self.blocks = blocks
        self.credit = credit


class RichBlockFooter(RichBlock):
    def __init__(
        self,
        *,
        client: "pyrogram.Client" = None,
        text: "types.RichText",
    ):
        super().__init__(client=client, type=enums.RichBlockType.FOOTER)
        self.text = text


class RichBlockList(RichBlock):
    def __init__(
        self,
        *,
        client: "pyrogram.Client" = None,
        items: List[RichBlockListItem],
    ):
        super().__init__(client=client, type=enums.RichBlockType.LIST)
        self.items = items


class RichBlockMap(RichBlock):
    def __init__(
        self,
        *,
        client: "pyrogram.Client" = None,
        location: "types.Location",
        zoom: int,
        width: int,
        height: int,
        caption: Optional[RichBlockCaption] = None,
    ):
        super().__init__(client=client, type=enums.RichBlockType.MAP)
        self.location = location
        self.zoom = zoom
        self.width = width
        self.height = height
        self.caption = caption


class RichBlockMathematicalExpression(RichBlock):
    def __init__(
        self,
        *,
        client: "pyrogram.Client" = None,
        expression: str,
    ):
        super().__init__(client=client, type=enums.RichBlockType.MATHEMATICAL_EXPRESSION)
        self.expression = expression


class RichBlockParagraph(RichBlock):
    def __init__(
        self,
        *,
        client: "pyrogram.Client" = None,
        text: "types.RichText",
    ):
        super().__init__(client=client, type=enums.RichBlockType.PARAGRAPH)
        self.text = text


class RichBlockPhoto(RichBlock):
    def __init__(
        self,
        *,
        client: "pyrogram.Client" = None,
        photo: "types.Photo",
        has_spoiler: Optional[bool] = None,
        caption: Optional[RichBlockCaption] = None,
    ):
        super().__init__(client=client, type=enums.RichBlockType.PHOTO)
        self.photo = photo
        self.has_spoiler = has_spoiler
        self.caption = caption


class RichBlockPreformatted(RichBlock):
    def __init__(
        self,
        *,
        client: "pyrogram.Client" = None,
        text: "types.RichText",
        language: Optional[str] = None,
    ):
        super().__init__(client=client, type=enums.RichBlockType.PREFORMATTED)
        self.text = text
        self.language = language


class RichBlockPullQuotation(RichBlock):
    def __init__(
        self,
        *,
        client: "pyrogram.Client" = None,
        text: "types.RichText",
        credit: Optional["types.RichText"] = None,
    ):
        super().__init__(client=client, type=enums.RichBlockType.PULL_QUOTATION)
        self.text = text
        self.credit = credit


class RichBlockSectionHeading(RichBlock):
    def __init__(
        self,
        *,
        client: "pyrogram.Client" = None,
        text: "types.RichText",
        size: str,
    ):
        super().__init__(client=client, type=enums.RichBlockType.SECTION_HEADING)
        self.text = text
        self.size = size


class RichBlockSlideshow(RichBlock):
    def __init__(
        self,
        *,
        client: "pyrogram.Client" = None,
        blocks: List[RichBlock],
        caption: Optional[RichBlockCaption] = None,
    ):
        super().__init__(client=client, type=enums.RichBlockType.SLIDESHOW)
        self.blocks = blocks
        self.caption = caption


class RichBlockTable(RichBlock):
    def __init__(
        self,
        *,
        client: "pyrogram.Client" = None,
        cells: List[List[RichBlockTableCell]],
        is_bordered: Optional[bool] = None,
        is_striped: Optional[bool] = None,
        caption: Optional[RichBlockCaption] = None,
        is_compact: Optional[bool] = None,
    ):
        super().__init__(client=client, type=enums.RichBlockType.TABLE)
        self.cells = cells
        self.is_bordered = is_bordered
        self.is_striped = is_striped
        self.caption = caption
        self.is_compact = is_compact


class RichBlockThinking(RichBlock):
    def __init__(
        self,
        *,
        client: "pyrogram.Client" = None,
        text: "types.RichText",
    ):
        super().__init__(client=client, type=enums.RichBlockType.THINKING)
        self.text = text


class RichBlockVideo(RichBlock):
    def __init__(
        self,
        *,
        client: "pyrogram.Client" = None,
        video: "types.Video",
        has_spoiler: Optional[bool] = None,
        caption: Optional[RichBlockCaption] = None,
    ):
        super().__init__(client=client, type=enums.RichBlockType.VIDEO)
        self.video = video
        self.has_spoiler = has_spoiler
        self.caption = caption


class RichBlockVoiceNote(RichBlock):
    def __init__(
        self,
        *,
        client: "pyrogram.Client" = None,
        voice_note: "types.Voice",
        caption: Optional[RichBlockCaption] = None,
    ):
        super().__init__(client=client, type=enums.RichBlockType.VOICE_NOTE)
        self.voice_note = voice_note
        self.caption = caption


class InputRichBlock(Object):
    """Base class for input rich blocks."""

    def __init__(
        self,
        *,
        type: "enums.InputRichBlockType",
    ):
        super().__init__()
        self.type = type


class InputRichBlockAnchor(InputRichBlock):
    def __init__(self, *, name: str):
        super().__init__(type=enums.InputRichBlockType.ANCHOR)
        self.name = name


class InputRichBlockAnimation(InputRichBlock):
    def __init__(
        self,
        *,
        animation: Any,
        caption: Optional[RichBlockCaption] = None,
    ):
        super().__init__(type=enums.InputRichBlockType.ANIMATION)
        self.animation = animation
        self.caption = caption


class InputRichBlockAudio(InputRichBlock):
    def __init__(
        self,
        *,
        audio: Any,
        caption: Optional[RichBlockCaption] = None,
    ):
        super().__init__(type=enums.InputRichBlockType.AUDIO)
        self.audio = audio
        self.caption = caption


class InputRichBlockBlockQuotation(InputRichBlock):
    def __init__(
        self,
        *,
        blocks: List[InputRichBlock],
        credit: Optional["types.RichText"] = None,
    ):
        super().__init__(type=enums.InputRichBlockType.BLOCK_QUOTATION)
        self.blocks = blocks
        self.credit = credit


class InputRichBlockButtons(InputRichBlock):
    def __init__(
        self,
        *,
        buttons: List[List["types.RichMessageButton"]],
        align: Optional[str] = None,
    ):
        super().__init__(type=enums.InputRichBlockType.BUTTONS)
        self.buttons = buttons
        self.align = align


class InputRichBlockCollage(InputRichBlock):
    def __init__(
        self,
        *,
        blocks: List[InputRichBlock],
        caption: Optional[RichBlockCaption] = None,
    ):
        super().__init__(type=enums.InputRichBlockType.COLLAGE)
        self.blocks = blocks
        self.caption = caption


class InputRichBlockDetails(InputRichBlock):
    def __init__(
        self,
        *,
        summary: "types.RichText",
        blocks: List[InputRichBlock],
        is_open: Optional[bool] = None,
    ):
        super().__init__(type=enums.InputRichBlockType.DETAILS)
        self.summary = summary
        self.blocks = blocks
        self.is_open = is_open


class InputRichBlockDivider(InputRichBlock):
    def __init__(self):
        super().__init__(type=enums.InputRichBlockType.DIVIDER)


class InputRichBlockDocument(InputRichBlock):
    def __init__(
        self,
        *,
        document: Any,
        caption: Optional[RichBlockCaption] = None,
    ):
        super().__init__(type=enums.InputRichBlockType.DOCUMENT)
        self.document = document
        self.caption = caption


class InputRichBlockExpandableBlockQuotation(InputRichBlock):
    def __init__(
        self,
        *,
        blocks: List[InputRichBlock],
        credit: Optional["types.RichText"] = None,
    ):
        super().__init__(type=enums.InputRichBlockType.EXPANDABLE_BLOCK_QUOTATION)
        self.blocks = blocks
        self.credit = credit


class InputRichBlockFooter(InputRichBlock):
    def __init__(
        self,
        *,
        text: "types.RichText",
    ):
        super().__init__(type=enums.InputRichBlockType.FOOTER)
        self.text = text


class InputRichBlockList(InputRichBlock):
    def __init__(
        self,
        *,
        items: List[InputRichBlockListItem],
    ):
        super().__init__(type=enums.InputRichBlockType.LIST)
        self.items = items


class InputRichBlockMap(InputRichBlock):
    def __init__(
        self,
        *,
        location: "types.Location",
        zoom: int,
        width: int,
        height: int,
        caption: Optional[RichBlockCaption] = None,
    ):
        super().__init__(type=enums.InputRichBlockType.MAP)
        self.location = location
        self.zoom = zoom
        self.width = width
        self.height = height
        self.caption = caption


class InputRichBlockMathematicalExpression(InputRichBlock):
    def __init__(
        self,
        *,
        expression: str,
    ):
        super().__init__(type=enums.InputRichBlockType.MATHEMATICAL_EXPRESSION)
        self.expression = expression


class InputRichBlockParagraph(InputRichBlock):
    def __init__(
        self,
        *,
        text: "types.RichText",
    ):
        super().__init__(type=enums.InputRichBlockType.PARAGRAPH)
        self.text = text


class InputRichBlockPhoto(InputRichBlock):
    def __init__(
        self,
        *,
        photo: Any,
        caption: Optional[RichBlockCaption] = None,
    ):
        super().__init__(type=enums.InputRichBlockType.PHOTO)
        self.photo = photo
        self.caption = caption


class InputRichBlockPreformatted(InputRichBlock):
    def __init__(
        self,
        *,
        text: "types.RichText",
        language: Optional[str] = None,
    ):
        super().__init__(type=enums.InputRichBlockType.PREFORMATTED)
        self.text = text
        self.language = language


class InputRichBlockPullQuotation(InputRichBlock):
    def __init__(
        self,
        *,
        text: "types.RichText",
        credit: Optional["types.RichText"] = None,
    ):
        super().__init__(type=enums.InputRichBlockType.PULL_QUOTATION)
        self.text = text
        self.credit = credit


class InputRichBlockSectionHeading(InputRichBlock):
    def __init__(
        self,
        *,
        text: "types.RichText",
        size: str,
    ):
        super().__init__(type=enums.InputRichBlockType.SECTION_HEADING)
        self.text = text
        self.size = size


class InputRichBlockSlideshow(InputRichBlock):
    def __init__(
        self,
        *,
        blocks: List[InputRichBlock],
        caption: Optional[RichBlockCaption] = None,
    ):
        super().__init__(type=enums.InputRichBlockType.SLIDESHOW)
        self.blocks = blocks
        self.caption = caption


class InputRichBlockTable(InputRichBlock):
    def __init__(
        self,
        *,
        cells: List[List[RichBlockTableCell]],
        is_bordered: Optional[bool] = None,
        is_striped: Optional[bool] = None,
        caption: Optional[RichBlockCaption] = None,
        is_compact: Optional[bool] = None,
    ):
        super().__init__(type=enums.InputRichBlockType.TABLE)
        self.cells = cells
        self.is_bordered = is_bordered
        self.is_striped = is_striped
        self.caption = caption
        self.is_compact = is_compact


class InputRichBlockThinking(InputRichBlock):
    def __init__(
        self,
        *,
        text: "types.RichText",
    ):
        super().__init__(type=enums.InputRichBlockType.THINKING)
        self.text = text


class InputRichBlockVideo(InputRichBlock):
    def __init__(
        self,
        *,
        video: Any,
        caption: Optional[RichBlockCaption] = None,
    ):
        super().__init__(type=enums.InputRichBlockType.VIDEO)
        self.video = video
        self.caption = caption


class InputRichBlockVoiceNote(InputRichBlock):
    def __init__(
        self,
        *,
        voice_note: Any,
        caption: Optional[RichBlockCaption] = None,
    ):
        super().__init__(type=enums.InputRichBlockType.VOICE_NOTE)
        self.voice_note = voice_note
        self.caption = caption
