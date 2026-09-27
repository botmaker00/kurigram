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

from typing import Union, List, Optional
import pyrogram
from pyrogram import raw, types
from .input_media import InputMedia

class InputMediaVoiceNote(InputMedia):
    """Represents a voice note to be sent inside an input media.

    Parameters:
        media (``str``):
            Voice note to send. Pass a file_id as string or a HTTP URL.

        duration (``int``, *optional*):
            Duration of the voice note in seconds.

        waveform (``bytes``, *optional*):
            Waveform representation of the voice note.

        caption (``str``, *optional*):
            Caption of the voice note to be sent, 0-1024 characters.
    """

    def __init__(
        self,
        media: str,
        duration: int = 0,
        waveform: bytes = None,
        caption: str = "",
        parse_mode: Optional["enums.ParseMode"] = None,
        caption_entities: List["types.MessageEntity"] = None
    ):
        super().__init__(media, caption, parse_mode, caption_entities)
        self.duration = duration
        self.waveform = waveform

    async def write(self, client: "pyrogram.Client") -> "raw.base.InputMedia":
        if self.media.startswith("http"):
            return raw.types.InputMediaDocumentExternal(
                url=self.media,
                ttl_seconds=None
            )
        else:
            return raw.types.InputMediaDocument(
                id=client.get_file_id(self.media),
                ttl_seconds=None
            )
