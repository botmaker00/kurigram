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

from typing import TYPE_CHECKING, Any, List, Optional, Union

import pyrogram
from pyrogram import types
from ..object import Object

if TYPE_CHECKING:
    from pyrogram import raw


class PaidMediaLivePhoto(Object):
    """Describes a paid live photo.

    Parameters:
        live_photo (:obj:`~pyrogram.types.LivePhoto`):
            The live photo.
    """

    def __init__(
        self,
        *,
        client: "pyrogram.Client" = None,
        live_photo: Optional["types.LivePhoto"] = None,
        photo: Optional[Union["types.Photo", Any]] = None,
        video: Optional["types.Video"] = None,
    ):
        super().__init__(client)

        self.type = "live_photo"
        if live_photo is not None:
            self.live_photo = live_photo
        elif photo is not None or video is not None:
            self.live_photo = types.LivePhoto(client=client, photo=photo, video=video)
        else:
            self.live_photo = None
        self.photo = photo or (self.live_photo.photo if self.live_photo else None)
        self.video = video or (self.live_photo.video if self.live_photo else None)

    @staticmethod
    def _parse(
        client: "pyrogram.Client",
        video: "raw.types.Document",
        video_attributes: "raw.types.DocumentAttributeVideo",
    ) -> "PaidMediaLivePhoto":
        return PaidMediaLivePhoto(
            client=client,
            live_photo=types.LivePhoto._parse(client, video, video_attributes),
        )
