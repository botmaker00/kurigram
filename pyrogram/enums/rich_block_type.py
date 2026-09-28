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


class RichBlockType(AutoName):
    """Rich block type enumeration."""

    PARAGRAPH = auto()
    HEADING = auto()
    SECTION_HEADING = auto()
    PRE = auto()
    PREFORMATTED = auto()
    FOOTER = auto()
    DIVIDER = auto()
    MATHEMATICAL_EXPRESSION = auto()
    ANCHOR = auto()
    LIST = auto()
    BLOCKQUOTE = auto()
    BLOCK_QUOTATION = auto()
    EXPANDABLE_BLOCKQUOTE = auto()
    EXPANDABLE_BLOCK_QUOTATION = auto()
    PULLQUOTE = auto()
    PULL_QUOTATION = auto()
    COLLAGE = auto()
    SLIDESHOW = auto()
    TABLE = auto()
    DETAILS = auto()
    MAP = auto()
    ANIMATION = auto()
    AUDIO = auto()
    DOCUMENT = auto()
    PHOTO = auto()
    VIDEO = auto()
    VOICE_NOTE = auto()
    THINKING = auto()
    BUTTONS = auto()
