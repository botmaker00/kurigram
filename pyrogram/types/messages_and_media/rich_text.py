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
