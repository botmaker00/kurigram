#  Kurigram - Telegram MTProto API Client Library for Python
#  Copyright (C) 2017-present Dan <https://github.com/delivrance>
#
#  This file is part of Kurigram.
#
#  Kurigram is free software: you can redistribute it and/or modify
#  it under the terms of the GNU Lesser General Public License as published
#  by the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  Kurigram is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU Lesser General Public License for more details.
#
#  You should have received a copy of the GNU Lesser General Public License
#  along with Kurigram.  If not, see <http://www.gnu.org/licenses/>.

from typing import Any, Optional
from pyrogram import raw
from .input_media import InputMedia


class InputMediaLink(InputMedia):
    """Content of a link/webpage media message to be sent.

    Parameters:
        url (``str``):
            HTTP URL of the media link to send.

        prefer_small_media (``bool``, *optional*):
            Pass True to prefer small media preview.

        prefer_large_media (``bool``, *optional*):
            Pass True to prefer large media preview.

        show_above_text (``bool``, *optional*):
            Pass True to show the media preview above the text.
    """

    def __init__(
        self,
        url: str,
        prefer_small_media: Optional[bool] = None,
        prefer_large_media: Optional[bool] = None,
        show_above_text: Optional[bool] = None,
        force_large_media: Optional[bool] = None,
        force_small_media: Optional[bool] = None,
    ):
        super().__init__(media=url)
        self.url = url
        self.prefer_small_media = prefer_small_media if prefer_small_media is not None else force_small_media
        self.prefer_large_media = prefer_large_media if prefer_large_media is not None else force_large_media
        self.force_small_media = self.prefer_small_media
        self.force_large_media = self.prefer_large_media
        self.show_above_text = show_above_text

    async def write(self, client=None, **kwargs) -> "raw.base.InputMedia":
        return raw.types.InputMediaWebPage(
            url=self.url,
            force_large_media=self.prefer_large_media,
            force_small_media=self.prefer_small_media,
            optional=True
        )

    @staticmethod
    def read(media: Any) -> Optional["InputMediaLink"]:
        if not media:
            return None
        if isinstance(media, InputMediaLink):
            return media
        from pyrogram import raw
        if isinstance(media, raw.types.InputMediaWebPage):
            return InputMediaLink(
                url=media.url,
                prefer_large_media=media.force_large_media,
                prefer_small_media=media.force_small_media,
            )
        if isinstance(media, raw.types.MessageMediaWebPage):
            url = getattr(media.webpage, "url", "") if hasattr(media, "webpage") else ""
            return InputMediaLink(
                url=url,
                prefer_large_media=getattr(media, "force_large_media", None),
                prefer_small_media=getattr(media, "force_small_media", None),
            )
        if isinstance(media, dict):
            return InputMediaLink(
                url=media.get("url", ""),
                prefer_large_media=media.get("prefer_large_media") or media.get("force_large_media"),
                prefer_small_media=media.get("prefer_small_media") or media.get("force_small_media"),
                show_above_text=media.get("show_above_text"),
            )
        return None
