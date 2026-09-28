import pytest
import os
import pyrogram
from pyrogram import Client, enums, types, raw
from pyrogram.crypto import aes


def test_hypercrypto_aes_ige():
    data = b"Hello, Telegram! HyperCrypto test 16b"[:32]
    key = b"k" * 32
    iv = b"i" * 32

    encrypted = aes.ige256_encrypt(data, key, iv)
    assert len(encrypted) == len(data)
    decrypted = aes.ige256_decrypt(encrypted, key, iv)
    assert decrypted == data


def test_hypercrypto_aes_ctr():
    data = b"Streaming data for MTProto transport encryption via HyperCrypto!"
    key = b"k" * 32
    iv = bytearray(b"i" * 16)
    state = bytearray(1)

    encrypted = aes.ctr256_encrypt(data, key, iv, state)
    assert len(encrypted) == len(data)

    iv2 = bytearray(b"i" * 16)
    state2 = bytearray(1)
    decrypted = aes.ctr256_decrypt(encrypted, key, iv2, state2)
    assert decrypted == data


def test_bot_api_enums():
    assert hasattr(enums.ButtonStyle, "LINK")
    assert enums.ButtonStyle.LINK.name == "LINK"

    assert hasattr(enums, "RichBlockType")
    assert enums.RichBlockType.PARAGRAPH.name == "PARAGRAPH"
    assert enums.RichBlockType.TABLE.name == "TABLE"
    assert enums.RichBlockType.BUTTONS.name == "BUTTONS"

    assert hasattr(enums, "InputRichBlockType")
    assert enums.InputRichBlockType.PHOTO.name == "PHOTO"
    assert enums.InputRichBlockType.DETAILS.name == "DETAILS"

    assert hasattr(enums, "RichTextType")
    assert enums.RichTextType.BOLD.name == "BOLD"
    assert enums.RichTextType.CODE.name == "CODE"


def test_inline_keyboard_button_disabled():
    btn = types.InlineKeyboardButton(text="Click", disabled=True)
    assert btn.disabled is True

    btn_default = types.InlineKeyboardButton(text="Click")
    assert btn_default.disabled is None


def test_keyboard_force_reply():
    fr = types.ForceReply(selective=True)
    ikb = types.InlineKeyboardMarkup(inline_keyboard=[[]], force_reply=fr)
    assert ikb.force_reply is fr

    rkm = types.ReplyKeyboardMarkup(keyboard=[["Button"]], force_reply=fr)
    assert rkm.force_reply is fr


def test_bot_command_ephemeral():
    cmd = types.BotCommand(command="help", description="Get help", is_ephemeral=True)
    assert cmd.is_ephemeral is True


def test_chat_admin_rights_welcome_messages():
    rights = types.ChatAdministratorRights(can_send_welcome_messages=True)
    assert rights.can_send_welcome_messages is True


def test_reply_parameters_ephemeral_id():
    rp = types.ReplyParameters(message_id=1, ephemeral_message_id=456)
    assert rp.ephemeral_message_id == 456


def test_community_types():
    comm = types.Community(id=101, name="My Community")
    assert comm.id == 101
    assert comm.name == "My Community"

    chat = types.Chat(id=-100123456789, type=enums.ChatType.SUPERGROUP, community=comm)
    assert chat.community is comm

    added = types.CommunityChatAdded(community=comm)
    assert added.community is comm

    removed = types.CommunityChatRemoved()
    assert isinstance(removed, types.CommunityChatRemoved)

    joined = types.CommunityChatJoined()
    assert isinstance(joined, types.CommunityChatJoined)


def test_bot_subscription_updated():
    user = types.User(id=999, first_name="Subscriber")
    sub = types.BotSubscriptionUpdated(user=user, invoice_payload="payload123", state="active")
    assert sub.user.id == 999
    assert sub.invoice_payload == "payload123"
    assert sub.state == "active"


