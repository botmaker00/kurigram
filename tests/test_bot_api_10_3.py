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
    # In Layer 227 schema, ReplyInlineMarkup and ReplyKeyboardMarkup do not have a force_reply field.
    # When force_reply is passed as truthy, write() raises NotImplementedError.
    force = types.ForceReply(selective=True)
    inline_markup = types.InlineKeyboardMarkup([[types.InlineKeyboardButton("Test", callback_data="cb")]], force_reply=force)
    with pytest.raises(NotImplementedError):
        await inline_markup.write()

    reply_markup = types.ReplyKeyboardMarkup([["Button"]], force_reply=force)
    with pytest.raises(NotImplementedError):
        await reply_markup.write()

    # Plain markups write successfully without force_reply
    plain_inline = types.InlineKeyboardMarkup([[types.InlineKeyboardButton("Test", callback_data="cb")]])
    raw_inline = await plain_inline.write()
    assert isinstance(raw_inline, raw.types.ReplyInlineMarkup)

    plain_reply = types.ReplyKeyboardMarkup([["Button"]])
    raw_reply = await plain_reply.write()
    assert isinstance(raw_reply, raw.types.ReplyKeyboardMarkup)

@pytest.mark.asyncio
async def test_chat_admin_rights_send_welcome_messages():
    # In Layer 227 schema, ChatAdminRights has no send_welcome_messages field.
    # Setting can_send_welcome_messages=True raises NotImplementedError on write().
    rights_custom = types.ChatAdministratorRights(
        can_send_welcome_messages=True,
        can_manage_tags=True,
        can_manage_direct_messages=True
    )
    with pytest.raises(NotImplementedError):
        rights_custom.write()

    # Default rights (can_send_welcome_messages=False) write successfully.
    rights_default = types.ChatAdministratorRights(
        can_manage_tags=True,
        can_manage_direct_messages=True
    )
    raw_rights = rights_default.write()
    assert isinstance(raw_rights, raw.types.ChatAdminRights)
    assert raw_rights.manage_ranks is True
    assert raw_rights.manage_direct_messages is True

    read_rights = types.ChatAdministratorRights.read(raw_rights)
    assert read_rights.can_send_welcome_messages is False
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
