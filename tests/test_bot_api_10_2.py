import pytest
from pyrogram import types, enums, raw, Client

def test_input_media_voice_note():
    assert hasattr(types, "InputMediaVoiceNote")
    vn = types.InputMediaVoiceNote(voice_note="path/to/voice.ogg", duration=10)
    assert vn.voice_note == "path/to/voice.ogg"
    assert vn.duration == 10

def test_ephemeral_message_parameters():
    params = types.EphemeralMessageParameters(
        receiver_user_id=12345,
        callback_query_id="query_abc",
        replace_callback_query_message=True
    )
    assert params.receiver_user_id == 12345
    assert params.callback_query_id == "query_abc"
    assert params.replace_callback_query_message is True

def test_ephemeral_client_methods():
    client = Client("test_client")
    assert hasattr(client, "edit_ephemeral_message_text")
    assert hasattr(client, "edit_ephemeral_message_media")
    assert hasattr(client, "edit_ephemeral_message_caption")
    assert hasattr(client, "edit_ephemeral_message_reply_markup")
    assert hasattr(client, "delete_ephemeral_message")

def test_ephemeral_message_bound_methods():
    msg = types.Message(id=1, ephemeral_message_id=42)
    assert hasattr(msg, "edit_ephemeral_text")
    assert hasattr(msg, "edit_ephemeral_caption")
    assert hasattr(msg, "edit_ephemeral_media")
    assert hasattr(msg, "edit_ephemeral_reply_markup")
    assert hasattr(msg, "delete_ephemeral")

def test_callback_query_ephemeral():
    cb = types.CallbackQuery(id="cb1", from_user=types.User(id=10, first_name="A"), chat_instance="inst")
    assert hasattr(cb, "as_ephemeral_message_parameters")
    assert hasattr(cb, "reply_ephemeral")
    params = cb.as_ephemeral_message_parameters()
    assert params.receiver_user_id == 10
    assert params.callback_query_id == "cb1"

def test_community_types():
    assert hasattr(types, "Community")
    assert hasattr(types, "CommunityChatAdded")
    assert hasattr(types, "CommunityChatRemoved")
    c = types.Community(id=1, title="Test Community")
    added = types.CommunityChatAdded(community=c)
    assert added.community.title == "Test Community"

    parsed_added = types.CommunityChatAdded.read({"community": {"id": 2, "title": "C2"}})
    assert parsed_added.community.title == "C2"

    removed = types.CommunityChatRemoved()
    parsed_removed = types.CommunityChatRemoved.read({})
    assert isinstance(parsed_removed, types.CommunityChatRemoved)

def test_bot_subscription_updated():
    assert hasattr(types, "BotSubscriptionUpdated")
