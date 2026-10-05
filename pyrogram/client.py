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

import asyncio
import functools
import inspect
import logging
import math
import os
import platform
import re
import shutil
import sys
import time
from concurrent.futures.thread import ThreadPoolExecutor
from datetime import datetime, timedelta
from hashlib import sha256
from importlib import import_module
from io import BytesIO, StringIO
from mimetypes import MimeTypes
from pathlib import Path
from typing import AsyncGenerator, Callable, List, Optional, Type, Union

import pyrogram
from pyrogram import __license__, __version__, enums, raw, utils
from pyrogram.crypto import aes
from pyrogram.errors import (
    AuthBytesInvalid,
    BadRequest,
    CDNFileHashMismatch,
    ChannelPrivate,
    FloodPremiumWait,
    FloodWait,
    PersistentTimestampInvalid,
    PersistentTimestampOutdated,
    SessionPasswordNeeded,
    Unauthorized,
    VolumeLocNotFound,
    AuthTokenExpired
)
from pyrogram.handlers.handler import Handler
from pyrogram.methods import Methods
import contextlib
from pyrogram.methods.rate_limiter import TokenBucket
from pyrogram.session import Auth, Session, media_window
from pyrogram.storage import SQLiteStorage, Storage
from pyrogram.types import LinkPreviewOptions, TermsOfService, User
from pyrogram.utils import ainput

from .connection import Connection
from .connection.transport import TCP, TCPAbridged
from .dispatcher import Dispatcher
from .file_id import FileId, FileType, ThumbnailSource
from .mime_types import mime_types
from .parser import Parser
from .session.internals import MsgId

log = logging.getLogger(__name__)


class ReadAhead:
    """Borrows read-ahead slots from a client-wide budget and always gives them back."""

    __slots__ = ("_budget", "_held")

    def __init__(self, budget: asyncio.Semaphore):
        self._budget = budget
        self._held = 0

    async def acquire(self):
        await self._budget.acquire()
        self._held += 1

    def release(self):
        if self._held:
            self._held -= 1
            self._budget.release()

    def release_all(self):
        while self._held:
            self.release()


_pwrite = getattr(os, "pwrite", None)


def write_at(fd: int, data: bytes, offset: int) -> None:
    """Write data at offset without disturbing the file position."""
    view = memoryview(data)

    if _pwrite is not None:
        while view:
            written = _pwrite(fd, view, offset)
            view = view[written:]
            offset += written
        return

    os.lseek(fd, offset, os.SEEK_SET)

    while view:
        view = view[os.write(fd, view):]


