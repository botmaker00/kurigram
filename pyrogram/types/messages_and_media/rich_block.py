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
        text: Optional[Union["types.RichText", str]] = None,
        credit: Optional[Union["types.RichText", str]] = None,
    ):
        super().__init__()
        self.text = text
        self.credit = credit

    async def write(self, client: "pyrogram.Client" = None) -> Any:
        import inspect
        from pyrogram import raw, types
        async def _get_raw(val):
            if val is None:
                return raw.types.TextEmpty()
            if hasattr(val, "write"):
                res = val.write(client)
                return await res if inspect.isawaitable(res) else res
            if isinstance(val, str):
                return raw.types.TextPlain(text=val)
            return raw.types.TextEmpty()
        t = await _get_raw(self.text)
        c = await _get_raw(self.credit)
        return raw.types.PageCaption(text=t, credit=c)

    @staticmethod
    def _parse(client: "pyrogram.Client" = None, caption: Any = None) -> Optional["RichBlockCaption"]:
        if not caption:
            return None
        if isinstance(caption, RichBlockCaption):
            return caption
        from pyrogram import types, raw
        if isinstance(caption, raw.types.PageCaption):
            return RichBlockCaption(
                text=types.RichText._parse(client, caption.text) or types.RichTextPlain(""),
                credit=types.RichText._parse(client, caption.credit) if not isinstance(caption.credit, raw.types.TextEmpty) else None,
            )
        if isinstance(caption, dict):
            return RichBlockCaption(
                text=types.RichText._parse(client, caption.get("text")) or types.RichTextPlain(""),
                credit=types.RichText._parse(client, caption.get("credit")),
            )
        return None

    @staticmethod
    def read(b: Any, client: "pyrogram.Client" = None) -> Optional["RichBlockCaption"]:
        return RichBlockCaption._parse(client, b)


class RichBlockTableCell(Object):
    """Cell in a rich formatted table."""

    def __init__(
        self,
        *,
        text: Optional[Union["types.RichText", str]] = None,
        align: Optional[str] = "left",
        valign: Optional[str] = "top",
        is_header: Optional[bool] = None,
        colspan: Optional[int] = None,
        rowspan: Optional[int] = None,
    ):
        super().__init__()
        self.text = text
        self.align = align
        self.valign = valign
        self.is_header = is_header
        self.colspan = colspan
        self.rowspan = rowspan

    async def write(self, client: "pyrogram.Client" = None) -> Any:
        import inspect
        from pyrogram import raw, types
        t = raw.types.TextEmpty()
        if self.text is not None:
            if hasattr(self.text, "write"):
                res = self.text.write(client)
                t = await res if inspect.isawaitable(res) else res
            elif isinstance(self.text, str):
                t = raw.types.TextPlain(text=self.text)
        align_center = True if self.align == "center" else None
        align_right = True if self.align == "right" else None
        valign_middle = True if self.valign == "middle" else None
        valign_bottom = True if self.valign == "bottom" else None
        return raw.types.PageTableCell(
            header=self.is_header,
            align_center=align_center,
            align_right=align_right,
            valign_middle=valign_middle,
            valign_bottom=valign_bottom,
            text=t,
            colspan=self.colspan,
            rowspan=self.rowspan,
        )

    @staticmethod
    def _parse(client: "pyrogram.Client" = None, cell: Any = None) -> Optional["RichBlockTableCell"]:
        if not cell:
            return None
        if isinstance(cell, RichBlockTableCell):
            return cell
        from pyrogram import types, raw
        if isinstance(cell, raw.types.PageTableCell):
            align = "center" if cell.align_center else ("right" if cell.align_right else "left")
            valign = "middle" if cell.valign_middle else ("bottom" if cell.valign_bottom else "top")
            t = types.RichText._parse(client, cell.text) if cell.text and not isinstance(cell.text, raw.types.TextEmpty) else None
            return RichBlockTableCell(
                align=align,
                valign=valign,
                text=t,
                is_header=cell.header,
                colspan=cell.colspan,
                rowspan=cell.rowspan,
            )
        if isinstance(cell, dict):
            return RichBlockTableCell(
                align=cell.get("align", "left"),
                valign=cell.get("valign", "top"),
                text=types.RichText._parse(client, cell.get("text")),
                is_header=cell.get("is_header"),
                colspan=cell.get("colspan"),
                rowspan=cell.get("rowspan"),
            )
        return None

    @staticmethod
    def read(b: Any, client: "pyrogram.Client" = None) -> Optional["RichBlockTableCell"]:
        return RichBlockTableCell._parse(client, b)