def test_unique_gift_info():
    info = types.UniqueGiftInfo(
        origin="transfer",
        last_resale_currency="XTR",
        last_resale_amount=500,
        text="Gift message",
        is_private=False,
    )
    assert info.origin == "transfer"
    assert info.last_resale_currency == "XTR"
    assert info.last_resale_amount == 500
    assert info.text == "Gift message"
    assert info.is_private is False


def test_ephemeral_message_parameters():
    params = types.EphemeralMessageParameters(
        receiver_user_id=123,
        callback_query_id="cb_id_1",
        replace_callback_query_message=True,
    )
    assert params.receiver_user_id == 123
    assert params.callback_query_id == "cb_id_1"
    assert params.replace_callback_query_message is True


def test_message_generation_stopped():
    chat = types.Chat(id=1, type=enums.ChatType.PRIVATE)
    stopped = types.MessageGenerationStopped(chat=chat, draft_id=42, message_thread_id=5)
    assert stopped.draft_id == 42
    assert stopped.message_thread_id == 5


def test_rich_message_and_blocks():
    text_bold = types.RichTextBold(text="Headline")
    assert text_bold.type == enums.RichTextType.BOLD
    assert text_bold.text == "Headline"

    p_block = types.RichBlockParagraph(text=text_bold)
    assert p_block.type == enums.RichBlockType.PARAGRAPH

    btn = types.RichMessageButton(text="Open", url="https://telegram.org")
    assert btn.text == "Open"
    assert btn.url == "https://telegram.org"

    buttons_block = types.RichBlockButtons(buttons=[[btn]])
    assert buttons_block.type == enums.RichBlockType.BUTTONS

    rich_msg = types.RichMessage(blocks=[p_block, buttons_block], is_rtl=False)
    assert len(rich_msg.blocks) == 2
    assert rich_msg.is_rtl is False

    input_msg = types.InputRichMessage(markdown="**bold**", is_rtl=True)
    assert input_msg.markdown == "**bold**"
    assert input_msg.is_rtl is True


def test_message_ephemeral_and_rich_fields():
    user = types.User(id=777, first_name="Alice")
    comm = types.Community(id=1, name="Devs")
    added = types.CommunityChatAdded(community=comm)

    msg = types.Message(
        id=1234,
        receiver_user=user,
        ephemeral_message_id=9876,
        community_chat_added=added,
    )
    assert msg.receiver_user.id == 777
    assert msg.ephemeral_message_id == 9876
    assert msg.community_chat_added.community.name == "Devs"
    assert hasattr(msg, "edit_ephemeral_text")
    assert hasattr(msg, "edit_ephemeral_caption")
    assert hasattr(msg, "edit_ephemeral_media")
    assert hasattr(msg, "edit_ephemeral_reply_markup")
    assert hasattr(msg, "delete_ephemeral")
    assert hasattr(msg, "reply_rich")


def test_client_methods_available():
    app = Client("test_session")
    for method in [
        "send_rich_message",
        "send_rich_message_draft",
        "edit_ephemeral_message_text",
        "edit_ephemeral_message_caption",
        "edit_ephemeral_message_media",
        "edit_ephemeral_message_reply_markup",
        "delete_ephemeral_message",
        "send_message_draft",
        "answer_chat_join_request_query",
        "send_chat_join_request_web_app",
    ]:
        assert hasattr(app, method), f"Client is missing method: {method}"


def test_callback_query_ephemeral():
    user = types.User(id=98765, first_name="Test")
    cb = types.CallbackQuery(id="cb123", from_user=user, chat_instance="inst1")
    params = cb.as_ephemeral_message_parameters(replace_callback_query_message=True)
    assert isinstance(params, types.EphemeralMessageParameters)
    assert params.receiver_user_id == 98765
    assert params.callback_query_id == "cb123"
    assert params.replace_callback_query_message is True
    assert hasattr(cb, "reply_ephemeral")


