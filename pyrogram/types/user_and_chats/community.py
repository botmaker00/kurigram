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

from typing import Any, Optional

import pyrogram
from ..object import Object


class Community(Object):
    """Represents a community (a group of chats).

    Parameters:
        id (``int``):
            Unique identifier for this community.

        name (``str``):
            Name of the community.
    """

    def __init__(
        self,
        *,
        client: "pyrogram.Client" = None,
        id: int = 0,
        name: Optional[str] = None,
        title: Optional[str] = None,
    ):
        super().__init__(client)

        self.id = id
        self.name = name or title or ""
        self.title = self.name

    @staticmethod
    def _parse(
        client: "pyrogram.Client" = None,
        community: Optional[Any] = None,
    ) -> Optional["Community"]:
        if community is None:
            return None
        if isinstance(community, Community):
            return community
        c_id = getattr(community, "id", None) or (community.get("id") if isinstance(community, dict) else 0)
        c_name = getattr(community, "name", None) or getattr(community, "title", None) or (community.get("name") or community.get("title") if isinstance(community, dict) else "")
        return Community(client=client, id=int(c_id), name=str(c_name))
        return None

    @staticmethod
    def read(b: Any, client: "pyrogram.Client" = None) -> "Community":
        return Community._parse(client, b)