class RichBlockListItem(Object):
    """Item of a rich list."""

    def __init__(
        self,
        *,
        label: Optional[str] = "",
        blocks: Optional[List["RichBlock"]] = None,
        text: Optional[Union["types.RichText", str]] = None,
        has_checkbox: Optional[bool] = None,
        is_checked: Optional[bool] = None,
        value: Optional[int] = None,
        type: Optional[str] = None,
    ):
        super().__init__()
        self.label = label
        self.blocks = blocks or []
        self.text = text
        self.has_checkbox = has_checkbox
        self.is_checked = is_checked
        self.value = value
        self.type = type

    async def write(self, client: "pyrogram.Client" = None) -> Any:
        from pyrogram import raw, types
        raw_blocks = []
        for b in (getattr(self, "blocks", []) or []):
            if hasattr(b, "write"):
                raw_blocks.append(await b.write(client))
            elif isinstance(b, raw.base.PageBlock):
                raw_blocks.append(b)
        if raw_blocks:
            return raw.types.PageListItemBlocks(
                blocks=raw_blocks,
                checkbox=self.has_checkbox,
                checked=self.is_checked,
            )
        else:
            label_text = getattr(self, "text", None) or getattr(self, "label", None) or ""
            t = await label_text.write(client) if hasattr(label_text, "write") else (raw.types.TextPlain(text=str(label_text)) if label_text else raw.types.TextEmpty())
            return raw.types.PageListItemText(
                text=t,
                checkbox=self.has_checkbox,
                checked=self.is_checked,
            )

    @staticmethod
    def _parse(client: "pyrogram.Client" = None, item: Any = None) -> Optional["RichBlockListItem"]:
        if not item:
            return None
        if isinstance(item, RichBlockListItem):
            return item
        from pyrogram import types, raw
        if isinstance(item, raw.types.PageListItemText):
            txt = types.RichText._parse(client, item.text)
            label = getattr(txt, "text", str(txt)) if txt else ""
            return RichBlockListItem(
                label=label,
                text=txt,
                blocks=[types.RichBlockParagraph(text=txt)] if txt else [],
                has_checkbox=item.checkbox,
                is_checked=item.checked,
            )
        if isinstance(item, raw.types.PageListItemBlocks):
            parsed_blocks = [types.RichBlock._parse(client, b) for b in item.blocks]
            return RichBlockListItem(
                label="",
                blocks=[b for b in parsed_blocks if b],
                has_checkbox=item.checkbox,
                is_checked=item.checked,
            )
        if isinstance(item, dict):
            blocks = [types.RichBlock._parse(client, b) for b in item.get("blocks", [])]
            return RichBlockListItem(
                label=item.get("label", ""),
                text=types.RichText._parse(client, item.get("text")),
                blocks=[b for b in blocks if b],
                has_checkbox=item.get("has_checkbox"),
                is_checked=item.get("is_checked"),
                value=item.get("value"),
                type=item.get("type"),
            )
        return None

    @staticmethod
    def read(b: Any, client: "pyrogram.Client" = None) -> Optional["RichBlockListItem"]:
        return RichBlockListItem._parse(client, b)


