#  Kurigram - Telegram MTProto API Client Library for Python
#  Copyright (C) 2017-present Dan <https://github.com/delivrance>
#
#  This file is part of Kurigram.
#
#  Kurigram is free software: you can redistribute it and/or modify
#  it under the terms of the GNU Lesser General Public License as published
#  by the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.

from typing import Optional, Union, Any, List
from pyrogram import enums
from ..object import Object


class RichText(Object):
    """Base class for rich text elements."""
    def __init__(self, text: str = "", type: Optional[Union["enums.RichTextType", str]] = None):
        super().__init__()
        self.text = text
        self.type = type

    def __str__(self) -> str:
        return self.text or ""

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, str):
            return self.text == other
        if isinstance(other, RichText):
            return self.text == other.text and self.type == other.type
        return super().__eq__(other)

    @staticmethod
    def _parse(
        client: "pyrogram.Client" = None,
        rich_text: Any = None,
    ) -> Optional["RichText"]:
        if not rich_text:
            return None
        if isinstance(rich_text, RichText):
            return rich_text
        if isinstance(rich_text, str):
            return RichText(text=rich_text, type=enums.RichTextType.PLAIN if hasattr(enums.RichTextType, "PLAIN") else "plain")

        # Handle raw TL types
        raw_name = type(rich_text).__name__
        from pyrogram import raw, utils

        def _sub_text(val):
            if val is None:
                return ""
            if isinstance(val, str):
                return val
            if isinstance(val, RichText):
                return val.text
            parsed = RichText._parse(client, val)
            return parsed.text if parsed else str(val)

        if isinstance(rich_text, raw.types.TextPlain):
            return RichText(text=rich_text.text)
        if isinstance(rich_text, raw.types.TextBold):
            return RichTextBold(text=_sub_text(rich_text.text))
        if isinstance(rich_text, raw.types.TextItalic):
            return RichTextItalic(text=_sub_text(rich_text.text))
        if isinstance(rich_text, raw.types.TextUnderline):
            return RichTextUnderline(text=_sub_text(rich_text.text))
        if isinstance(rich_text, raw.types.TextStrike):
            return RichTextStrikethrough(text=_sub_text(rich_text.text))
        if isinstance(rich_text, raw.types.TextFixed):
            return RichTextCode(text=_sub_text(rich_text.text))
        if isinstance(rich_text, raw.types.TextSpoiler):
            return RichTextSpoiler(text=_sub_text(rich_text.text))
        if isinstance(rich_text, raw.types.TextUrl):
            return RichTextUrl(text=_sub_text(rich_text.text), url=getattr(rich_text, "url", None))
        if isinstance(rich_text, raw.types.TextEmail):
            return RichTextEmailAddress(text=_sub_text(rich_text.text))
        if isinstance(rich_text, raw.types.TextPhone):
            return RichTextPhoneNumber(text=_sub_text(rich_text.text))
        if isinstance(rich_text, raw.types.TextSubscript):
            return RichTextSubscript(text=_sub_text(rich_text.text))
        if isinstance(rich_text, raw.types.TextSuperscript):
            return RichTextSuperscript(text=_sub_text(rich_text.text))
        if isinstance(rich_text, raw.types.TextMarked):
            return RichTextMarked(text=_sub_text(rich_text.text))
        if isinstance(rich_text, raw.types.TextAnchor):
            return RichTextAnchor(text=_sub_text(rich_text.text), name=getattr(rich_text, "name", None))
        if isinstance(rich_text, raw.types.TextMath):
            return RichTextMathematicalExpression(text=getattr(rich_text, "source", ""))
        if isinstance(rich_text, raw.types.TextCustomEmoji):
            return RichTextCustomEmoji(text=getattr(rich_text, "alt", ""), custom_emoji_id=str(getattr(rich_text, "document_id", "")))
        if isinstance(rich_text, raw.types.TextMention):
            return RichTextMention(text=_sub_text(rich_text.text))
        if isinstance(rich_text, raw.types.TextMentionName):
            from pyrogram import types as _types
            return RichTextTextMention(text=_sub_text(rich_text.text), user=_types.User(id=rich_text.user_id, client=client))
        if isinstance(rich_text, raw.types.TextHashtag):
            return RichTextHashtag(text=_sub_text(rich_text.text))
        if isinstance(rich_text, raw.types.TextCashtag):
            return RichTextCashtag(text=_sub_text(rich_text.text))
        if isinstance(rich_text, raw.types.TextBotCommand):
            return RichTextBotCommand(text=_sub_text(rich_text.text))
        if isinstance(rich_text, raw.types.TextBankCard):
            return RichTextBankCardNumber(text=_sub_text(rich_text.text))
        if isinstance(rich_text, raw.types.TextDate):
            return RichTextDateTime(text=_sub_text(rich_text.text))
        if isinstance(rich_text, raw.types.TextConcat):
            sub_texts = [_sub_text(t) for t in (rich_text.texts or [])]
            return RichText(text="".join(sub_texts))
        if isinstance(rich_text, raw.types.TextEmpty):
            return RichText(text="")

        # Handle dictionary representations
        if isinstance(rich_text, dict):
            t_type = (rich_text.get("type") or "").lower()
            text_val = rich_text.get("text", "")
            if t_type in ("bold", "rich_text_bold"):
                return RichTextBold(text=text_val)
            if t_type in ("italic", "rich_text_italic"):
                return RichTextItalic(text=text_val)
            if t_type in ("underline", "rich_text_underline"):
                return RichTextUnderline(text=text_val)
            if t_type in ("strikethrough", "strike", "rich_text_strikethrough"):
                return RichTextStrikethrough(text=text_val)
            if t_type in ("code", "pre", "rich_text_code"):
                return RichTextCode(text=text_val)
            if t_type in ("spoiler", "rich_text_spoiler"):
                return RichTextSpoiler(text=text_val)
            if t_type in ("url", "rich_text_url"):
                return RichTextUrl(text=text_val, url=rich_text.get("url"))
            if t_type in ("email_address", "email", "rich_text_email_address"):
                return RichTextEmailAddress(text=text_val)
            if t_type in ("phone_number", "phone", "rich_text_phone_number"):
                return RichTextPhoneNumber(text=text_val)
            if t_type in ("bank_card_number", "bank_card", "rich_text_bank_card_number"):
                return RichTextBankCardNumber(text=text_val)
            if t_type in ("mention", "rich_text_mention"):
                return RichTextMention(text=text_val, user_id=rich_text.get("user_id"))
            if t_type in ("text_mention", "rich_text_text_mention"):
                return RichTextTextMention(text=text_val, user=rich_text.get("user"))
            if t_type in ("hashtag", "rich_text_hashtag"):
                return RichTextHashtag(text=text_val)
            if t_type in ("cashtag", "rich_text_cashtag"):
                return RichTextCashtag(text=text_val)
            if t_type in ("bot_command", "rich_text_bot_command"):
                return RichTextBotCommand(text=text_val)
            if t_type in ("custom_emoji", "rich_text_custom_emoji"):
                return RichTextCustomEmoji(text=text_val, custom_emoji_id=rich_text.get("custom_emoji_id"))
            if t_type in ("subscript", "rich_text_subscript"):
                return RichTextSubscript(text=text_val)
            if t_type in ("superscript", "rich_text_superscript"):
                return RichTextSuperscript(text=text_val)
            if t_type in ("marked", "rich_text_marked"):
                return RichTextMarked(text=text_val)
            if t_type in ("mathematical_expression", "math", "rich_text_mathematical_expression"):
                return RichTextMathematicalExpression(text=text_val)
            if t_type in ("date_time", "date", "rich_text_date_time"):
                return RichTextDateTime(text=text_val, date_time_format=rich_text.get("date_time_format"))
            if t_type in ("anchor", "rich_text_anchor"):
                return RichTextAnchor(text=text_val, name=rich_text.get("name"))
            if t_type in ("anchor_link", "rich_text_anchor_link"):
                return RichTextAnchorLink(text=text_val, anchor_name=rich_text.get("anchor_name"))
            if t_type in ("reference", "rich_text_reference"):
                return RichTextReference(text=text_val, index=rich_text.get("index"))
            if t_type in ("reference_link", "rich_text_reference_link"):
                return RichTextReferenceLink(text=text_val, reference_index=rich_text.get("reference_index"))
            if t_type in ("button", "rich_text_button"):
                return RichTextButton(text=text_val, button=rich_text.get("button"))
            return RichText(text=text_val, type=t_type)

        # Fallback for generic objects
        return RichText(text=str(getattr(rich_text, "text", rich_text)))


