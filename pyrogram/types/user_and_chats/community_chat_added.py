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
from pyrogram import types
from ..object import Object


class CommunityChatAdded(Object):
    """Describes a service message about a chat being added to a community.

    Parameters:
        community (:obj:`~pyrogram.types.Community`):
            The new community to which the chat belongs.
    """

    def __init__(
        self,
        *,
        client: "pyrogram.Client" = None,
        community: "types.Community" = None,
    ):
        super().__init__(client)

        self.community = community

    @staticmethod
    def _parse(
        client: "pyrogram.Client" = None,
        action: Optional[Any] = None,
    ) -> Optional["CommunityChatAdded"]:
        if not action:
            return None
        if isinstance(action, CommunityChatAdded):
            return action
        comm = getattr(action, "community", None) or (action.get("community") if isinstance(action, dict) else None)
        parsed_comm = types.Community._parse(client, comm) if hasattr(types.Community, "_parse") else comm
        return CommunityChatAdded(client=client, community=parsed_comm)

    @staticmethod
    def read(b: Any, client: "pyrogram.Client" = None) -> "CommunityChatAdded":
        return CommunityChatAdded._parse(client, b)
