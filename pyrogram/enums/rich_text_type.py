#  Kurigram - Telegram MTProto API Client Library for Python
#  Copyright (C) 2017-present Dan <https://github.com/delivrance>
#
#  This file is part of Kurigram.
#
#  Kurigram is free software: you can redistribute it and/or modify
#  it under the terms of the GNU Lesser General Public License as published
#  by the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.

from enum import auto
from .auto_name import AutoName


class RichTextType(AutoName):
    """Rich text type enumeration."""

    BOLD = auto()
    ITALIC = auto()
    UNDERLINE = auto()
    STRIKETHROUGH = auto()
    SPOILER = auto()
    DATE_TIME = auto()
    TEXT_MENTION = auto()
    SUBSCRIPT = auto()
    SUPERSCRIPT = auto()
    MARKED = auto()
    CODE = auto()
    CUSTOM_EMOJI = auto()
    MATHEMATICAL_EXPRESSION = auto()
    URL = auto()
    EMAIL_ADDRESS = auto()
    PHONE_NUMBER = auto()
    BANK_CARD_NUMBER = auto()
    MENTION = auto()
    HASHTAG = auto()
    CASHTAG = auto()
    BOT_COMMAND = auto()
    ANCHOR = auto()
    ANCHOR_LINK = auto()
    REFERENCE = auto()
    REFERENCE_LINK = auto()
    BUTTON = auto()