def test_fs_input_file_and_buffered_input_file(tmp_path):
    fpath = tmp_path / "test.txt"
    fpath.write_text("hello kurigram")
    fs_file = types.FSInputFile(fpath)
    assert fs_file.filename == "test.txt"
    assert fs_file.path == str(fpath)
    assert fs_file.read() == b"hello kurigram"
    assert str(fs_file) == str(fpath)
    assert os.fspath(fs_file) == str(fpath)

    buf_file = types.BufferedInputFile(b"test data", filename="data.bin")
    assert buf_file.filename == "data.bin"
    bio = buf_file.to_io()
    assert bio.read() == b"test data"
    assert bio.name == "data.bin"


def test_user_requested_types_exported():
    required_names = [
        "CallbackQuery",
        "EphemeralMessageParameters",
        "FSInputFile",
        "InputRichBlockBlockQuotation",
        "InputRichBlockButtons",
        "InputRichBlockParagraph",
        "InputRichBlockSectionHeading",
        "InputRichMessage",
        "Message",
        "RichMessageButton",
        "RichText",
    ]
    for name in required_names:
        assert hasattr(types, name), f"pyrogram.types missing {name}"


def test_unique_gifts_and_prepared_types():
    assert hasattr(types, "DisabledButton")
    assert hasattr(types, "CopyTextButton")
    assert hasattr(types, "PreparedKeyboardButton")
    assert hasattr(types, "PreparedInlineMessage")
    assert hasattr(types, "UniqueGift")
    assert hasattr(types, "UniqueGiftModel")
    assert hasattr(types, "UniqueGiftSymbol")
    assert hasattr(types, "UniqueGiftBackdrop")
    assert hasattr(types, "UniqueGiftColors")
    assert hasattr(types, "GiftInfo")
    assert hasattr(types, "OwnedGift")
    assert hasattr(types, "OwnedGiftRegular")
    assert hasattr(types, "OwnedGiftUnique")
    assert hasattr(types, "OwnedGifts")
    assert hasattr(types, "Gifts")
    assert hasattr(types, "UserProfileAudios")
    assert hasattr(types, "StarTransaction")
    assert hasattr(types, "StarTransactions")

    copy_btn = types.CopyTextButton(text="copy me")
    btn = types.InlineKeyboardButton(text="Copy", copy_text=copy_btn)
    assert btn.copy_text == "copy me"


def test_message_as_reply_parameters():
    msg = types.Message(id=42, ephemeral_message_id=999)
    rp_eph = msg.as_reply_parameters()
    assert rp_eph.ephemeral_message_id == 999
    assert rp_eph.message_id is None

    msg2 = types.Message(id=101)
    rp_reg = msg2.as_reply_parameters()
    assert rp_reg.message_id == 101
    assert rp_reg.ephemeral_message_id is None


def test_client_bot_api_10_methods():
    app = Client("test_session")
    for method in [
        "save_prepared_inline_message",
        "save_prepared_keyboard_button",
        "get_star_transactions",
        "get_my_star_balance",
        "get_user_profile_audios",
    ]:
        assert hasattr(app, method), f"Client is missing: {method}"


@pytest.mark.asyncio
async def test_message_parse_and_rich_message_parse():
    app = Client("test_session")
    raw_msg = raw.types.Message(
        id=1,
        peer_id=raw.types.PeerUser(user_id=123),
        date=1600000000,
        message="hello world",
        entities=[],
    )
    users = {123: raw.types.User(id=123, access_hash=0, first_name="Test")}
    chats = {}
    parsed = await types.Message._parse(app, raw_msg, users, chats)
    assert parsed.id == 1
    assert parsed.text == "hello world"
    assert parsed.rich_message is None

    empty = raw.types.MessageEmpty(id=2)
    parsed_empty = await types.Message._parse(app, empty, users, chats)
    assert parsed_empty.empty is True

    # Test RichMessage._parse
    assert types.RichMessage._parse(app, None) is None
    rm = types.RichMessage()
    assert types.RichMessage._parse(app, rm) is rm
    parsed_dict = types.RichMessage._parse(app, {"blocks": [], "is_rtl": True})
    assert parsed_dict.is_rtl is True