class RichTextBold(RichText):
    def __init__(self, text: str):
        super().__init__(text=text, type=enums.RichTextType.BOLD)


class RichTextItalic(RichText):
    def __init__(self, text: str):
        super().__init__(text=text, type=enums.RichTextType.ITALIC)


class RichTextUnderline(RichText):
    def __init__(self, text: str):
        super().__init__(text=text, type=enums.RichTextType.UNDERLINE)


class RichTextStrikethrough(RichText):
    def __init__(self, text: str):
        super().__init__(text=text, type=enums.RichTextType.STRIKETHROUGH)


class RichTextSpoiler(RichText):
    def __init__(self, text: str):
        super().__init__(text=text, type=enums.RichTextType.SPOILER)


class RichTextCode(RichText):
    def __init__(self, text: str):
        super().__init__(text=text, type=enums.RichTextType.CODE)


class RichTextDateTime(RichText):
    def __init__(self, text: str, date_time_format: Optional[str] = None):
        super().__init__(text=text, type=enums.RichTextType.DATE_TIME)
        self.date_time_format = date_time_format


class RichTextTextMention(RichText):
    def __init__(self, text: str, user: Optional[Any] = None):
        super().__init__(text=text, type=enums.RichTextType.TEXT_MENTION)
        self.user = user


