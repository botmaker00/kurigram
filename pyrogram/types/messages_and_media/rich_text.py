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

    def write(self, client: "pyrogram.Client" = None) -> "raw.base.RichText":
        from pyrogram import raw
        return raw.types.TextPlain(text=self.text or "")

    @staticmethod
    def read(b: Any, client: "pyrogram.Client" = None) -> "RichText":
        return RichText._parse(client, b)

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
                return RichTextButton(
                    text=text_val,
                    button=rich_text.get("button"),
                    url=rich_text.get("url"),
                    callback_data=rich_text.get("callback_data"),
                )
            return RichText(text=text_val, type=t_type)

        # Fallback for generic objects
        return RichText(text=str(getattr(rich_text, "text", rich_text)))


class RichTextBold(RichText):
    def __init__(self, text: str):
        super().__init__(text=text, type=enums.RichTextType.BOLD)

    def write(self, client: "pyrogram.Client" = None) -> "raw.base.RichText":
        from pyrogram import raw
        return raw.types.TextBold(text=raw.types.TextPlain(text=self.text or ""))


class RichTextItalic(RichText):
    def __init__(self, text: str):
        super().__init__(text=text, type=enums.RichTextType.ITALIC)

    def write(self, client: "pyrogram.Client" = None) -> "raw.base.RichText":
        from pyrogram import raw
        return raw.types.TextItalic(text=raw.types.TextPlain(text=self.text or ""))


class RichTextUnderline(RichText):
    def __init__(self, text: str):
        super().__init__(text=text, type=enums.RichTextType.UNDERLINE)

    def write(self, client: "pyrogram.Client" = None) -> "raw.base.RichText":
        from pyrogram import raw
        return raw.types.TextUnderline(text=raw.types.TextPlain(text=self.text or ""))


class RichTextStrikethrough(RichText):
    def __init__(self, text: str):
        super().__init__(text=text, type=enums.RichTextType.STRIKETHROUGH)

    def write(self, client: "pyrogram.Client" = None) -> "raw.base.RichText":
        from pyrogram import raw
        return raw.types.TextStrike(text=raw.types.TextPlain(text=self.text or ""))


class RichTextSpoiler(RichText):
    def __init__(self, text: str):
        super().__init__(text=text, type=enums.RichTextType.SPOILER)

    def write(self, client: "pyrogram.Client" = None) -> "raw.base.RichText":
        from pyrogram import raw
        return raw.types.TextSpoiler(text=raw.types.TextPlain(text=self.text or ""))


class RichTextCode(RichText):
    def __init__(self, text: str):
        super().__init__(text=text, type=enums.RichTextType.CODE)

    def write(self, client: "pyrogram.Client" = None) -> "raw.base.RichText":
        from pyrogram import raw
        return raw.types.TextFixed(text=raw.types.TextPlain(text=self.text or ""))


class RichTextDateTime(RichText):
    def __init__(self, text: str, date_time_format: Optional[str] = None):
        super().__init__(text=text, type=enums.RichTextType.DATE_TIME)
        self.date_time_format = date_time_format

    def write(self, client: "pyrogram.Client" = None) -> "raw.base.RichText":
        from pyrogram import raw
        return raw.types.TextDate(text=raw.types.TextPlain(text=self.text or ""))


class RichTextTextMention(RichText):
    def __init__(self, text: str, user: Optional[Any] = None):
        super().__init__(text=text, type=enums.RichTextType.TEXT_MENTION)
        self.user = user

    def write(self, client: "pyrogram.Client" = None) -> "raw.base.RichText":
        from pyrogram import raw
        user_id = getattr(self.user, "id", self.user) if self.user is not None else 0
        return raw.types.TextMentionName(text=raw.types.TextPlain(text=self.text or ""), user_id=int(user_id or 0))


class RichTextSubscript(RichText):
    def __init__(self, text: str):
        super().__init__(text=text, type=enums.RichTextType.SUBSCRIPT)

    def write(self, client: "pyrogram.Client" = None) -> "raw.base.RichText":
        from pyrogram import raw
        return raw.types.TextSubscript(text=raw.types.TextPlain(text=self.text or ""))


class RichTextSuperscript(RichText):
    def __init__(self, text: str):
        super().__init__(text=text, type=enums.RichTextType.SUPERSCRIPT)

    def write(self, client: "pyrogram.Client" = None) -> "raw.base.RichText":
        from pyrogram import raw
        return raw.types.TextSuperscript(text=raw.types.TextPlain(text=self.text or ""))


class RichTextMarked(RichText):
    def __init__(self, text: str):
        super().__init__(text=text, type=enums.RichTextType.MARKED)

    def write(self, client: "pyrogram.Client" = None) -> "raw.base.RichText":
        from pyrogram import raw
        return raw.types.TextMarked(text=raw.types.TextPlain(text=self.text or ""))


class RichTextCustomEmoji(RichText):
    def __init__(self, text: str, custom_emoji_id: Optional[str] = None):
        super().__init__(text=text, type=enums.RichTextType.CUSTOM_EMOJI)
        self.custom_emoji_id = custom_emoji_id

    def write(self, client: "pyrogram.Client" = None) -> "raw.base.RichText":
        from pyrogram import raw
        doc_id = int(self.custom_emoji_id or 0)
        return raw.types.TextCustomEmoji(alt=self.text or "", document_id=doc_id)