def test_paid_media_live_photo_and_inputs():
    pmlp = types.PaidMediaLivePhoto(
        photo=types.Photo(file_id="photo123", file_unique_id="u123", width=100, height=100, file_size=1024, date=0),
        video=types.Video(file_id="vid123", file_unique_id="uv123", width=100, height=100, duration=3, file_size=2048, date=0, codec="h264")
    )
    assert pmlp.photo.file_id == "photo123"
    assert pmlp.video.file_id == "vid123"

    inp_lp = types.InputPaidMediaLivePhoto(media="photo.jpg", video="video.mp4")
    assert inp_lp.media == "photo.jpg"
    assert inp_lp.video == "video.mp4"

    inp_photo = types.InputPaidMediaPhoto(media="photo.jpg")
    assert inp_photo.media == "photo.jpg"

    inp_video = types.InputPaidMediaVideo(media="video.mp4")
    assert inp_video.media == "video.mp4"


@pytest.mark.asyncio
async def test_input_media_voice_note():
    import io
    bio = io.BytesIO(b"dummy ogg audio")
    bio.name = "voice.ogg"
    vm = types.InputMediaVoiceNote(media=bio, duration=15)
    assert vm.duration == 15
    assert vm.media is bio

    class DummyClient:
        async def save_file(self, path, progress=None, progress_args=()):
            return raw.types.InputFile(id=1, parts=1, name="voice.ogg", md5_checksum="")

        async def invoke(self, query):
            assert isinstance(query, raw.functions.messages.UploadMedia)
            assert isinstance(query.media, raw.types.InputMediaUploadedDocument)
            assert query.media.mime_type == "audio/ogg"
            has_voice = any(
                isinstance(a, raw.types.DocumentAttributeAudio) and a.voice is True
                for a in query.media.attributes
            )
            assert has_voice
            doc = raw.types.Document(
                id=12345,
                access_hash=67890,
                file_reference=b"ref",
                date=0,
                mime_type="audio/ogg",
                size=100,
                dc_id=1,
                attributes=[],
            )
            return raw.types.MessageMediaDocument(document=doc)

    raw_media = await vm.write(DummyClient())
    assert isinstance(raw_media, raw.types.InputMediaDocument)
    assert raw_media.id.id == 12345


def test_external_reply_info_live_photo():
    eri = types.ExternalReplyInfo(
        origin=types.MessageOriginUser(date=0, sender_user=types.User(id=1, first_name="X")),
        live_photo=types.LivePhoto(
            photo=types.Photo(file_id="p1", file_unique_id="up1", width=10, height=10, file_size=100, date=0),
            video=types.Video(file_id="v1", file_unique_id="uv1", width=10, height=10, duration=2, file_size=200, date=0, codec="h264")
        )
    )
    assert eri.live_photo is not None
    assert eri.live_photo.photo.file_id == "p1"
    assert eri.message_id is None


def test_rich_text_parse_raw_types():
    app = Client("test_session")
    # TextBold
    tb = raw.types.TextBold(text=raw.types.TextPlain(text="hello"))
    parsed_tb = types.RichText._parse(app, tb)
    assert isinstance(parsed_tb, types.RichTextBold)
    assert parsed_tb.text == "hello"

    # TextItalic
    ti = raw.types.TextItalic(text=raw.types.TextPlain(text="italic"))
    parsed_ti = types.RichText._parse(app, ti)
    assert isinstance(parsed_ti, types.RichTextItalic)
    assert parsed_ti.text == "italic"

    # TextUrl
    tu = raw.types.TextUrl(text=raw.types.TextPlain(text="link"), url="https://example.com", webpage_id=0)
    parsed_tu = types.RichText._parse(app, tu)
    assert isinstance(parsed_tu, types.RichTextUrl)
    assert parsed_tu.url == "https://example.com"
    assert parsed_tu.text == "link"

    # TextMention
    tm = raw.types.TextMention(text=raw.types.TextPlain(text="@bot"))
    parsed_tm = types.RichText._parse(app, tm)
    assert isinstance(parsed_tm, types.RichTextMention)
    assert parsed_tm.text == "@bot"