class RichTextSubscript(RichText):
    def __init__(self, text: str):
        super().__init__(text=text, type=enums.RichTextType.SUBSCRIPT)


class RichTextSuperscript(RichText):
    def __init__(self, text: str):
        super().__init__(text=text, type=enums.RichTextType.SUPERSCRIPT)


class RichTextMarked(RichText):
    def __init__(self, text: str):
        super().__init__(text=text, type=enums.RichTextType.MARKED)


class RichTextCustomEmoji(RichText):
    def __init__(self, text: str, custom_emoji_id: Optional[str] = None):
        super().__init__(text=text, type=enums.RichTextType.CUSTOM_EMOJI)
        self.custom_emoji_id = custom_emoji_id


class RichTextMathematicalExpression(RichText):
    def __init__(self, text: str):
        super().__init__(text=text, type=enums.RichTextType.MATHEMATICAL_EXPRESSION)


class RichTextUrl(RichText):
    def __init__(self, text: str, url: Optional[str] = None):
        super().__init__(text=text, type=enums.RichTextType.URL)
        self.url = url or text


class RichTextEmailAddress(RichText):
    def __init__(self, text: str):
        super().__init__(text=text, type=enums.RichTextType.EMAIL_ADDRESS)


class RichTextPhoneNumber(RichText):
    def __init__(self, text: str):
        super().__init__(text=text, type=enums.RichTextType.PHONE_NUMBER)


class RichTextBankCardNumber(RichText):
    def __init__(self, text: str):
        super().__init__(text=text, type=enums.RichTextType.BANK_CARD_NUMBER)


class RichTextMention(RichText):
    def __init__(self, text: str, user_id: Optional[int] = None):
        super().__init__(text=text, type=enums.RichTextType.MENTION)
        self.user_id = user_id


class RichTextHashtag(RichText):
    def __init__(self, text: str):
        super().__init__(text=text, type=enums.RichTextType.HASHTAG)


class RichTextCashtag(RichText):
    def __init__(self, text: str):
        super().__init__(text=text, type=enums.RichTextType.CASHTAG)


class RichTextBotCommand(RichText):
    def __init__(self, text: str):
        super().__init__(text=text, type=enums.RichTextType.BOT_COMMAND)


class RichTextAnchor(RichText):
    def __init__(self, text: str, name: Optional[str] = None):
        super().__init__(text=text, type=enums.RichTextType.ANCHOR)
        self.name = name


class RichTextAnchorLink(RichText):
    def __init__(self, text: str, anchor_name: Optional[str] = None):
        super().__init__(text=text, type=enums.RichTextType.ANCHOR_LINK)
        self.anchor_name = anchor_name


class RichTextReference(RichText):
    def __init__(self, text: str, index: Optional[int] = None):
        super().__init__(text=text, type=enums.RichTextType.REFERENCE)
        self.index = index


class RichTextReferenceLink(RichText):
    def __init__(self, text: str, reference_index: Optional[int] = None):
        super().__init__(text=text, type=enums.RichTextType.REFERENCE_LINK)
        self.reference_index = reference_index


class RichTextButton(RichText):
    def __init__(self, text: str, button: Optional[Any] = None):
        super().__init__(text=text, type=enums.RichTextType.BUTTON)
        self.button = button