class InputRichBlockListItem(Object):
    """Item of an input rich list."""

    def __init__(
        self,
        *,
        blocks: Optional[List["InputRichBlock"]] = None,
        label: Optional[str] = "",
        text: Optional[Union["types.RichText", str]] = None,
        has_checkbox: Optional[bool] = None,
        is_checked: Optional[bool] = None,
        value: Optional[int] = None,
        type: Optional[str] = None,
    ):
        super().__init__()
        self.blocks = blocks or []
        self.label = label
        self.text = text
        self.has_checkbox = has_checkbox
        self.is_checked = is_checked
        self.value = value
        self.type = type

    async def write(self, client: "pyrogram.Client" = None) -> Any:
        from pyrogram import raw, types
        raw_blocks = []
        for b in (getattr(self, "blocks", []) or []):
            if hasattr(b, "write"):
                raw_blocks.append(await b.write(client))
            elif isinstance(b, raw.base.PageBlock):
                raw_blocks.append(b)
        if raw_blocks:
            return raw.types.PageListItemBlocks(
                blocks=raw_blocks,
                checkbox=self.has_checkbox,
                checked=self.is_checked,
            )
        else:
            label_text = getattr(self, "text", None) or getattr(self, "label", None) or ""
            t = await label_text.write(client) if hasattr(label_text, "write") else (raw.types.TextPlain(text=str(label_text)) if label_text else raw.types.TextEmpty())
            return raw.types.PageListItemText(
                text=t,
                checkbox=self.has_checkbox,
                checked=self.is_checked,
            )

    @staticmethod
    def _parse(client: "pyrogram.Client" = None, item: Any = None) -> Optional["InputRichBlockListItem"]:
        if not item:
            return None
        if isinstance(item, InputRichBlockListItem):
            return item
        from pyrogram import types, raw
        if isinstance(item, raw.types.PageListItemText):
            txt = types.RichText._parse(client, item.text)
            return InputRichBlockListItem(
                label=getattr(txt, "text", str(txt)) if txt else "",
                text=txt,
                blocks=[types.InputRichBlockParagraph(text=txt)] if txt else [],
                has_checkbox=item.checkbox,
                is_checked=item.checked,
            )
        if isinstance(item, raw.types.PageListItemBlocks):
            parsed_blocks = [types.RichBlock._parse(client, b) for b in item.blocks]
            return InputRichBlockListItem(
                blocks=[b for b in parsed_blocks if b],
                has_checkbox=item.checkbox,
                is_checked=item.checked,
            )
        if isinstance(item, dict):
            blocks = [types.RichBlock._parse(client, b) for b in item.get("blocks", [])]
            return InputRichBlockListItem(
                label=item.get("label", ""),
                text=types.RichText._parse(client, item.get("text")),
                blocks=[b for b in blocks if b],
                has_checkbox=item.get("has_checkbox"),
                is_checked=item.get("is_checked"),
                value=item.get("value"),
                type=item.get("type"),
            )
        return None

    @staticmethod
    def read(b: Any, client: "pyrogram.Client" = None) -> Optional["InputRichBlockListItem"]:
        return InputRichBlockListItem._parse(client, b)


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

    @classmethod
    def read(cls, b: Any, client: "pyrogram.Client" = None) -> Optional["RichBlock"]:
        return cls._parse(client, b)

    async def write(self, client: "pyrogram.Client" = None) -> Any:
        import inspect
        from pyrogram import raw, types

        async def _call_write(obj):
            if hasattr(obj, "write"):
                res = obj.write(client)
                return await res if inspect.isawaitable(res) else res
            return obj

        async def _to_raw_text(t):
            if t is None:
                return raw.types.TextEmpty()
            if hasattr(t, "write"):
                res = t.write(client)
                return await res if inspect.isawaitable(res) else res
            if isinstance(t, str):
                return raw.types.TextPlain(text=t)
            return raw.types.TextEmpty()

        async def _to_raw_caption(c):
            if c is None:
                return raw.types.PageCaption(text=raw.types.TextEmpty(), credit=raw.types.TextEmpty())
            if hasattr(c, "write"):
                res = c.write(client)
                return await res if inspect.isawaitable(res) else res
            if isinstance(c, (str, types.RichText)):
                return raw.types.PageCaption(text=await _to_raw_text(c), credit=raw.types.TextEmpty())
            return raw.types.PageCaption(text=raw.types.TextEmpty(), credit=raw.types.TextEmpty())

        if isinstance(self, (RichBlockParagraph, InputRichBlockParagraph)):
            return raw.types.PageBlockParagraph(text=await _to_raw_text(getattr(self, "text", None)))

        if isinstance(self, (RichBlockSectionHeading, InputRichBlockSectionHeading)):
            t = await _to_raw_text(getattr(self, "text", None))
            sz = str(getattr(self, "size", "h1")).lower()
            if sz == "h2":
                return raw.types.PageBlockSubheader(text=t)
            elif sz == "h3":
                return raw.types.PageBlockHeading3(text=t)
            elif sz == "h4":
                return raw.types.PageBlockHeading4(text=t)
            elif sz == "h5":
                return raw.types.PageBlockHeading5(text=t)
            elif sz == "h6":
                return raw.types.PageBlockHeading6(text=t)
            return raw.types.PageBlockHeader(text=t)

        if isinstance(self, (RichBlockPreformatted, InputRichBlockPreformatted)):
            return raw.types.PageBlockPreformatted(
                text=await _to_raw_text(getattr(self, "text", None)),
                language=getattr(self, "language", None) or "",
            )

        if isinstance(self, (RichBlockFooter, InputRichBlockFooter)):
            return raw.types.PageBlockFooter(text=await _to_raw_text(getattr(self, "text", None)))

        if isinstance(self, (RichBlockDivider, InputRichBlockDivider)):
            return raw.types.PageBlockDivider()

        if isinstance(self, (RichBlockAnchor, InputRichBlockAnchor)):
            return raw.types.PageBlockAnchor(name=getattr(self, "name", "") or "")

        if isinstance(self, (RichBlockMathematicalExpression, InputRichBlockMathematicalExpression)):
            source_txt = getattr(self, "expression", None)
            if source_txt is None and hasattr(self, "text"):
                source_txt = self.text.text if hasattr(self.text, "text") else str(self.text)
            return raw.types.PageBlockMath(source=str(source_txt or ""))

        if isinstance(self, (RichBlockThinking, InputRichBlockThinking)):
            return raw.types.PageBlockThinking(text=await _to_raw_text(getattr(self, "text", None)))

        if isinstance(self, (RichBlockBlockQuotation, InputRichBlockBlockQuotation,
                              RichBlockPullQuotation, InputRichBlockPullQuotation,
                              RichBlockExpandableBlockQuotation, InputRichBlockExpandableBlockQuotation)):
            t = await _to_raw_text(getattr(self, "text", None))
            credit_txt = await _to_raw_text(getattr(self, "credit", None))
            if isinstance(self, (RichBlockPullQuotation, InputRichBlockPullQuotation)):
                return raw.types.PageBlockPullquote(text=t, caption=credit_txt)
            return raw.types.PageBlockBlockquote(text=t, caption=credit_txt)

        if isinstance(self, (RichBlockDetails, InputRichBlockDetails)):
            title_obj = getattr(self, "title", None) or getattr(self, "summary", None)
            title_raw = await _to_raw_text(title_obj)
            sub_raw = []
            for b in (getattr(self, "blocks", []) or []):
                sub_raw.append(await _call_write(b))
            return raw.types.PageBlockDetails(
                title=title_raw,
                blocks=sub_raw,
                open=getattr(self, "is_open", None),
            )

        if isinstance(self, (RichBlockTable, InputRichBlockTable)):
            raw_rows = []
            for row in (getattr(self, "cells", []) or []):
                row_cells = []
                for c in row:
                    row_cells.append(await _call_write(c))
                raw_rows.append(raw.types.PageTableRow(cells=row_cells))
            cap = getattr(self, "caption", None)
            title_raw = await _to_raw_text(cap.text if cap and hasattr(cap, "text") else cap)
            return raw.types.PageBlockTable(
                title=title_raw,
                rows=raw_rows,
                bordered=getattr(self, "is_bordered", None),
                striped=getattr(self, "is_striped", None),
            )

        if isinstance(self, (RichBlockList, InputRichBlockList)):
            raw_items = []
            for item in (getattr(self, "items", []) or []):
                raw_items.append(await _call_write(item))
            return raw.types.PageBlockList(items=raw_items)

        if isinstance(self, (RichBlockButtons, InputRichBlockButtons)):
            rows = []
            for r in (getattr(self, "buttons", []) or []):
                row_btns = []
                for b in r:
                    row_btns.append(await _call_write(b))
                rows.append(raw.types.KeyboardButtonRow(buttons=row_btns))
            return raw.types.ReplyInlineMarkup(rows=rows)

        if isinstance(self, (RichBlockCollage, InputRichBlockCollage)):
            sub_raw = []
            for b in (getattr(self, "blocks", []) or []):
                sub_raw.append(await _call_write(b))
            cap = await _to_raw_caption(getattr(self, "caption", None))
            return raw.types.PageBlockCollage(items=sub_raw, caption=cap)

        if isinstance(self, (RichBlockSlideshow, InputRichBlockSlideshow)):
            sub_raw = []
            for b in (getattr(self, "blocks", []) or []):
                sub_raw.append(await _call_write(b))
            cap = await _to_raw_caption(getattr(self, "caption", None))
            return raw.types.PageBlockSlideshow(items=sub_raw, caption=cap)

        if isinstance(self, (RichBlockPhoto, InputRichBlockPhoto)):
            p = getattr(self, "photo", None)
            photo_id = p if isinstance(p, int) else (getattr(p, "id", 0) if p else 0)
            cap = await _to_raw_caption(getattr(self, "caption", None))
            return raw.types.PageBlockPhoto(photo_id=photo_id, caption=cap, spoiler=getattr(self, "has_spoiler", None))

        if isinstance(self, (RichBlockVideo, InputRichBlockVideo)):
            v = getattr(self, "video", None)
            video_id = v if isinstance(v, int) else (getattr(v, "id", 0) if v else 0)
            cap = await _to_raw_caption(getattr(self, "caption", None))
            return raw.types.PageBlockVideo(video_id=video_id, caption=cap, spoiler=getattr(self, "has_spoiler", None))

        if isinstance(self, (RichBlockAudio, InputRichBlockAudio)):
            a = getattr(self, "audio", None)
            audio_id = a if isinstance(a, int) else (getattr(a, "id", 0) if a else 0)
            cap = await _to_raw_caption(getattr(self, "caption", None))
            return raw.types.PageBlockAudio(audio_id=audio_id, caption=cap)

        if isinstance(self, (RichBlockVoiceNote, InputRichBlockVoiceNote)):
            vn = getattr(self, "voice_note", None)
            vn_id = vn if isinstance(vn, int) else (getattr(vn, "id", 0) if vn else 0)
            cap = await _to_raw_caption(getattr(self, "caption", None))
            return raw.types.PageBlockAudio(audio_id=vn_id, caption=cap)

        if isinstance(self, (RichBlockMap, InputRichBlockMap)):
            loc = getattr(self, "location", None)
            geo = raw.types.GeoPoint(lat=getattr(loc, "latitude", 0.0), long=getattr(loc, "longitude", 0.0), access_hash=0) if loc else raw.types.GeoPointEmpty()
            cap = await _to_raw_caption(getattr(self, "caption", None))
            return raw.types.PageBlockMap(
                geo=geo,
                zoom=getattr(self, "zoom", 12) or 12,
                w=getattr(self, "width", 600) or 600,
                h=getattr(self, "height", 400) or 400,
                caption=cap,
            )

        raise NotImplementedError(f"Rich block serialization not implemented for {type(self).__name__}")

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
        if isinstance(rich_block, (raw.types.ReplyInlineMarkup, raw.types.ReplyKeyboardMarkup)):
            rows = []
            for r in getattr(rich_block, "rows", []):
                row_btns = []
                for b in getattr(r, "buttons", []):
                    parsed_btn = types.RichMessageButton._parse(client, b)
                    if parsed_btn:
                        row_btns.append(parsed_btn)
                rows.append(row_btns)
            return RichBlockButtons(client=client, buttons=rows)

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
        summary: Optional["types.RichText"] = None,
        title: Optional["types.RichText"] = None,
        blocks: Optional[List[RichBlock]] = None,
        is_open: Optional[bool] = None,
    ):
        super().__init__(client=client, type=enums.RichBlockType.DETAILS)
        self.summary = summary or title or types.RichText("")
        self.title = self.summary
        self.blocks = blocks or []
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
        expression: Optional[str] = None,
        text: Optional[Union["types.RichText", str]] = None,
    ):
        super().__init__(client=client, type=enums.RichBlockType.MATHEMATICAL_EXPRESSION)
        self.expression = expression or (text.text if hasattr(text, "text") else (str(text) if text is not None else ""))
        self.text = text or types.RichText(self.expression)


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


class InputRichBlock(RichBlock):
    """Base class for input rich blocks."""

    def __init__(
        self,
        *,
        type: "enums.InputRichBlockType",
    ):
        super().__init__(type=type)


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
        summary: Optional["types.RichText"] = None,
        title: Optional["types.RichText"] = None,
        blocks: Optional[List[InputRichBlock]] = None,
        is_open: Optional[bool] = None,
    ):
        super().__init__(type=enums.InputRichBlockType.DETAILS)
        self.summary = summary or title or types.RichText("")
        self.title = self.summary
        self.blocks = blocks or []
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
        expression: Optional[str] = None,
        text: Optional[Union["types.RichText", str]] = None,
    ):
        super().__init__(type=enums.InputRichBlockType.MATHEMATICAL_EXPRESSION)
        self.expression = expression or (text.text if hasattr(text, "text") else (str(text) if text is not None else ""))
        self.text = text or types.RichText(self.expression)


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
