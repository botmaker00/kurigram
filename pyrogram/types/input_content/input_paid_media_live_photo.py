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

from typing import BinaryIO, List, Optional, Union

from ... import enums
from ..messages_and_media import MessageEntity
from .input_media_live_photo import InputMediaLivePhoto
from .input_media_photo import InputMediaPhoto
from .input_media_video import InputMediaVideo


class InputPaidMediaLivePhoto(InputMediaLivePhoto):
    """Describes a paid live photo to be sent.

    Parameters:
        media (``str`` | ``BinaryIO``):
            Video of the live photo to send.

        photo (``str`` | ``BinaryIO``, *optional*):
            The static photo to send.

        thumb (``str``, *optional*):
            Thumbnail of the video.

        caption (``str``, *optional*):
            Caption of the paid live photo.

        parse_mode (:obj:`~pyrogram.enums.ParseMode`, *optional*):
            Parse mode for the caption.

        caption_entities (List of :obj:`~pyrogram.types.MessageEntity`, *optional*):
            Special entities that appear in the caption.

        show_caption_above_media (``bool``, *optional*):
            Whether to show caption above media.

        has_spoiler (``bool``, *optional*):
            Whether to show spoiler animation.
    """
    type: str = "live_photo"


class InputPaidMediaPhoto(InputMediaPhoto):
    """Describes a paid photo to be sent."""
    type: str = "photo"


class InputPaidMediaVideo(InputMediaVideo):
    """Describes a paid video to be sent."""
    type: str = "video"
