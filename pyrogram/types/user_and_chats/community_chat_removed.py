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


class CommunityChatRemoved(Object):
    """Describes a service message about a chat being removed from a community. Currently holds no information."""

    def __init__(
        self,
        *,
        client: "pyrogram.Client" = None,
    ):
        super().__init__(client)

    @staticmethod
    def _parse(
        client: "pyrogram.Client" = None,
        action: Optional[Any] = None,
    ) -> Optional["CommunityChatRemoved"]:
        if action is None:
            return None
        if isinstance(action, CommunityChatRemoved):
            return action
        return CommunityChatRemoved(client=client)

    @staticmethod
    def read(b: Any, client: "pyrogram.Client" = None) -> "CommunityChatRemoved":
        return CommunityChatRemoved._parse(client, b)