def test_rich_block_parse_raw_types():
    app = Client("test_session")
    # PageBlockParagraph
    pb_p = raw.types.PageBlockParagraph(text=raw.types.TextPlain(text="Paragraph text"))
    parsed_p = types.RichBlock._parse(app, pb_p)
    assert isinstance(parsed_p, types.RichBlockParagraph)
    assert parsed_p.text == "Paragraph text"

    # PageBlockDivider
    pb_div = raw.types.PageBlockDivider()
    parsed_div = types.RichBlock._parse(app, pb_div)
    assert isinstance(parsed_div, types.RichBlockDivider)

    # PageBlockBlockquote
    pb_bq = raw.types.PageBlockBlockquote(text=raw.types.TextPlain(text="Quote"), caption=raw.types.TextEmpty())
    parsed_bq = types.RichBlock._parse(app, pb_bq)
    assert isinstance(parsed_bq, types.RichBlockBlockQuotation)
    assert parsed_bq.text == "Quote"

    # PageBlockTable
    cell = raw.types.PageTableCell(text=raw.types.TextPlain(text="Cell 1"))
    row = raw.types.PageTableRow(cells=[cell])
    pb_table = raw.types.PageBlockTable(title=raw.types.TextEmpty(), rows=[row], bordered=True, striped=False)
    parsed_table = types.RichBlock._parse(app, pb_table)
    assert isinstance(parsed_table, types.RichBlockTable)
    assert len(parsed_table.cells) == 1
    assert parsed_table.cells[0][0].text == "Cell 1"


def test_ephemeral_bound_methods_exist():
    msg = types.Message(id=1, ephemeral_message_id=999)
    assert callable(msg.edit_ephemeral_text)
    assert callable(msg.edit_ephemeral_caption)
    assert callable(msg.edit_ephemeral_media)
    assert callable(msg.edit_ephemeral_reply_markup)
    assert callable(msg.delete_ephemeral)
    assert callable(msg.reply_rich)


def test_hypercrypto_mtproto_pack_and_kdf():
    from pyrogram.crypto import mtproto
    from pyrogram.raw.core import Long

    auth_key = os.urandom(256)
    msg_key = os.urandom(16)
    k1, iv1 = mtproto.kdf(auth_key, msg_key, True)
    assert len(k1) == 32
    assert len(iv1) == 32

    # Test pack
    salt = 987654321
    session_id = b"sess_123"
    auth_key_id = b"auth1234"

    class SimpleRawMessage:
        def __init__(self, body):
            self.msg_id = 1111
            self.seq_no = 1
            self.length = len(body)
            self.body = body

        def write(self):
            return Long(self.msg_id) + int(self.seq_no).to_bytes(4, "little") + int(self.length).to_bytes(4, "little") + self.body

    msg = SimpleRawMessage(b"test mtproto message payload")
    packed = mtproto.pack(msg, salt, session_id, auth_key, auth_key_id)
    assert packed.startswith(auth_key_id)
    assert len(packed) > 32


def test_hypercrypto_aes_ctr_streaming_speed_and_accuracy():
    key = os.urandom(32)
    initial_iv = os.urandom(16)

    iv_enc = bytearray(initial_iv)
    st_enc = bytearray(1)

    iv_dec = bytearray(initial_iv)
    st_dec = bytearray(1)

    chunks = [
        os.urandom(1),
        os.urandom(15),
        os.urandom(16),
        os.urandom(17),
        os.urandom(1024),
        os.urandom(65536),
    ]

    encrypted_chunks = [aes.ctr256_encrypt(c, key, iv_enc, st_enc) for c in chunks]
    decrypted_chunks = [aes.ctr256_decrypt(c, key, iv_dec, st_dec) for c in encrypted_chunks]

    assert decrypted_chunks == chunks
    assert iv_enc == iv_dec
    assert st_enc == st_dec