class RichTextMathematicalExpression(RichText):
    def __init__(self, text: str):
        super().__init__(text=text, type=enums.RichTextType.MATHEMATICAL_EXPRESSION)

    def write(self, client: "pyrogram.Client" = None) -> "raw.base.RichText":
        from pyrogram import raw
        return raw.types.TextMath(source=self.text or "")


class RichTextUrl(RichText):
    def __init__(self, text: str, url: Optional[str] = None):
        super().__init__(text=text, type=enums.RichTextType.URL)
        self.url = url or text

    def write(self, client: "pyrogram.Client" = None) -> "raw.base.RichText":
        from pyrogram import raw
        return raw.types.TextUrl(text=raw.types.TextPlain(text=self.text or ""), url=self.url or self.text or "", webpage_id=0)


class RichTextEmailAddress(RichText):
    def __init__(self, text: str):
        super().__init__(text=text, type=enums.RichTextType.EMAIL_ADDRESS)

    def write(self, client: "pyrogram.Client" = None) -> "raw.base.RichText":
        from pyrogram import raw
        return raw.types.TextEmail(text=raw.types.TextPlain(text=self.text or ""), email=self.text or "")


class RichTextPhoneNumber(RichText):
    def __init__(self, text: str):
        super().__init__(text=text, type=enums.RichTextType.PHONE_NUMBER)

    def write(self, client: "pyrogram.Client" = None) -> "raw.base.RichText":
        from pyrogram import raw
        return raw.types.TextPhone(text=raw.types.TextPlain(text=self.text or ""), phone=self.text or "")


class RichTextBankCardNumber(RichText):
    def __init__(self, text: str):
        super().__init__(text=text, type=enums.RichTextType.BANK_CARD_NUMBER)

    def write(self, client: "pyrogram.Client" = None) -> "raw.base.RichText":
        from pyrogram import raw
        return raw.types.TextBankCard(text=raw.types.TextPlain(text=self.text or ""))


class RichTextMention(RichText):
    def __init__(self, text: str, user_id: Optional[int] = None):
        super().__init__(text=text, type=enums.RichTextType.MENTION)
        self.user_id = user_id

    def write(self, client: "pyrogram.Client" = None) -> "raw.base.RichText":
        from pyrogram import raw
        return raw.types.TextMention(text=raw.types.TextPlain(text=self.text or ""))


class RichTextHashtag(RichText):
    def __init__(self, text: str):
        super().__init__(text=text, type=enums.RichTextType.HASHTAG)

    def write(self, client: "pyrogram.Client" = None) -> "raw.base.RichText":
        from pyrogram import raw
        return raw.types.TextHashtag(text=raw.types.TextPlain(text=self.text or ""))


class RichTextCashtag(RichText):
    def __init__(self, text: str):
        super().__init__(text=text, type=enums.RichTextType.CASHTAG)

    def write(self, client: "pyrogram.Client" = None) -> "raw.base.RichText":
        from pyrogram import raw
        return raw.types.TextCashtag(text=raw.types.TextPlain(text=self.text or ""))


class RichTextBotCommand(RichText):
    def __init__(self, text: str):
        super().__init__(text=text, type=enums.RichTextType.BOT_COMMAND)

    def write(self, client: "pyrogram.Client" = None) -> "raw.base.RichText":
        from pyrogram import raw
        return raw.types.TextBotCommand(text=raw.types.TextPlain(text=self.text or ""))


class RichTextAnchor(RichText):
    def __init__(self, text: str, name: Optional[str] = None):
        super().__init__(text=text, type=enums.RichTextType.ANCHOR)
        self.name = name

    def write(self, client: "pyrogram.Client" = None) -> "raw.base.RichText":
        from pyrogram import raw
        return raw.types.TextAnchor(text=raw.types.TextPlain(text=self.text or ""), name=self.name or "")


class RichTextAnchorLink(RichText):
    def __init__(self, text: str, anchor_name: Optional[str] = None):
        super().__init__(text=text, type=enums.RichTextType.ANCHOR_LINK)
        self.anchor_name = anchor_name

    def write(self, client: "pyrogram.Client" = None) -> "raw.base.RichText":
        from pyrogram import raw
        return raw.types.TextAnchor(text=raw.types.TextPlain(text=self.text or ""), name=self.anchor_name or "")


class RichTextReference(RichText):
    def __init__(self, text: str, index: Optional[int] = None):
        super().__init__(text=text, type=enums.RichTextType.REFERENCE)
        self.index = index

    def write(self, client: "pyrogram.Client" = None) -> "raw.base.RichText":
        from pyrogram import raw
        return raw.types.TextPlain(text=self.text or "")


class RichTextReferenceLink(RichText):
    def __init__(self, text: str, reference_index: Optional[int] = None):
        super().__init__(text=text, type=enums.RichTextType.REFERENCE_LINK)
        self.reference_index = reference_index

    def write(self, client: "pyrogram.Client" = None) -> "raw.base.RichText":
        from pyrogram import raw
        return raw.types.TextPlain(text=self.text or "")


