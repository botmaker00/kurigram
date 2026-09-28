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

        from pyrogram import raw, types

        # Dictionary / Bot API dispatch
        if isinstance(rich_block, dict):
            b_type = (rich_block.get("type") or "").lower()
            text_val = rich_block.get("text")
            parsed_text = types.RichText._parse(client, text_val) if text_val is not None else None

            if b_type in ("paragraph", "rich_block_paragraph"):
                return RichBlockParagraph(client=client, text=parsed_text or types.RichText(""))
            if b_type in ("section_heading", "rich_block_section_heading", "heading"):
                return RichBlockSectionHeading(client=client, text=parsed_text or types.RichText(""), size=rich_block.get("size", "h1"))
            if b_type in ("preformatted", "rich_block_preformatted", "code"):
                return RichBlockPreformatted(client=client, text=parsed_text or types.RichText(""), language=rich_block.get("language"))
            if b_type in ("footer", "rich_block_footer"):
                return RichBlockFooter(client=client, text=parsed_text or types.RichText(""))
            if b_type in ("divider", "rich_block_divider"):
                return RichBlockDivider(client=client)
            if b_type in ("mathematical_expression", "rich_block_mathematical_expression", "math"):
                return RichBlockMathematicalExpression(client=client, text=parsed_text or types.RichText(""))
            if b_type in ("anchor", "rich_block_anchor"):
                return RichBlockAnchor(client=client, name=rich_block.get("name", ""))
            if b_type in ("list", "rich_block_list"):
                return RichBlockList(client=client, items=rich_block.get("items", []))
            if b_type in ("block_quotation", "rich_block_block_quotation", "quote"):
                return RichBlockBlockQuotation(client=client, text=parsed_text or types.RichText(""))
            if b_type in ("expandable_block_quotation", "rich_block_expandable_block_quotation"):
                return RichBlockExpandableBlockQuotation(client=client, text=parsed_text or types.RichText(""))
            if b_type in ("pull_quotation", "rich_block_pull_quotation"):
                return RichBlockPullQuotation(client=client, text=parsed_text or types.RichText(""))
            if b_type in ("collage", "rich_block_collage"):
                sub_blocks = [RichBlock._parse(client, b) for b in rich_block.get("blocks", [])]
                return RichBlockCollage(client=client, blocks=[b for b in sub_blocks if b])
            if b_type in ("slideshow", "rich_block_slideshow"):
                sub_blocks = [RichBlock._parse(client, b) for b in rich_block.get("blocks", [])]
                return RichBlockSlideshow(client=client, blocks=[b for b in sub_blocks if b])
            if b_type in ("table", "rich_block_table"):
                return RichBlockTable(client=client, cells=rich_block.get("cells", []), is_bordered=rich_block.get("is_bordered"), is_striped=rich_block.get("is_striped"), is_compact=rich_block.get("is_compact"))
            if b_type in ("details", "rich_block_details"):
                title_val = rich_block.get("title")
                parsed_title = types.RichText._parse(client, title_val) if title_val is not None else types.RichText("")
                sub_blocks = [RichBlock._parse(client, b) for b in rich_block.get("blocks", [])]
                return RichBlockDetails(client=client, title=parsed_title, blocks=[b for b in sub_blocks if b], is_open=rich_block.get("is_open"))
            if b_type in ("map", "rich_block_map"):
                return RichBlockMap(client=client, location=rich_block.get("location"))
            if b_type in ("animation", "rich_block_animation"):
                return RichBlockAnimation(client=client, animation=rich_block.get("animation"))
            if b_type in ("audio", "rich_block_audio"):
                return RichBlockAudio(client=client, audio=rich_block.get("audio"))
            if b_type in ("document", "rich_block_document"):
                return RichBlockDocument(client=client, document=rich_block.get("document"))
            if b_type in ("photo", "rich_block_photo"):
                return RichBlockPhoto(client=client, photo=rich_block.get("photo"))
            if b_type in ("video", "rich_block_video"):
                return RichBlockVideo(client=client, video=rich_block.get("video"))
            if b_type in ("voice_note", "rich_block_voice_note"):
                return RichBlockVoiceNote(client=client, voice_note=rich_block.get("voice_note"))
            if b_type in ("thinking", "rich_block_thinking"):
                return RichBlockThinking(client=client, text=parsed_text or types.RichText(""))
            if b_type in ("buttons", "rich_block_buttons"):
                return RichBlockButtons(client=client, buttons=rich_block.get("buttons", []))
            return None

        # Raw TL PageBlock dispatch
        if isinstance(rich_block, raw.types.PageBlockParagraph):
            return RichBlockParagraph(client=client, text=types.RichText._parse(client, rich_block.text) or types.RichText(""))
        if isinstance(rich_block, raw.types.PageBlockHeader):
            return RichBlockSectionHeading(client=client, text=types.RichText._parse(client, rich_block.text) or types.RichText(""), size="h1")
        if isinstance(rich_block, raw.types.PageBlockSubheader):
            return RichBlockSectionHeading(client=client, text=types.RichText._parse(client, rich_block.text) or types.RichText(""), size="h2")
        if isinstance(rich_block, (raw.types.PageBlockHeading1, raw.types.PageBlockHeading2, raw.types.PageBlockHeading3, raw.types.PageBlockHeading4, raw.types.PageBlockHeading5, raw.types.PageBlockHeading6)):
            h_size = type(rich_block).__name__.replace("PageBlockHeading", "h")
            return RichBlockSectionHeading(client=client, text=types.RichText._parse(client, rich_block.text) or types.RichText(""), size=h_size.lower())
        if isinstance(rich_block, (raw.types.PageBlockTitle, raw.types.PageBlockSubtitle, raw.types.PageBlockKicker)):
            return RichBlockSectionHeading(client=client, text=types.RichText._parse(client, rich_block.text) or types.RichText(""), size="h1")
        if isinstance(rich_block, raw.types.PageBlockPreformatted):
            return RichBlockPreformatted(client=client, text=types.RichText._parse(client, rich_block.text) or types.RichText(""), language=getattr(rich_block, "language", None))
        if isinstance(rich_block, raw.types.PageBlockFooter):
            return RichBlockFooter(client=client, text=types.RichText._parse(client, rich_block.text) or types.RichText(""))
        if isinstance(rich_block, raw.types.PageBlockDivider):
            return RichBlockDivider(client=client)
        if isinstance(rich_block, raw.types.PageBlockAnchor):
            return RichBlockAnchor(client=client, name=rich_block.name)
        if isinstance(rich_block, raw.types.PageBlockMath):
            return RichBlockMathematicalExpression(client=client, text=types.RichText(getattr(rich_block, "source", "")))
        if isinstance(rich_block, raw.types.PageBlockThinking):
            return RichBlockThinking(client=client, text=types.RichText._parse(client, rich_block.text) or types.RichText(""))
        if isinstance(rich_block, raw.types.PageBlockBlockquote):
            return RichBlockBlockQuotation(client=client, text=types.RichText._parse(client, rich_block.text) or types.RichText(""))
        if isinstance(rich_block, raw.types.PageBlockBlockquoteBlocks):
            return RichBlockBlockQuotation(client=client, text=types.RichText._parse(client, getattr(rich_block, "caption", "")) or types.RichText(""))
        if isinstance(rich_block, raw.types.PageBlockPullquote):
            return RichBlockPullQuotation(client=client, text=types.RichText._parse(client, rich_block.text) or types.RichText(""))
        if isinstance(rich_block, raw.types.PageBlockCollage):
            sub_blocks = [RichBlock._parse(client, b) for b in (rich_block.items or [])]
            return RichBlockCollage(client=client, blocks=[b for b in sub_blocks if b])
        if isinstance(rich_block, raw.types.PageBlockSlideshow):
            sub_blocks = [RichBlock._parse(client, b) for b in (rich_block.items or [])]
            return RichBlockSlideshow(client=client, blocks=[b for b in sub_blocks if b])
        if isinstance(rich_block, raw.types.PageBlockTable):
            table_cells = []
            for row in getattr(rich_block, "rows", []) or []:
                row_cells = []
                for c in getattr(row, "cells", []) or []:
                    c_text = types.RichText._parse(client, getattr(c, "text", None)) or types.RichText("")
                    align = "center" if getattr(c, "align_center", False) else ("right" if getattr(c, "align_right", False) else "left")
                    valign = "middle" if getattr(c, "valign_middle", False) else ("bottom" if getattr(c, "valign_bottom", False) else "top")
                    row_cells.append(
                        RichBlockTableCell(
                            text=c_text,
                            align=align,
                            valign=valign,
                            is_header=getattr(c, "header", None),
                            colspan=getattr(c, "colspan", None),
                            rowspan=getattr(c, "rowspan", None),
                        )
                    )
                table_cells.append(row_cells)
            return RichBlockTable(
                client=client,
                cells=table_cells,
                is_bordered=getattr(rich_block, "bordered", None),
                is_striped=getattr(rich_block, "striped", None),
            )
        if isinstance(rich_block, raw.types.PageBlockDetails):
            sub_blocks = [RichBlock._parse(client, b) for b in (rich_block.blocks or [])]
            return RichBlockDetails(client=client, title=types.RichText._parse(client, rich_block.title) or types.RichText(""), blocks=[b for b in sub_blocks if b], is_open=getattr(rich_block, "open", None))
        if isinstance(rich_block, (raw.types.PageBlockList, raw.types.PageBlockOrderedList)):
            items = []
            for item in getattr(rich_block, "items", []) or []:
                item_text = types.RichText._parse(client, getattr(item, "text", item)) or types.RichText("")
                items.append(RichBlockListItem(text=item_text))
            return RichBlockList(client=client, items=items)
        if isinstance(rich_block, raw.types.PageBlockPhoto):
            return RichBlockPhoto(client=client, photo=getattr(rich_block, "photo_id", None))
        if isinstance(rich_block, raw.types.PageBlockVideo):
            return RichBlockVideo(client=client, video=getattr(rich_block, "video_id", None))
        if isinstance(rich_block, raw.types.PageBlockAudio):
            return RichBlockAudio(client=client, audio=getattr(rich_block, "audio_id", None))
        if isinstance(rich_block, (raw.types.PageBlockMap, getattr(raw.types, "InputPageBlockMap", object))):
            return RichBlockMap(client=client, zoom=getattr(rich_block, "zoom", None), width=getattr(rich_block, "w", None), height=getattr(rich_block, "h", None))

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
        blocks: Optional[List[RichBlock]] = None,
        credit: Optional["types.RichText"] = None,
        text: Optional[Union["types.RichText", str]] = None,
    ):
        super().__init__(client=client, type=enums.RichBlockType.BLOCK_QUOTATION)
        self.blocks = blocks or []
        self.credit = credit
        self.text = text or (self.blocks[0].text if self.blocks and hasattr(self.blocks[0], "text") else None)


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
        blocks: Optional[List[RichBlock]] = None,
        credit: Optional["types.RichText"] = None,
        text: Optional[Union["types.RichText", str]] = None,
    ):
        super().__init__(client=client, type=enums.RichBlockType.EXPANDABLE_BLOCK_QUOTATION)
        self.blocks = blocks or []
        self.credit = credit
        self.text = text or (self.blocks[0].text if self.blocks and hasattr(self.blocks[0], "text") else None)


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
        blocks: Optional[List[InputRichBlock]] = None,
        credit: Optional["types.RichText"] = None,
        text: Optional[Union["types.RichText", str]] = None,
    ):
        super().__init__(type=enums.InputRichBlockType.BLOCK_QUOTATION)
        self.blocks = blocks or []
        self.credit = credit
        self.text = text or (self.blocks[0].text if self.blocks and hasattr(self.blocks[0], "text") else None)


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
        blocks: Optional[List[InputRichBlock]] = None,
        credit: Optional["types.RichText"] = None,
        text: Optional[Union["types.RichText", str]] = None,
    ):
        super().__init__(type=enums.InputRichBlockType.EXPANDABLE_BLOCK_QUOTATION)
        self.blocks = blocks or []
        self.credit = credit
        self.text = text or (self.blocks[0].text if self.blocks and hasattr(self.blocks[0], "text") else None)


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