class Client(Methods):
    """Pyrogram Client, the main means for interacting with Telegram.

    Parameters:
        name (``str``):
            A name for the client, e.g.: "my_account".

        api_id (``int`` | ``str``, *optional*):
            The *api_id* part of the Telegram API key, as integer or string.
            E.g.: 12345 or "12345".

        api_hash (``str``, *optional*):
            The *api_hash* part of the Telegram API key, as string.
            E.g.: "0123456789abcdef0123456789abcdef".

        app_version (``str``, *optional*):
            Application version.
            Defaults to "Pyrogram x.y.z".

        device_model (``str``, *optional*):
            Device model.
            Defaults to *platform.python_implementation() + " " + platform.python_version()*.

        system_version (``str``, *optional*):
            Operating System version.
            Defaults to *platform.system() + " " + platform.release()*.

        lang_pack (``str``, *optional*):
            Name of the language pack used on the client.
            Defaults to "" (empty string).

        lang_code (``str``, *optional*):
            Code of the language used on the client, in ISO 639-1 standard.
            Defaults to "en".

        system_lang_code (``str``, *optional*):
            Code of the language used on the system, in ISO 639-1 standard.
            Defaults to "en".

        ipv6 (``bool``, *optional*):
            Pass True to connect to Telegram using IPv6.
            If the session was previously used with IPv4,
            the first request will be made via IPv4,
            after which the server address will be updated (works both ways).
            Defaults to False (IPv4).

        proxy (``dict`` | ``str``, *optional*):
            The Proxy settings as dict.
            E.g.: *dict(scheme="socks5", hostname="11.22.33.44", port=1234, username="user", password="pass")*
            or *"http://11.22.33.44:1234"* or *"socks5://user:pass@11.22.33.44:1234"* or *"tg://user:pass@11.22.33.44:1234"*.
            The *username* and *password* can be omitted if the proxy doesn't require authorization.

        test_mode (``bool``, *optional*):
            Enable or disable login to the test servers.
            Only applicable for new sessions and will be ignored in case previously created sessions are loaded.
            Defaults to False.

        bot_token (``str``, *optional*):
            Pass the Bot API token to create a bot session, e.g.: "123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11"
            Only applicable for new sessions.

        session_string (``str``, *optional*):
            Pass a session string to load the session in-memory.
            Implies ``in_memory=True``.

        in_memory (``bool``, *optional*):
            Pass True to start an in-memory session that will be discarded as soon as the client stops.
            In order to reconnect again using an in-memory session without having to login again, you can use
            :meth:`~pyrogram.Client.export_session_string` before stopping the client to get a session string you can
            pass to the ``session_string`` parameter.
            Defaults to False.

        phone_number (``str``, *optional*):
            Pass the phone number as string (with the Country Code prefix included) to avoid entering it manually.
            Only applicable for new sessions.

        phone_code (``str``, *optional*):
            Pass the phone code as string (for test numbers only) to avoid entering it manually.
            Only applicable for new sessions.

        password (``str``, *optional*):
            Pass the Two-Step Verification password as string (if required) to avoid entering it manually.
            Only applicable for new sessions.

        workers (``int``, *optional*):
            Number of maximum concurrent workers for handling incoming updates.
            Defaults to ``min(32, os.cpu_count() + 4)``.

        workdir (``str``, *optional*):
            Define a custom working directory.
            The working directory is the location in the filesystem where Pyrogram will store the session files.
            Defaults to the parent directory of the main script.

        plugins (``dict``, *optional*):
            Smart Plugins settings as dict, e.g.: *dict(root="plugins")*.

        parse_mode (:obj:`~pyrogram.enums.ParseMode`, *optional*):
            Set the global parse mode of the client. By default, texts are parsed using both Markdown and HTML styles.
            You can combine both syntaxes together.

        no_updates (``bool``, *optional*):
            Pass True to disable incoming updates.
            When updates are disabled the client can't receive messages or other updates.
            Useful for batch programs that don't need to deal with updates.
            Defaults to False (updates enabled and received).

        skip_updates (``bool``, *optional*):
            Pass True to skip pending updates that arrived while the client was offline.
            Doesn't work if *in_memory* is set to True.
            Defaults to True.

        takeout (``bool``, *optional*):
            Pass True to let the client use a takeout session instead of a normal one, implies *no_updates=True*.
            Useful for exporting Telegram data. Methods invoked inside a takeout session (such as get_chat_history,
            download_media, ...) are less prone to throw FloodWait exceptions.
            Only available for users, bots will ignore this parameter.
            Defaults to False (normal session).

        sleep_threshold (``int``, *optional*):
            Set a sleep threshold for flood wait exceptions happening globally in this client instance, below which any
            request that raises a flood wait will be automatically invoked again after sleeping for the required amount
            of time. Flood wait exceptions requiring higher waiting times will be raised.
            Defaults to 10 seconds.

        hide_password (``bool``, *optional*):
            Pass True to hide the password when typing it during the login.
            Defaults to False, because ``getpass`` (the library used) is known to be problematic in some
            terminal environments.

        max_concurrent_transmissions (``int``, *optional*):
            Set the maximum amount of concurrent transmissions (uploads & downloads).
            A value that is too high may result in network related issues.
            Defaults to 1.

        max_message_cache_size (``int``, *optional*):
            Set the maximum size of the message cache.
            Defaults to 1000.

        max_topic_cache_size (``int``, *optional*):
            Set the maximum size of the topic cache.
            Defaults to 1000.

        storage_engine (:obj:`~pyrogram.storage.Storage`, *optional*):
            Pass an instance of your own implementation of session storage engine.
            Useful when you want to store your session in databases like Mongo, Redis, etc.

        client_platform (:obj:`~pyrogram.enums.ClientPlatform`, *optional*):
            The platform where this client is running.
            Defaults to 'other'

        link_preview_options (:obj:`~pyrogram.types.LinkPreviewOptions`, *optional*):
            Global link preview options for the client.

        fetch_replies (``bool``, *optional*):
            Pass True to automatically fetch replies for messages.
            Defaults to True.

        fetch_topics (``bool``, *optional*):
            Pass True to automatically fetch forum topics.
            Defaults to True.

        fetch_stories (``bool``, *optional*):
            Pass True to automatically fetch stories if they are missing.
            Defaults to True.

        fetch_stickers (``bool``, *optional*):
            Pass True to automatically fetch names of sticker sets.
            Defaults to True.

        loop (:py:class:`asyncio.AbstractEventLoop`, *optional*):
            Event loop.

        init_connection_params (``dict``, *optional*):
            Additional initConnection parameters.
            For now, only the tz_offset field is supported, for specifying timezone offset in seconds.
    """

    APP_VERSION = f"Pyrogram {__version__}"
    DEVICE_MODEL = f"{platform.python_implementation()} {platform.python_version()}"
    SYSTEM_VERSION = f"{platform.system()} {platform.release()}"

    LANG_PACK = ""
    LANG_CODE = "en"
    SYSTEM_LANG_CODE = "en"

    PARENT_DIR = Path(sys.argv[0]).parent

    INVITE_LINK_RE = re.compile(r"^(?:https?://)?(?:www\.)?(?:t(?:elegram)?\.(?:org|me|dog)/(?:joinchat/|\+))([\w-]+)$")
    UPGRADED_GIFT_RE = re.compile(r"^(?:https?://)?(?:www\.)?(?:t(?:elegram)?\.(?:org|me|dog)/(?:nft/|\+))([\w-]+)$")
    CHATLIST_INVITE_RE = re.compile(r"^(?:https?://)?(?:www\.)?(?:t(?:elegram)?\.(?:org|me|dog)/(?:addlist/|\+))([\w-]+)$")
    SAVED_GIFT_RE = re.compile(r"^(-\d+)_(\d+)$")
    CHANNEL_MESSAGE_LINK_RE = re.compile(r"^(?:https?://)?(?:www\.)?(?:t(?:elegram)?\.(?:org|me|dog)/(?:c/)?)([\w]+)(?:.+)?$")
    WORKERS = min(32, (os.cpu_count() or 0) + 4)  # os.cpu_count() can be None
    WORKDIR = PARENT_DIR

    # Interval of seconds in which the updates watchdog will kick in
    UPDATES_WATCHDOG_INTERVAL = 15 * 60

    MAX_CONCURRENT_TRANSMISSIONS = 1
    MAX_MESSAGE_CACHE_SIZE = 1000
    MAX_TOPIC_CACHE_SIZE = 1000

    mimetypes = MimeTypes()
    mimetypes.readfp(StringIO(mime_types))

    def __init__(
        self,
        name: str,
        api_id: Optional[Union[int, str]] = None,
        api_hash: Optional[str] = None,
        app_version: str = APP_VERSION,
        device_model: str = DEVICE_MODEL,
        system_version: str = SYSTEM_VERSION,
        lang_pack: str = LANG_PACK,
        lang_code: str = LANG_CODE,
        system_lang_code: str = SYSTEM_LANG_CODE,
        ipv6: Optional[bool] = False,
        proxy: Optional[Union[dict, str]] = None,
        test_mode: Optional[bool] = False,
        bot_token: Optional[str] = None,
        session_string: Optional[str] = None,
        in_memory: Optional[bool] = None,
        phone_number: Optional[str] = None,
        phone_code: Optional[str] = None,
        password: Optional[str] = None,
        workers: int = WORKERS,
        workdir: Union[str, Path] = WORKDIR,
        plugins: Optional[dict] = None,
        parse_mode: "enums.ParseMode" = enums.ParseMode.DEFAULT,
        no_updates: Optional[bool] = None,
        skip_updates: Optional[bool] = True,
        takeout: Optional[bool] = None,
        sleep_threshold: int = Session.SLEEP_THRESHOLD,
        hide_password: Optional[bool] = False,
        max_concurrent_transmissions: int = MAX_CONCURRENT_TRANSMISSIONS,
        max_message_cache_size: int = MAX_MESSAGE_CACHE_SIZE,
        max_topic_cache_size: int = MAX_TOPIC_CACHE_SIZE,
        storage_engine: Optional[Storage] = None,
        client_platform: "enums.ClientPlatform" = enums.ClientPlatform.OTHER,
        link_preview_options: Optional[LinkPreviewOptions] = None,
        fetch_replies: Optional[bool] = True,
        fetch_topics: Optional[bool] = True,
        fetch_stories: Optional[bool] = True,
        fetch_stickers: Optional[bool] = True,
        init_connection_params: Optional[dict] = None,
        connection_factory: Type[Connection] = Connection,
        protocol_factory: Type[TCP] = TCPAbridged,
        loop: Optional[asyncio.AbstractEventLoop] = None
    ):
        super().__init__()

        self.name = name
        self.api_id = int(api_id) if api_id else None
        self.api_hash = api_hash
        self.app_version = app_version
        self.device_model = device_model
        self.system_version = system_version
        self.lang_pack = lang_pack.lower()
        self.lang_code = lang_code.lower()
        self.system_lang_code = system_lang_code.lower()
        self.ipv6 = ipv6
        self.proxy = proxy
        self.test_mode = test_mode
        self.bot_token = bot_token
        self.session_string = session_string
        self.in_memory = in_memory
        self.phone_number = phone_number
        self.phone_code = phone_code
        self.password = password
        self.workers = workers
        self.workdir = Path(workdir)
        self.plugins = plugins
        self.parse_mode = parse_mode
        self.no_updates = no_updates
        self.skip_updates = skip_updates
        self.takeout = takeout
        self.sleep_threshold = sleep_threshold
        self.hide_password = hide_password
        self.max_concurrent_transmissions = max_concurrent_transmissions
        self.max_message_cache_size = max_message_cache_size
        self.max_topic_cache_size = max_topic_cache_size
        self.client_platform = client_platform
        self.link_preview_options = link_preview_options
        self.fetch_replies = fetch_replies
        self.fetch_topics = fetch_topics
        self.fetch_stories = fetch_stories
        self.fetch_stickers = fetch_stickers
        self.init_connection_params = init_connection_params
        self.connection_factory = connection_factory
        self.protocol_factory = protocol_factory

        self.executor = ThreadPoolExecutor(self.workers, thread_name_prefix="Handler")

        self.storage: Storage

        if self.session_string:
            self.storage = SQLiteStorage(
                self.name,
                workdir=self.workdir,
                session_string=self.session_string,
                in_memory=True
            )
        elif self.in_memory:
            self.storage = SQLiteStorage(self.name, workdir=self.workdir, in_memory=True)
        elif isinstance(storage_engine, Storage):
            self.storage = storage_engine
        else:
            self.storage = SQLiteStorage(self.name, workdir=self.workdir)

        self.listeners = {listener_type: [] for listener_type in pyrogram.types.ListenerTypes}

        self.dispatcher: Dispatcher = Dispatcher(self)

        self.rnd_id = MsgId
        self._server_time_offset = 0.0

        self.parser: Parser = Parser(self)

        self.session: Optional[Session] = None

        self.business_connections = {}

        self.sessions = {}
        self.media_sessions = {}
        self.media_session_pools = {}
        self._media_sessions_locks = {}
        self._media_pool_demand = {}
        self._session_creation_gate = asyncio.Lock()
        self.read_ahead_slots = asyncio.Semaphore(int(os.environ.get("KURIGRAM_READ_AHEAD_SLOTS", 32)))
        self.MEDIA_POOL_CAP = int(os.environ.get("KURIGRAM_MEDIA_POOL_CAP", 20))
        self.sessions_lock = asyncio.Lock()

        self.save_file_semaphore = asyncio.Semaphore(self.max_concurrent_transmissions)
        self.get_file_semaphore = asyncio.Semaphore(self.max_concurrent_transmissions)

        self.is_connected = None
        self.is_initialized = None

        self.takeout_id = None

        self.start_handler = None
        self.stop_handler = None
        self.connect_handler = None
        self.disconnect_handler = None

        self.me: Optional[User] = None

        self.message_cache = Cache(self.max_message_cache_size)
        self.topic_cache = Cache(self.max_topic_cache_size)

        # Sometimes, for some reason, the server will stop sending updates and will only respond to pings.
        # This watchdog will invoke updates.GetState in order to wake up the server and enable it sending updates again
        # after some idle time has been detected.
        self.updates_watchdog_task = None
        self.updates_watchdog_event = asyncio.Event()
        self.last_update_time = datetime.now()

        if isinstance(loop, asyncio.AbstractEventLoop):
            self.loop = loop
        else:
            self.loop = None

        self.__config: "raw.types.Config" = None

    @property
    def loop(self) -> asyncio.AbstractEventLoop:
        if not self._loop:
            self._loop = utils.get_event_loop()
        return self._loop

    @loop.setter
    def loop(self, value: asyncio.AbstractEventLoop):
        self._loop = value

    def __enter__(self):
        return self.start()

    def __exit__(self, *args):
        try:
            self.stop()
        except ConnectionError:
            pass

    async def __aenter__(self):
        return await self.start()

    async def __aexit__(self, *args):
        try:
            await self.stop()
        except ConnectionError:
            pass

    async def updates_watchdog(self):
        while True:
            try:
                await asyncio.wait_for(self.updates_watchdog_event.wait(), self.UPDATES_WATCHDOG_INTERVAL)
            except asyncio.TimeoutError:
                pass
            else:
                break

            if datetime.now() - self.last_update_time > timedelta(seconds=self.UPDATES_WATCHDOG_INTERVAL):
                await self.invoke(raw.functions.updates.GetState())
                await self.recover_gaps()

    async def authorize(self) -> User:
        if self.bot_token:
            return await self.sign_in_bot(self.bot_token)

        print(f"Welcome to Pyrogram (version {__version__})")
        print(f"Pyrogram is free software and comes with ABSOLUTELY NO WARRANTY. Licensed\n"
              f"under the terms of the {__license__}.\n")

        while True:
            try:
                if not self.phone_number:
                    while True:
                        value = await ainput("Enter phone number or bot token: ", loop=self.loop)

                        if not value:
                            continue

                        confirm = await ainput(f'Is "{value}" correct? (y/N): ', loop=self.loop)

                        if confirm.lower() == "y":
                            break

                    if ":" in value:
                        self.bot_token = value
                        return await self.sign_in_bot(value)
                    else:
                        self.phone_number = value

                sent_code = await self.send_phone_number_code(self.phone_number)
            except BadRequest as e:
                print(e.MESSAGE)
                self.phone_number = None
                self.bot_token = None
            else:
                break

        if sent_code.type == enums.SentCodeType.SETUP_EMAIL_REQUIRED:
            print("Setup email required for authorization")

            while True:
                try:
                    while True:
                        email = await ainput("Enter email: ", loop=self.loop)

                        if not email:
                            continue

                        confirm = await ainput(f'Is "{email}" correct? (y/N): ', loop=self.loop)

                        if confirm.lower() == "y":
                            break

                    await self.invoke(
                        raw.functions.account.SendVerifyEmailCode(
                            purpose=raw.types.EmailVerifyPurposeLoginSetup(
                                phone_number=self.phone_number,
                                phone_code_hash=sent_code.phone_code_hash,
                            ),
                            email=email,
                        )
                    )

                    email_code = await ainput("Enter confirmation code: ", loop=self.loop)

                    email_sent_code = await self.invoke(
                        raw.functions.account.VerifyEmail(
                            purpose=raw.types.EmailVerifyPurposeLoginSetup(
                                phone_number=self.phone_number,
                                phone_code_hash=sent_code.phone_code_hash,
                            ),
                            verification=raw.types.EmailVerificationCode(code=email_code),
                        )
                    )

                    if isinstance(email_sent_code, raw.types.account.EmailVerifiedLogin):
                        if isinstance(email_sent_code.sent_code, raw.types.auth.SentCodePaymentRequired):
                            # TODO: raw.functions.auth.CheckPaidAuth
                            raise Unauthorized(
                                f"You need to pay {email_sent_code.sent_code.amount}{email_sent_code.sent_code.currency} or purchase premium to continue authorization "
                                "process, which is currently not supported by Pyrogram."
                            )
                except BadRequest as e:
                    print(e.MESSAGE)
                else:
                    break
        else:
            sent_code_descriptions = {
                enums.SentCodeType.APP: "Telegram app",
                enums.SentCodeType.SMS: "SMS",
                enums.SentCodeType.CALL: "phone call",
                enums.SentCodeType.FLASH_CALL: "phone flash call",
                enums.SentCodeType.FRAGMENT_SMS: "Fragment",
                enums.SentCodeType.EMAIL_CODE: "email code"
            }

            print(f"The confirmation code has been sent via {sent_code_descriptions[sent_code.type]}")

        while True:
            if not self.phone_code:
                self.phone_code = await ainput("Enter confirmation code: ", loop=self.loop)

            try:
                signed_in = await self.sign_in(self.phone_number, sent_code.phone_code_hash, self.phone_code)
            except BadRequest as e:
                print(e.MESSAGE)
                self.phone_code = None
            except SessionPasswordNeeded as e:
                print(e.MESSAGE)

                while True:
                    print("Password hint: {}".format(await self.get_password_hint()))

                    if not self.password:
                        self.password = await ainput("Enter 2FA password (empty to recover): ", hide=self.hide_password, loop=self.loop)

                    try:
                        if not self.password:
                            confirm = await ainput("Confirm password recovery (y/N): ", loop=self.loop)

                            if confirm.lower() == "y":
                                email_pattern = await self.send_recovery_code()
                                print(f"The recovery code has been sent to {email_pattern}")

                                while True:
                                    recovery_code = await ainput("Enter recovery code: ", loop=self.loop)

                                    try:
                                        return await self.recover_password(recovery_code)
                                    except BadRequest as e:
                                        print(e.MESSAGE)
                                    except Exception as e:
                                        log.exception(e)
                                        raise
                            else:
                                self.password = None
                        else:
                            return await self.check_password(self.password)
                    except BadRequest as e:
                        print(e.MESSAGE)
                        self.password = None
            else:
                break

        if isinstance(signed_in, User):
            return signed_in

        while True:
            first_name = await ainput("Enter first name: ", loop=self.loop)
            last_name = await ainput("Enter last name (empty to skip): ", loop=self.loop)

            try:
                signed_up = await self.sign_up(
                    self.phone_number,
                    sent_code.phone_code_hash,
                    first_name,
                    last_name
                )
            except BadRequest as e:
                print(e.MESSAGE)
            else:
                break

        if isinstance(signed_in, TermsOfService):
            print("\n" + signed_in.text + "\n")
            await self.accept_terms_of_service(signed_in.id)

        return signed_up

    async def authorize_qr(self, except_ids: List[int] = []) -> "User":
        from qrcode import QRCode

        qr_login = QRLogin(self, except_ids)
        await qr_login.recreate()

        qr = QRCode(version=1)

        while True:
            try:
                print(
                    "\x1b[2J\n"
                    f"Welcome to Pyrogram (version {__version__})\n"
                    "Pyrogram is free software and comes with ABSOLUTELY NO WARRANTY. Licensed\n"
                    f"under the terms of the {__license__}.\n"
                    "Scan the QR code below to login\n"
                    "Settings -> Privacy and Security -> Active Sessions -> Scan QR Code.",
                    flush=True
                )

                qr.clear()
                qr.add_data(qr_login.url)
                qr.print_ascii(tty=True)
                log.info("Waiting for QR code being scanned.")

                signed_in = await qr_login.wait()

                if signed_in:
                    log.info(f"Logged in successfully as {signed_in.full_name}")
                    return signed_in
            except asyncio.TimeoutError:
                log.info("Recreating QR code.")
                await qr_login.recreate()
            except AuthTokenExpired:
                log.info("Auth token expired. Recreating QR code.")
                await qr_login.recreate()
            except SessionPasswordNeeded as e:
                print(e.MESSAGE)

                while True:
                    print("Password hint: {}".format(await self.get_password_hint()))

                    if not self.password:
                        self.password = await ainput("Enter 2FA password (empty to recover): ", hide=self.hide_password, loop=self.loop)

                    try:
                        if not self.password:
                            confirm = await ainput("Confirm password recovery (y/N): ", loop=self.loop)

                            if confirm.lower() == "y":
                                email_pattern = await self.send_recovery_code()
                                print(f"The recovery code has been sent to {email_pattern}")

                                while True:
                                    recovery_code = await ainput("Enter recovery code: ", loop=self.loop)

                                    try:
                                        return await self.recover_password(recovery_code)
                                    except BadRequest as e:
                                        print(e.MESSAGE)
                                    except Exception as e:
                                        log.exception(e)
                                        raise
                            else:
                                self.password = None
                        else:
                            return await self.check_password(self.password)
                    except BadRequest as e:
                        print(e.MESSAGE)
                        self.password = None
            else:
                break

    def set_parse_mode(self, parse_mode: Optional["enums.ParseMode"]):
        """Set the parse mode to be used globally by the client.

        When setting the parse mode with this method, all other methods having a *parse_mode* parameter will follow the
        global value by default.

        Parameters:
            parse_mode (:obj:`~pyrogram.enums.ParseMode`):
                By default, texts are parsed using both Markdown and HTML styles.
                You can combine both syntaxes together.

        Example:
            .. code-block:: python

                from pyrogram import enums

                # Default combined mode: Markdown + HTML
                await app.send_message("me", "1. **markdown** and <i>html</i>")

                # Force Markdown-only, HTML is disabled
                app.set_parse_mode(enums.ParseMode.MARKDOWN)
                await app.send_message("me", "2. **markdown** and <i>html</i>")

                # Force HTML-only, Markdown is disabled
                app.set_parse_mode(enums.ParseMode.HTML)
                await app.send_message("me", "3. **markdown** and <i>html</i>")

                # Disable the parser completely
                app.set_parse_mode(enums.ParseMode.DISABLED)
                await app.send_message("me", "4. **markdown** and <i>html</i>")

                # Bring back the default combined mode
                app.set_parse_mode(enums.ParseMode.DEFAULT)
                await app.send_message("me", "5. **markdown** and <i>html</i>")
        """

        self.parse_mode = parse_mode

    async def fetch_peers(self, peers: List[Union[raw.types.User, raw.types.Chat, raw.types.Channel]]) -> bool:
        is_min = False
        parsed_peers = []
        parsed_usernames = []

        for peer in peers:
            if getattr(peer, "min", False):
                is_min = True
                continue

            usernames = []
            phone_number = None

            if isinstance(peer, raw.types.User):
                peer_id = peer.id
                access_hash = peer.access_hash
                phone_number = peer.phone
                peer_type = "bot" if peer.bot else "user"

                if peer.username:
                    usernames.append(peer.username.lower())
                elif peer.usernames:
                    usernames.extend(username.username.lower() for username in peer.usernames)
            elif isinstance(peer, (raw.types.Chat, raw.types.ChatForbidden)):
                peer_id = -peer.id
                access_hash = 0
                peer_type = "group"
            elif isinstance(peer, raw.types.Channel):
                peer_id = utils.get_channel_id(peer.id)
                access_hash = peer.access_hash
                peer_type = "direct" if peer.monoforum else "channel" if peer.broadcast else "forum" if peer.forum else "supergroup"

                if peer.username:
                    usernames.append(peer.username.lower())
                elif peer.usernames:
                    usernames.extend(username.username.lower() for username in peer.usernames)
            elif isinstance(peer, raw.types.ChannelForbidden):
                peer_id = utils.get_channel_id(peer.id)
                access_hash = peer.access_hash
                peer_type = "channel" if peer.broadcast else "supergroup"
            else:
                continue

            parsed_peers.append((peer_id, access_hash, peer_type, phone_number))

            if usernames:
                parsed_usernames.append((peer_id, usernames))

        await self.storage.update_peers(parsed_peers)

        if parsed_usernames:
            await self.storage.update_usernames(parsed_usernames)

        return is_min

    async def handle_updates(self, updates):
        self.last_update_time = datetime.now()

        if isinstance(updates, (raw.types.Updates, raw.types.UpdatesCombined)):
            is_min = any((
                await self.fetch_peers(updates.users),
                await self.fetch_peers(updates.chats),
            ))

            users = {u.id: u for u in updates.users}
            chats = {c.id: c for c in updates.chats}

            for update in updates.updates:
                channel_id = getattr(
                    getattr(
                        getattr(
                            update, "message", None
                        ), "peer_id", None
                    ), "channel_id", None
                ) or getattr(update, "channel_id", None)

                pts = getattr(update, "pts", None)
                pts_count = getattr(update, "pts_count", None)

                if pts:
                    await self.storage.update_state(
                        (
                            utils.get_channel_id(channel_id) if channel_id else 0,
                            pts,
                            None,
                            updates.date,
                            updates.seq
                        )
                    )

                if isinstance(update, raw.types.UpdateChannelTooLong):
                    log.info(update)

                if isinstance(update, raw.types.UpdateNewChannelMessage) and is_min:
                    message = update.message

                    if not isinstance(message, raw.types.MessageEmpty):
                        try:
                            diff = await self.invoke(
                                raw.functions.updates.GetChannelDifference(
                                    channel=await self.resolve_peer(utils.get_channel_id(channel_id)),
                                    filter=raw.types.ChannelMessagesFilter(
                                        ranges=[raw.types.MessageRange(
                                            min_id=update.message.id,
                                            max_id=update.message.id
                                        )]
                                    ),
                                    pts=pts - pts_count,
                                    limit=pts,
                                    force=False
                                )
                            )
                        except (ChannelPrivate, PersistentTimestampOutdated, PersistentTimestampInvalid):
                            pass
                        else:
                            if not isinstance(diff, raw.types.updates.ChannelDifferenceEmpty):
                                users.update({u.id: u for u in diff.users})
                                chats.update({c.id: c for c in diff.chats})

                self.dispatcher.updates_queue.put_nowait((update, users, chats))
        elif isinstance(updates, (raw.types.UpdateShortMessage, raw.types.UpdateShortChatMessage)):
            await self.storage.update_state(
                (
                    0,
                    updates.pts,
                    None,
                    updates.date,
                    None
                )
            )

            diff = await self.invoke(
                raw.functions.updates.GetDifference(
                    pts=updates.pts - updates.pts_count,
                    date=updates.date,
                    qts=-1
                )
            )

            if diff.new_messages:
                self.dispatcher.updates_queue.put_nowait((
                    raw.types.UpdateNewMessage(
                        message=diff.new_messages[0],
                        pts=updates.pts,
                        pts_count=updates.pts_count
                    ),
                    {u.id: u for u in diff.users},
                    {c.id: c for c in diff.chats}
                ))
            else:
                if diff.other_updates:  # The other_updates list can be empty
                    self.dispatcher.updates_queue.put_nowait((diff.other_updates[0], {}, {}))
        elif isinstance(updates, raw.types.UpdateShort):
            self.dispatcher.updates_queue.put_nowait((updates.update, {}, {}))
        elif isinstance(updates, raw.types.UpdatesTooLong):
            log.info(updates)

    async def load_session(self):
        await self.storage.open()

        session_empty = any([
            await self.storage.test_mode() is None,
            await self.storage.auth_key() is None,
            await self.storage.user_id() is None,
            await self.storage.is_bot() is None
        ])

        if session_empty:
            if not self.api_id or not self.api_hash:
                raise AttributeError("The API key is required for new authorizations. "
                                     "More info: https://docs.pyrogram.org/start/auth")

            await self.storage.api_id(self.api_id)

            await self.storage.dc_id(2)

            if self.test_mode:
                await self.storage.server_address("2001:67c:4e8:f002::e" if self.ipv6 else "149.154.167.40")
                await self.storage.port(80)
            else:
                await self.storage.server_address("2001:67c:4e8:f002::a" if self.ipv6 else "149.154.167.51")
                await self.storage.port(443)

            await self.storage.date(0)

            await self.storage.test_mode(self.test_mode)
            await self.storage.auth_key(
                await Auth(
                    self,
                    await self.storage.dc_id(),
                    await self.storage.server_address(),
                    await self.storage.port(),
                    await self.storage.test_mode()
                ).create()
            )
            await self.storage.user_id(None)
            await self.storage.is_bot(None)
        else:
            # Needed for migration from storage v2 to v3
            if not await self.storage.api_id():
                if self.api_id:
                    await self.storage.api_id(self.api_id)
                else:
                    while True:
                        try:
                            value = int(await ainput("Enter the api_id part of the API key: ", loop=self.loop))

                            if value <= 0:
                                print("Invalid value")
                                continue

                            confirm = await ainput(f'Is "{value}" correct? (y/N): ', loop=self.loop)

                            if confirm.lower() == "y":
                                await self.storage.api_id(value)
                                break
                        except Exception as e:
                            print(e)

    def load_plugins(self):
        if self.plugins:
            plugins = self.plugins.copy()

            for option in ["include", "exclude"]:
                if plugins.get(option, []):
                    plugins[option] = [
                        (i.split()[0], i.split()[1:] or None)
                        for i in self.plugins[option]
                    ]
        else:
            return

        if plugins.get("enabled", True):
            root = plugins["root"]
            include = plugins.get("include", [])
            exclude = plugins.get("exclude", [])

            count = 0

            if not include:
                for path in sorted(Path(root.replace(".", "/")).rglob("*.py")):
                    module_path = '.'.join(path.parent.parts + (path.stem,))
                    module = import_module(module_path)

                    for name in vars(module).keys():
                        # noinspection PyBroadException
                        try:
                            for handler, group in getattr(module, name).handlers:
                                if isinstance(handler, Handler) and isinstance(group, int):
                                    self.add_handler(handler, group)

                                    log.info('[{}] [LOAD] {}("{}") in group {} from "{}"'.format(
                                        self.name, type(handler).__name__, name, group, module_path))

                                    count += 1
                        except Exception:
                            pass
            else:
                for path, handlers in include:
                    module_path = root + "." + path
                    warn_non_existent_functions = True

                    try:
                        module = import_module(module_path)
                    except ImportError:
                        log.warning('[%s] [LOAD] Ignoring non-existent module "%s"', self.name, module_path)
                        continue

                    if "__path__" in dir(module):
                        log.warning('[%s] [LOAD] Ignoring namespace "%s"', self.name, module_path)
                        continue

                    if handlers is None:
                        handlers = vars(module).keys()
                        warn_non_existent_functions = False

                    for name in handlers:
                        # noinspection PyBroadException
                        try:
                            for handler, group in getattr(module, name).handlers:
                                if isinstance(handler, Handler) and isinstance(group, int):
                                    self.add_handler(handler, group)

                                    log.info('[{}] [LOAD] {}("{}") in group {} from "{}"'.format(
                                        self.name, type(handler).__name__, name, group, module_path))

                                    count += 1
                        except Exception:
                            if warn_non_existent_functions:
                                log.warning('[{}] [LOAD] Ignoring non-existent function "{}" from "{}"'.format(
                                    self.name, name, module_path))

            if exclude:
                for path, handlers in exclude:
                    module_path = root + "." + path
                    warn_non_existent_functions = True

                    try:
                        module = import_module(module_path)
                    except ImportError:
                        log.warning('[%s] [UNLOAD] Ignoring non-existent module "%s"', self.name, module_path)
                        continue

                    if "__path__" in dir(module):
                        log.warning('[%s] [UNLOAD] Ignoring namespace "%s"', self.name, module_path)
                        continue

                    if handlers is None:
                        handlers = vars(module).keys()
                        warn_non_existent_functions = False

                    for name in handlers:
                        # noinspection PyBroadException
                        try:
                            for handler, group in getattr(module, name).handlers:
                                if isinstance(handler, Handler) and isinstance(group, int):
                                    self.remove_handler(handler, group)

                                    log.info('[{}] [UNLOAD] {}("{}") from group {} in "{}"'.format(
                                        self.name, type(handler).__name__, name, group, module_path))

                                    count -= 1
                        except Exception:
                            if warn_non_existent_functions:
                                log.warning('[{}] [UNLOAD] Ignoring non-existent function "{}" from "{}"'.format(
                                    self.name, name, module_path))

            if count > 0:
                log.info('[{}] Successfully loaded {} plugin{} from "{}"'.format(
                    self.name, count, "s" if count > 1 else "", root))
            else:
                log.warning('[%s] No plugin loaded from "%s"', self.name, root)

    async def handle_download(self, packet):
        file_id, directory, file_name, in_memory, file_size, progress, progress_args = packet

        os.makedirs(directory, exist_ok=True) if not in_memory else None
        temp_file_path = os.path.abspath(re.sub(r"[/\\]", "/", os.path.join(directory, file_name))) + ".temp"
        file = BytesIO() if in_memory else open(temp_file_path, "w+b")
        if not in_memory and file_size > 0:
            file.truncate(file_size)

        try:
            async for chunk in self.get_file(file_id, file_size, 0, 0, progress, progress_args, _write_file=None if in_memory else file):
                if in_memory:
                    file.write(chunk)
        except BaseException as e:
            if not in_memory:
                file.close()
                os.remove(temp_file_path)

            if isinstance(e, pyrogram.StopTransmission):
                return None

            raise e
        else:
            if in_memory:
                file.name = file_name
                return file
            else:
                file.close()
                file_path = os.path.splitext(temp_file_path)[0]
                shutil.move(temp_file_path, file_path)
                return file_path

    async def get_file(
        self,
        file_id: FileId,
        file_size: int = 0,
        limit: int = 0,
        offset: int = 0,
        progress: Optional[Callable] = None,
        progress_args: tuple = (),
        _write_file: object = None,
    ) -> AsyncGenerator[bytes, None]:
        async with self.get_file_semaphore:
            file_type = file_id.file_type

            if file_type == FileType.CHAT_PHOTO:
                if file_id.chat_id > 0:
                    peer = raw.types.InputPeerUser(
                        user_id=file_id.chat_id,
                        access_hash=file_id.chat_access_hash
                    )
                else:
                    if file_id.chat_access_hash == 0:
                        peer = raw.types.InputPeerChat(
                            chat_id=-file_id.chat_id
                        )
                    else:
                        peer = raw.types.InputPeerChannel(
                            channel_id=utils.get_channel_id(file_id.chat_id),
                            access_hash=file_id.chat_access_hash
                        )

                location = raw.types.InputPeerPhotoFileLocation(
                    peer=peer,
                    photo_id=file_id.media_id,
                    big=file_id.thumbnail_source == ThumbnailSource.CHAT_PHOTO_BIG
                )
            elif file_type == FileType.PHOTO:
                location = raw.types.InputPhotoFileLocation(
                    id=file_id.media_id,
                    access_hash=file_id.access_hash,
                    file_reference=file_id.file_reference,
                    thumb_size=file_id.thumbnail_size
                )
            else:
                location = raw.types.InputDocumentFileLocation(
                    id=file_id.media_id,
                    access_hash=file_id.access_hash,
                    file_reference=file_id.file_reference,
                    thumb_size=file_id.thumbnail_size
                )

            current = 0
            total = abs(limit) or (1 << 31) - 1
            chunk_size = 1024 * 1024
            offset_bytes = abs(offset) * chunk_size

            async def _report(sent: int) -> None:
                if not progress:
                    return

                func = functools.partial(
                    progress,
                    min(sent, file_size) if file_size else sent,
                    file_size,
                    *progress_args
                )

                try:
                    if inspect.iscoroutinefunction(progress):
                        await func()
                    elif self.executor is not None:
                        await self.loop.run_in_executor(self.executor, func)
                    else:
                        func()
                except pyrogram.StopTransmission:
                    raise
                except Exception as e:
                    log.warning(f"Download progress callback error: {e}")

            dc_id = file_id.dc_id
            pool_lease = contextlib.AsyncExitStack()

            try:
                _is_bot = getattr(self.me, "is_bot", False)
                _is_premium = getattr(self.me, "is_premium", False)

                if _is_bot:
                    dl_pool_size = int(os.environ.get("KURIGRAM_DL_POOL_BOT", 5))
                    dl_workers_per_session = int(os.environ.get("KURIGRAM_DL_WORKERS_BOT", 3))
                    dl_rate = int(os.environ.get("KURIGRAM_DL_RATE_BOT", 100))
                    dl_burst = int(os.environ.get("KURIGRAM_DL_BURST_BOT", 25))
                elif _is_premium:
                    dl_pool_size = int(os.environ.get("KURIGRAM_DL_POOL_PREMIUM", 6))
                    dl_workers_per_session = int(os.environ.get("KURIGRAM_DL_WORKERS_PREMIUM", 4))
                    dl_rate = int(os.environ.get("KURIGRAM_DL_RATE_PREMIUM", 150))
                    dl_burst = int(os.environ.get("KURIGRAM_DL_BURST_PREMIUM", 35))
                else:
                    dl_pool_size = int(os.environ.get("KURIGRAM_DL_POOL_USER", 5))
                    dl_workers_per_session = int(os.environ.get("KURIGRAM_DL_WORKERS_USER", 3))
                    dl_rate = int(os.environ.get("KURIGRAM_DL_RATE_USER", 100))
                    dl_burst = int(os.environ.get("KURIGRAM_DL_BURST_USER", 25))

                total_chunks = math.ceil((file_size - offset_bytes) / chunk_size) if file_size > 0 else 0
                pool_size = min(dl_pool_size, total_chunks) if total_chunks > 0 else 1
                needs_pool = min(total, total_chunks) > 1 if total_chunks > 0 else False

                if needs_pool and hasattr(self, "_media_pool"):
                    pool_task = await pool_lease.enter_async_context(
                        self._media_pool(dc_id, pool_size)
                    )
                else:
                    pool_task = None

                session = await self.get_session(dc_id, is_media=True)

                _write_mode = _write_file is not None and file_size > 0
                _write_fd = _write_file.fileno() if _write_mode and hasattr(_write_file, "fileno") else -1
                if _write_fd < 0:
                    _write_mode = False

                data_ready = asyncio.Event()
                buffer_slots = ReadAhead(self.read_ahead_slots)
                received = {}
                work = asyncio.Queue()
                tasks = []
                _done_count = 0
                _total_chunks = 0
                _getfile_rate = TokenBucket(rate=dl_rate, burst=dl_burst)
                _last_rate_adj = 0.0
                _fast_window = 0

                async def _worker(pool, i):
                    nonlocal _done_count, _last_rate_adj, _fast_window
                    window = media_window(getattr(pool[0], "auth_key", b""), dc_id)

                    while True:
                        await buffer_slots.acquire()

                        try:
                            offset_val = work.get_nowait()
                        except asyncio.QueueEmpty:
                            buffer_slots.release()
                            return

                        sess = window.pick(pool, i)

                        try:
                            await _getfile_rate.acquire()
                            t0 = time.monotonic()
                            try:
                                res = await sess.invoke(
                                    raw.functions.upload.GetFile(
                                        location=location,
                                        offset=offset_val,
                                        limit=chunk_size,
                                    ),
                                    timeout=Session.MEDIA_WAIT_TIMEOUT,
                                    sleep_threshold=30,
                                )
                            except TypeError:
                                res = await sess.invoke(
                                    raw.functions.upload.GetFile(
                                        location=location,
                                        offset=offset_val,
                                        limit=chunk_size,
                                    ),
                                    sleep_threshold=30,
                                )
                        except BaseException:
                            buffer_slots.release()
                            raise

                        chunk_data = res.bytes
                        res = None
                        t1 = time.monotonic()

                        if _write_mode:
                            write_at(_write_fd, chunk_data, offset_val)
                            buffer_slots.release()
                        else:
                            received[offset_val] = chunk_data

                        _done_count += 1
                        data_ready.set()

                        chunk_len = len(chunk_data)
                        chunk_data = None

                        if chunk_len < chunk_size:
                            return

                        elapsed = t1 - t0
                        now = t1
                        if elapsed > 2.0 and now - _last_rate_adj > 0.5:
                            _last_rate_adj = now
                            _fast_window = 0
                            _getfile_rate.rate = max(_getfile_rate.rate * 0.8, 3.0)
                        elif elapsed < 0.5:
                            _fast_window += 1
                            if _fast_window >= 5 and now - _last_rate_adj > 0.5:
                                _last_rate_adj = now
                                _getfile_rate.rate = min(_getfile_rate.rate + 2.0, dl_rate)
                                _fast_window = 0
                        else:
                            _fast_window = 0

                async def _launch(start):
                    nonlocal _total_chunks
                    chunks_needed = min(
                        total - 1,
                        math.ceil((file_size - start) / chunk_size),
                    )

                    if chunks_needed <= 0:
                        return []

                    if pool_task is not None:
                        pool = await pool_task
                    else:
                        pool = [session]

                    n_sessions = len(pool)
                    if not n_sessions:
                        return []

                    _total_chunks = chunks_needed

                    for i in range(chunks_needed):
                        work.put_nowait(start + i * chunk_size)

                    started = [
                        asyncio.ensure_future(_worker(pool, i))
                        for i in range(
                            min(dl_pool_size * dl_workers_per_session, chunks_needed)
                        )
                    ]

                    for t in started:
                        t.add_done_callback(lambda _: data_ready.set())

                    return started

                _prefetch = (
                    asyncio.ensure_future(_launch(offset_bytes + chunk_size))
                    if needs_pool and file_size > 0 and total > 1
                    else None
                )

                async def _drop_prefetch():
                    nonlocal _prefetch

                    if _prefetch is None:
                        return

                    pending, _prefetch = _prefetch, None
                    pending.cancel()
                    outcome = (await asyncio.gather(pending, return_exceptions=True))[0]
                    started = outcome if isinstance(outcome, list) else []

                    for t in started:
                        t.cancel()

                    if started:
                        await asyncio.gather(*started, return_exceptions=True)

                    buffer_slots.release_all()

                try:
                    try:
                        r = await session.invoke(
                            raw.functions.upload.GetFile(
                                location=location,
                                offset=offset_bytes,
                                limit=chunk_size
                            ),
                            timeout=Session.MEDIA_WAIT_TIMEOUT,
                            sleep_threshold=30
                        )
                    except TypeError:
                        r = await session.invoke(
                            raw.functions.upload.GetFile(
                                location=location,
                                offset=offset_bytes,
                                limit=chunk_size
                            ),
                            sleep_threshold=30
                        )
                except BaseException:
                    await _drop_prefetch()
                    raise

                if isinstance(r, raw.types.upload.File):
                    first_chunk = r.bytes
                    r = None

                    try:
                        yield first_chunk
                        current += 1
                        offset_bytes += chunk_size
                        if _write_file is not None:
                            _write_file.seek(0)
                            _write_file.write(first_chunk)

                        first_len = len(first_chunk)
                        first_chunk = None

                        await _report(offset_bytes)
                    except BaseException:
                        await _drop_prefetch()
                        raise

                    if not first_len or first_len < chunk_size or current >= total:
                        await _drop_prefetch()
                        return

                    # Sequential fallback when file size is unknown
                    if file_size <= 0:
                        while current < total:
                            try:
                                res = await session.invoke(
                                    raw.functions.upload.GetFile(
                                        location=location,
                                        offset=offset_bytes,
                                        limit=chunk_size,
                                    ),
                                    timeout=Session.MEDIA_WAIT_TIMEOUT,
                                    sleep_threshold=30,
                                )
                            except TypeError:
                                res = await session.invoke(
                                    raw.functions.upload.GetFile(
                                        location=location,
                                        offset=offset_bytes,
                                        limit=chunk_size,
                                    ),
                                    sleep_threshold=30,
                                )
                            chunk = res.bytes
                            if not chunk:
                                return
                            yield chunk
                            if _write_file is not None:
                                _write_file.write(chunk)
                            current += 1
                            offset_bytes += chunk_size

                            await _report(offset_bytes)

                            if len(chunk) < chunk_size or current >= total:
                                return
                        return

                    if _prefetch is not None:
                        pending, _prefetch = _prefetch, None
                        tasks = await pending
                    else:
                        tasks = await _launch(offset_bytes)

                    _reported_count = -1

                    try:
                        while current < total:
                            if _write_mode:
                                if _done_count >= _total_chunks:
                                    await _report(offset_bytes + _done_count * chunk_size)
                                    return
                                for t in tasks:
                                    if t.done() and not t.cancelled():
                                        exc = t.exception()
                                        if exc is not None:
                                            raise exc
                                if all(t.done() for t in tasks):
                                    return
                                try:
                                    await asyncio.wait_for(data_ready.wait(), 0.5)
                                except asyncio.TimeoutError:
                                    pass
                                data_ready.clear()

                                if _done_count != _reported_count:
                                    _reported_count = _done_count
                                    await _report(offset_bytes + _done_count * chunk_size)

                                yield b""
                            else:
                                while offset_bytes not in received:
                                    for t in tasks:
                                        if t.done() and not t.cancelled():
                                            exc = t.exception()
                                            if exc is not None:
                                                raise exc
                                    if all(t.done() for t in tasks):
                                        return
                                    await data_ready.wait()
                                    data_ready.clear()

                                chunk = received.pop(offset_bytes)
                                buffer_slots.release()
                                yield chunk
                                current += 1
                                offset_bytes += chunk_size

                                await _report(offset_bytes)

                                if len(chunk) < chunk_size or current >= total:
                                    return
                    finally:
                        for t in tasks:
                            if not t.done():
                                t.cancel()
                        buffer_slots.release_all()

                elif isinstance(r, raw.types.upload.FileCdnRedirect):

                    cdn_session = await self.get_session(dc_id, is_cdn=True, temporary=True)

                    try:
                        while True:
                            r2 = await cdn_session.invoke(
                                raw.functions.upload.GetCdnFile(
                                    file_token=r.file_token,
                                    offset=offset_bytes,
                                    limit=chunk_size
                                )
                            )

                            if isinstance(r2, raw.types.upload.CdnFileReuploadNeeded):
                                try:
                                    await session.invoke(
                                        raw.functions.upload.ReuploadCdnFile(
                                            file_token=r.file_token,
                                            request_token=r2.request_token
                                        )
                                    )
                                except VolumeLocNotFound:
                                    break
                                else:
                                    continue

                            chunk = r2.bytes

                            # https://core.telegram.org/cdn#decrypting-files
                            decrypted_chunk = await self.loop.run_in_executor(
                                self.executor,
                                aes.ctr256_decrypt,
                                chunk,
                                r.encryption_key,
                                bytearray(r.encryption_iv[:-4] + (offset_bytes // 16).to_bytes(4, "big"))
                            )

                            hashes = await session.invoke(
                                raw.functions.upload.GetCdnFileHashes(
                                    file_token=r.file_token,
                                    offset=offset_bytes
                                )
                            )

                            # https://core.telegram.org/cdn#verifying-files
                            def _check_all_hashes():
                                for i, h in enumerate(hashes):
                                    cdn_chunk = decrypted_chunk[h.limit * i: h.limit * (i + 1)]
                                    CDNFileHashMismatch.check(
                                        h.hash == sha256(cdn_chunk).digest(),
                                        "h.hash == sha256(cdn_chunk).digest()"
                                    )

                            await self.loop.run_in_executor(self.executor, _check_all_hashes)

                            yield decrypted_chunk

                            current += 1
                            offset_bytes += chunk_size

                            if progress:
                                func = functools.partial(
                                    progress,
                                    min(offset_bytes, file_size) if file_size != 0 else offset_bytes,
                                    file_size,
                                    *progress_args
                                )

                                if inspect.iscoroutinefunction(progress):
                                    await func()
                                else:
                                    await self.loop.run_in_executor(self.executor, func)

                            if len(chunk) < chunk_size or current >= total:
                                break
                    except Exception as e:
                        raise e
                    finally:
                        await cdn_session.stop()
            except Exception as e:
                raise e

    async def get_session(
        self,
        dc_id: Optional[int] = None,
        is_media: Optional[bool] = False,
        is_cdn: Optional[bool] = False,
        business_connection_id: Optional[str] = None,
        export_authorization: Optional[bool] = True,
        server_address: Optional[str] = None,
        port: Optional[int] = None,
        temporary: Optional[bool] = False
    ) -> "Session":
        """Get existing session or create a new one.

        Parameters:
            dc_id (``int``, *optional*):
                Datacenter identifier.

            is_media (``bool``, *optional*):
                Pass True to get or create a media session.

            is_cdn (``bool``, *optional*):
                Pass True to get or create a cdn session.

            business_connection_id (``str``, *optional*):
                Business connection identifier.

            export_authorization (``bool``, *optional*):
                Pass True to export authorization after creating the session.
                Used only when creating a new session.

            server_address (``str``, *optional*):
                Custom server address to connect to.
                Used only when creating a new session.

            port (``int``, *optional*):
                Custom port to connect to.
                Used only when creating a new session.

            temporary (``bool``, *optional*):
                Create temporary session instead of getting from storage.
                Used only when uploading/downloading and don't forget to stop it.
        """
        if not dc_id:
            dc_id = await self.storage.dc_id()

        if business_connection_id:
            dc_id = self.business_connections.get(business_connection_id)

            if dc_id is None:
                connection = await self.session.invoke(
                    raw.functions.account.GetBotBusinessConnection(
                        connection_id=business_connection_id
                    )
                )

                dc_id = self.business_connections[business_connection_id] = connection.updates[0].connection.dc_id

        is_current_dc = await self.storage.dc_id() == dc_id

        if not temporary and is_current_dc and not is_media:
            return self.session

        sessions = self.media_sessions if is_media else self.sessions

        if not temporary and sessions.get(dc_id):
            return sessions[dc_id]

        if not server_address or not port:
            dc_option = await self.get_dc_option(dc_id, is_media=is_media, ipv6=self.ipv6, is_cdn=is_cdn)

            server_address = server_address or dc_option.ip_address
            port = port or dc_option.port

        if is_media:
            auth_key = (await self.get_session(dc_id)).auth_key
        else:
            if not is_current_dc:
                auth_key = await Auth(
                    self,
                    dc_id,
                    server_address,
                    port,
                    await self.storage.test_mode()
                ).create()
            else:
                auth_key = await self.storage.auth_key()

        session = Session(
            self,
            dc_id,
            server_address,
            port,
            auth_key,
            await self.storage.test_mode(),
            is_media=is_media
        )

        if not temporary:
            sessions[dc_id] = session

        await session.start()

        if not is_current_dc and export_authorization:
            for _ in range(3):
                exported_auth = await self.invoke(
                    raw.functions.auth.ExportAuthorization(
                        dc_id=dc_id
                    )
                )

                try:
                    await session.invoke(
                        raw.functions.auth.ImportAuthorization(
                            id=exported_auth.id,
                            bytes=exported_auth.bytes
                        )
                    )
                except AuthBytesInvalid:
                    continue
                else:
                    break
            else:
                await session.stop()
                raise AuthBytesInvalid

        return session

    async def _make_media_session(
        self,
        dc_id: int,
        auth_key: bytes,
        server_address: Optional[str] = None,
        port: Optional[int] = None
    ) -> "Session":
        session = Session(
            self,
            dc_id,
            server_address,
            port,
            auth_key,
            await self.storage.test_mode(),
            is_media=True
        )
        await session.start()
        return session

    @contextlib.asynccontextmanager
    async def _media_pool(self, dc_id: int, n: int):
        self._media_pool_demand[dc_id] = self._media_pool_demand.get(dc_id, 0) + n
        task = asyncio.ensure_future(
            self._get_media_session_pool(
                dc_id, min(self._media_pool_demand[dc_id], self.MEDIA_POOL_CAP)
            )
        )
        task.add_done_callback(lambda t: t.cancelled() or t.exception())

        try:
            yield task
        finally:
            remaining = self._media_pool_demand.get(dc_id, n) - n

            if remaining > 0:
                self._media_pool_demand[dc_id] = remaining
            else:
                self._media_pool_demand.pop(dc_id, None)

    async def _get_media_session_pool(self, dc_id: int, n: int) -> list:
        lock = self._media_sessions_locks.setdefault(dc_id, asyncio.Lock())
        async with lock:
            media = await self.get_session(dc_id, is_media=True)
            if not hasattr(media, "auth_key") or not isinstance(media.auth_key, (bytes, bytearray)):
                return [media]

            window = media_window(media.auth_key, dc_id)
            window.fixed = bool(getattr(self.me, "is_premium", False))
            n = window.connections(n)
            extras = []

            for session in self.media_session_pools.get(dc_id, []):
                if getattr(session, "is_closed", False):
                    self.loop.create_task(session.stop())
                elif len(extras) >= window.size - 1 and not getattr(session, "results", None):
                    self.loop.create_task(session.stop())
                else:
                    extras.append(session)

            needed = n - 1 - len(extras)

            while needed > 0:
                chunk = min(needed, 3)
                async with self._session_creation_gate:
                    extras.extend(await asyncio.gather(*(
                        self._make_media_session(
                            dc_id, media.auth_key, media.server_address, media.port
                        )
                        for _ in range(chunk)
                    )))
                needed -= chunk

            self.media_session_pools[dc_id] = extras
            return [media] + extras[:n - 1]


    async def get_dc_option(
        self,
        dc_id: int = None,
        is_media: bool = False,
        is_cdn: bool = False,
        ipv6: bool = False
    ) -> "raw.types.DcOption":
        self.__config = await self.invoke(raw.functions.help.GetConfig())

        if dc_id is None:
            dc_id = self.__config.this_dc

        options = [dc for dc in self.__config.dc_options if dc.id == dc_id and dc.ipv6 == ipv6] # type: List[raw.types.DcOption]

        if not options:
            raise ValueError(f"DC{dc_id} not found")

        if is_cdn:
            cdn_options = [dc for dc in options if dc.cdn]

            if cdn_options:
                return cdn_options[0]

            log.debug(
                "No CDN datacenter found for DC%s, falling back to media DC",
                dc_id
            )

            is_media = True

        if is_media:
            media_options = [dc for dc in options if dc.media_only]

            if media_options:
                return media_options[0]

            log.debug(
                "No media datacenter found for DC%s, falling back to prod DC",
                dc_id
            )

        prod_options = [dc for dc in options if not dc.media_only]

        if prod_options:
            return prod_options[0]

        raise ValueError("No suitable DC found")

    async def set_dc(
        self,
        dc_id: Optional[int] = None,
        server_address: Optional[str] = None,
        port: Optional[int] = None
    ):
        """Set configuration for the specified datacenter.

        .. note::

            Be careful with this method, you can easily break your session.

        Parameters:
            dc_id (``int``, *optional*):
                Datacenter identifier.
                Defaults to the current datacenter.

            server_address (``str``, *optional*):
                Custom server address.

            port (``int``, *optional*):
                Custom port.
        """
        if not self.__config:
            self.__config = await self.invoke(raw.functions.help.GetConfig())

        dc_id = dc_id or self.__config.this_dc
        dc_option = await self.get_dc_option(dc_id, ipv6=self.ipv6)

        server_address = server_address or dc_option.ip_address
        port = port or dc_option.port

        await self.storage.dc_id(dc_id)
        await self.storage.server_address(server_address)
        await self.storage.port(port)

        if self.session.server_address != server_address or self.session.port != port:
            self.session.server_address = server_address
            self.session.port = port

            await self.session.restart()
            log.info("Changed session DC%s address to %s:%s", dc_id, server_address, port)
        else:
            log.info("Session DC%s address is already %s:%s", dc_id, server_address, port)

    @property
    def server_time(self) -> float:
        return time.time() + self._server_time_offset

    def _set_server_time(self, msg_id: int):
        server_ts = msg_id / float(2**32)
        self._server_time_offset = server_ts - time.time()
        log.info(f"Time synced: offset={self._server_time_offset:.3f}s, server_time={utils.timestamp_to_datetime(server_ts)}")

    def guess_mime_type(self, filename: Union[str, BytesIO]) -> Optional[str]:
        if isinstance(filename, BytesIO):
            return self.mimetypes.guess_type(filename.name)[0]

        return self.mimetypes.guess_type(filename)[0]

    def guess_extension(self, mime_type: str) -> Optional[str]:
        return self.mimetypes.guess_extension(mime_type)


class Cache:
    def __init__(self, capacity: int):
        self.capacity = capacity
        self.store = {}

    def __getitem__(self, key):
        return self.store.get(key, None)

    def __setitem__(self, key, value):
        if key in self.store:
            del self.store[key]

        self.store[key] = value

        if len(self.store) > self.capacity:
            for _ in range(self.capacity // 2 + 1):
                del self.store[next(iter(self.store))]