class RichTextButton(RichText):
    def __init__(
        self,
        text: str = "",
        button: Optional[Any] = None,
        *,
        url: Optional[str] = None,
        callback_data: Optional[Union[str, bytes]] = None,
    ):
        super().__init__(text=text, type=enums.RichTextType.BUTTON)
        self.button = button

        extracted_url = url
        extracted_cb = callback_data

        if extracted_url is None and button is not None:
            extracted_url = getattr(button, "url", None) or (button.get("url") if isinstance(button, dict) else None)
            if extracted_url is None and isinstance(button, str) and (button.startswith("http://") or button.startswith("https://") or button.startswith("tg://")):
                extracted_url = button

        if extracted_cb is None and button is not None:
            extracted_cb = getattr(button, "callback_data", None) or (button.get("callback_data") if isinstance(button, dict) else None)
            if extracted_cb is None and getattr(button, "data", None):
                d = button.data
                extracted_cb = d.decode("utf-8", errors="ignore") if isinstance(d, bytes) else str(d)

        if isinstance(extracted_cb, bytes):
            extracted_cb = extracted_cb.decode("utf-8", errors="ignore")

        self.url = extracted_url
        self.callback_data = extracted_cb

        if self.button is None and (self.url is not None or self.callback_data is not None):
            from .rich_message import RichMessageButton
            self.button = RichMessageButton(text=self.text, url=self.url, callback_data=self.callback_data)

    def write(self, client: "pyrogram.Client" = None) -> "raw.base.RichText":
        from pyrogram import raw
        target_url = self.url
        if not target_url and self.callback_data:
            target_url = f"tg://btn?data={self.callback_data}"
        if not target_url and self.button is not None:
            b_url = getattr(self.button, "url", None) or (self.button.get("url") if isinstance(self.button, dict) else None)
            b_cb = getattr(self.button, "callback_data", None) or (self.button.get("callback_data") if isinstance(self.button, dict) else None)
            if b_url:
                target_url = b_url
            elif b_cb:
                cb_str = b_cb.decode("utf-8", errors="ignore") if isinstance(b_cb, bytes) else str(b_cb)
                target_url = f"tg://btn?data={cb_str}"
        return raw.types.TextUrl(text=raw.types.TextPlain(text=self.text or ""), url=target_url or "", webpage_id=0)

    @staticmethod
    def _parse(client: "pyrogram.Client" = None, rich_text: Any = None) -> Optional["RichTextButton"]:
        if not rich_text:
            return None
        if isinstance(rich_text, RichTextButton):
            return rich_text
        from pyrogram import raw
        if isinstance(rich_text, raw.types.TextUrl):
            text_str = getattr(getattr(rich_text, "text", None), "text", str(rich_text.text))
            u = rich_text.url or ""
            if u.startswith("tg://btn?data="):
                return RichTextButton(text=text_str, callback_data=u[len("tg://btn?data="):])
            if u.startswith("tg://callback?data="):
                return RichTextButton(text=text_str, callback_data=u[len("tg://callback?data="):])
            return RichTextButton(text=text_str, url=u)
        if isinstance(rich_text, dict):
            return RichTextButton(
                text=rich_text.get("text", ""),
                button=rich_text.get("button"),
                url=rich_text.get("url"),
                callback_data=rich_text.get("callback_data")
            )
        return RichTextButton(text=str(getattr(rich_text, "text", rich_text)))

    @staticmethod
    def read(b: Any, client: "pyrogram.Client" = None) -> Optional["RichTextButton"]:
        return RichTextButton._parse(client, b)



# InputRichText aliases for Bot API compatibility
InputRichText = RichText
InputRichTextPlain = RichText
InputRichTextBold = RichTextBold
InputRichTextItalic = RichTextItalic
InputRichTextUnderline = RichTextUnderline
InputRichTextStrikethrough = RichTextStrikethrough
InputRichTextSpoiler = RichTextSpoiler
InputRichTextCode = RichTextCode
InputRichTextUrl = RichTextUrl
InputRichTextEmailAddress = RichTextEmailAddress
InputRichTextPhoneNumber = RichTextPhoneNumber
InputRichTextBankCardNumber = RichTextBankCardNumber
InputRichTextMention = RichTextMention
InputRichTextTextMention = RichTextTextMention
InputRichTextHashtag = RichTextHashtag
InputRichTextCashtag = RichTextCashtag
InputRichTextBotCommand = RichTextBotCommand
InputRichTextAnchor = RichTextAnchor
InputRichTextAnchorLink = RichTextAnchorLink
InputRichTextReference = RichTextReference
InputRichTextReferenceLink = RichTextReferenceLink
InputRichTextCustomEmoji = RichTextCustomEmoji
InputRichTextMathematicalExpression = RichTextMathematicalExpression
InputRichTextSubscript = RichTextSubscript
InputRichTextSuperscript = RichTextSuperscript
InputRichTextMarked = RichTextMarked
InputRichTextDateTime = RichTextDateTime
InputRichTextButton = RichTextButton

