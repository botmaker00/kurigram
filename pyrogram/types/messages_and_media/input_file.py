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

from __future__ import annotations

import io
import os
from pathlib import Path
from typing import Optional, Union, BinaryIO

DEFAULT_CHUNK_SIZE = 64 * 1024


class InputFile:
    """This object represents the contents of a file to be uploaded.

    Parameters:
        filename (``str``, *optional*):
            Name of the file.
        chunk_size (``int``, *optional*):
            Chunk size in bytes. Defaults to 64 KiB.
    """

    def __init__(
        self,
        filename: Optional[str] = None,
        chunk_size: int = DEFAULT_CHUNK_SIZE
    ):
        self.filename = filename
        self.chunk_size = chunk_size

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(filename={self.filename!r})"


class FSInputFile(InputFile, os.PathLike):
    """This object represents a file from the local filesystem to be uploaded.

    Parameters:
        path (``str`` | ``pathlib.Path``):
            Path to the local file.
        filename (``str``, *optional*):
            Name of the file to be sent to Telegram. By default parsed from ``path``.
        chunk_size (``int``, *optional*):
            Uploading chunk size in bytes. Defaults to 64 KiB.
    """

    def __init__(
        self,
        path: Union[str, Path],
        filename: Optional[str] = None,
        chunk_size: int = DEFAULT_CHUNK_SIZE
    ):
        path_str = str(path)
        if filename is None:
            filename = os.path.basename(path_str)
        super().__init__(filename=filename, chunk_size=chunk_size)
        self.path: str = path_str

    def __fspath__(self) -> str:
        return self.path

    def __str__(self) -> str:
        return self.path

    def __repr__(self) -> str:
        return f"FSInputFile(path={self.path!r}, filename={self.filename!r})"

    def open(self, mode: str = "rb") -> BinaryIO:
        """Open the file in binary read mode."""
        return open(self.path, mode)

    def read(self, *args, **kwargs) -> bytes:
        """Read bytes from the file."""
        with open(self.path, "rb") as f:
            return f.read(*args, **kwargs)


class BufferedInputFile(InputFile):
    """This object represents an in-memory file from bytes to be uploaded.

    Parameters:
        file (``bytes``):
            Bytes content of the file.
        filename (``str``):
            Name of the file to be sent to Telegram.
        chunk_size (``int``, *optional*):
            Uploading chunk size in bytes. Defaults to 64 KiB.
    """

    def __init__(
        self,
        file: bytes,
        filename: str,
        chunk_size: int = DEFAULT_CHUNK_SIZE
    ):
        super().__init__(filename=filename, chunk_size=chunk_size)
        self.data: bytes = file

    def to_io(self) -> io.BytesIO:
        """Convert the file to a BytesIO object with filename set."""
        bio = io.BytesIO(self.data)
        bio.name = self.filename
        return bio

    def __repr__(self) -> str:
        return f"BufferedInputFile(filename={self.filename!r}, size={len(self.data)})"


class URLInputFile(InputFile):
    """This object represents a file to be downloaded and streamed from a URL.

    Parameters:
        url (``str``):
            URL to the file.
        headers (``dict``, *optional*):
            HTTP headers to pass when fetching the file.
        filename (``str``, *optional*):
            Name of the file. By default extracted from URL path.
        chunk_size (``int``, *optional*):
            Uploading chunk size in bytes. Defaults to 64 KiB.
        timeout (``int``, *optional*):
            Request timeout in seconds. Defaults to 30.
    """

    def __init__(
        self,
        url: str,
        headers: Optional[dict] = None,
        filename: Optional[str] = None,
        chunk_size: int = DEFAULT_CHUNK_SIZE,
        timeout: int = 30
    ):
        if filename is None:
            filename = url.split("?")[0].split("/")[-1] or "file"
        super().__init__(filename=filename, chunk_size=chunk_size)
        self.url: str = url
        self.headers: Optional[dict] = headers
        self.timeout: int = timeout

    def __repr__(self) -> str:
        return f"URLInputFile(url={self.url!r}, filename={self.filename!r})"
