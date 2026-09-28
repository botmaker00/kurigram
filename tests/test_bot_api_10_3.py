import pytest
import inspect
from pyrogram import types, enums, raw, Client

@pytest.mark.asyncio
async def test_disabled_inline_button_serialization():
    btn = types.InlineKeyboardButton(text="Click", disabled=True)
    raw_btn = await btn.write()
    assert isinstance(raw_btn, raw.types.KeyboardButton)
    assert raw_btn.text == "Click"
    # Read back
    read_btn = types.InlineKeyboardButton.read(raw_btn)
    assert read_btn.text == "Click"
    assert read_btn.disabled is True

@pytest.mark.asyncio
async def test_disabled_button_class():
    d_btn = types.DisabledButton(text="Disabled")
    raw_btn = await d_btn.write()
    assert isinstance(raw_btn, raw.types.KeyboardButton)
    assert raw_btn.text == "Disabled"
    read_d_btn = types.DisabledButton.read(raw_btn)
    assert read_d_btn.text == "Disabled"

@pytest.mark.asyncio
async def test_force_reply_in_markups():
    force = types.ForceReply(selective=True)
    inline_markup = types.InlineKeyboardMarkup([[types.InlineKeyboardButton("Test", callback_data="cb")]], force_reply=force)
    raw_inline = await inline_markup.write()
    assert hasattr(raw_inline, "force_reply")
    assert raw_inline.force_reply is not None
    assert isinstance(raw_inline.force_reply, raw.types.ReplyKeyboardForceReply)
    assert raw_inline.force_reply.selective is True

    read_inline = types.InlineKeyboardMarkup.read(raw_inline)
    assert read_inline.force_reply is not None
    assert read_inline.force_reply.selective is True

    reply_markup = types.ReplyKeyboardMarkup([["Button"]], force_reply=force)
    raw_reply = await reply_markup.write()
    assert hasattr(raw_reply, "force_reply")
    assert raw_reply.force_reply is not None
    assert isinstance(raw_reply.force_reply, raw.types.ReplyKeyboardForceReply)

    read_reply = types.ReplyKeyboardMarkup.read(raw_reply)
    assert read_reply.force_reply is not None
    assert read_reply.force_reply.selective is True

@pytest.mark.asyncio
async def test_chat_admin_rights_send_welcome_messages():
    rights = types.ChatAdministratorRights(
        can_send_welcome_messages=True,
        can_manage_tags=True,
        can_manage_direct_messages=True
    )
    raw_rights = rights.write()
    assert isinstance(raw_rights, raw.types.ChatAdminRights)
    assert raw_rights.send_welcome_messages is True
    assert raw_rights.manage_ranks is True
    assert raw_rights.manage_direct_messages is True

    read_rights = types.ChatAdministratorRights.read(raw_rights)
    assert read_rights.can_send_welcome_messages is True
    assert read_rights.can_manage_tags is True
    assert read_rights.can_manage_direct_messages is True

def test_draft_can_stop_keep_on_stop():
    app = Client("test_client")
    sig = inspect.signature(getattr(app.send_message_draft, "__wrapped__", app.send_message_draft))
    assert "can_stop" in sig.parameters
    assert "keep_on_stop" in sig.parameters

    sig_rich = inspect.signature(getattr(app.send_rich_message_draft, "__wrapped__", app.send_rich_message_draft))
    assert "can_stop" in sig_rich.parameters
    assert "keep_on_stop" in sig_rich.parameters

def test_community_chat_joined():
    assert hasattr(types, "CommunityChatJoined")
    joined = types.CommunityChatJoined()
    assert isinstance(joined, types.CommunityChatJoined)
    parsed = types.CommunityChatJoined.read({})
    assert isinstance(parsed, types.CommunityChatJoined)

def test_unique_gift_info():
    assert hasattr(types, "UniqueGiftInfo")
    gift = types.UniqueGiftInfo(
        origin="test",
        last_resale_currency="XTR",
        last_resale_amount=100,
        text="A unique gift",
        is_private=True
    )
    assert gift.text == "A unique gift"
    assert gift.is_private is True
    assert gift.last_resale_currency == "XTR"
    assert gift.last_resale_amount == 100

@pytest.mark.asyncio
async def test_rich_block_buttons():
    btn = types.RichMessageButton(text="Open", url="https://example.com")
    raw_btn = btn.write()
    assert isinstance(raw_btn, raw.types.KeyboardButtonUrl)

    read_btn = types.RichMessageButton.read(raw_btn)
    assert read_btn.text == "Open"
    assert read_btn.url == "https://example.com"

    block_buttons = types.RichBlockButtons(buttons=[[btn]])
    raw_markup = await block_buttons.write()
    assert isinstance(raw_markup, raw.types.ReplyInlineMarkup)
    assert len(raw_markup.rows) == 1
    assert len(raw_markup.rows[0].buttons) == 1

    read_block = types.RichBlock.read(raw_markup)
    assert isinstance(read_block, types.RichBlockButtons)
    assert len(read_block.buttons) == 1
    assert read_block.buttons[0][0].text == "Open"
