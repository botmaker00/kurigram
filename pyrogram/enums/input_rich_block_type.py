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


class InputRichBlockType(AutoName):
    """Input rich block type enumeration."""

    ANCHOR = auto()
    ANIMATION = auto()
    AUDIO = auto()
    BLOCKQUOTE = auto()
    BLOCK_QUOTATION = auto()
    BUTTONS = auto()
    COLLAGE = auto()
    DETAILS = auto()
    DIVIDER = auto()
    DOCUMENT = auto()
    EXPANDABLE_BLOCKQUOTE = auto()
    EXPANDABLE_BLOCK_QUOTATION = auto()
    FOOTER = auto()
    LIST = auto()
    MAP = auto()
    MATHEMATICAL_EXPRESSION = auto()
    PARAGRAPH = auto()
    PHOTO = auto()
    PRE = auto()
    PREFORMATTED = auto()
    PULLQUOTE = auto()
    PULL_QUOTATION = auto()
    HEADING = auto()
    SECTION_HEADING = auto()
    SLIDESHOW = auto()
    TABLE = auto()
    THINKING = auto()
    VIDEO = auto()
    VOICE_NOTE = auto()
