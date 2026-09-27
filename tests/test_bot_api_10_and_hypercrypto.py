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


