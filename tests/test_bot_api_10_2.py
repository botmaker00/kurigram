import pytest
from pyrogram.types import InputMediaVoiceNote, ReplyParameters, Message, BotCommand

def test_input_media_voice_note():
    vm = InputMediaVoiceNote(media="voice.ogg", duration=10)
    assert vm.media == "voice.ogg"
    assert vm.duration == 10

def test_ephemeral_reply_params():
    rp = ReplyParameters(message_id=100, ephemeral_message_id="ephem_123")
    assert rp.ephemeral_message_id == "ephem_123"

def test_ephemeral_bot_command():
    bc = BotCommand(command="start", description="Start bot", is_ephemeral=True)
    assert bc.is_ephemeral is True

def test_message_receiver_user():
    msg = Message(id=1, ephemeral_message_id="ephem_555")
    assert msg.ephemeral_message_id == "ephem_555"
