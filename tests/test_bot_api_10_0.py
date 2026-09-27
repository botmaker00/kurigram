import pytest
from pyrogram.types import User, Message, ChatPermissions, ChatMember
from pyrogram import enums

def test_user_guest_queries():
    user = User(id=123, first_name="Test", supports_guest_queries=True)
    assert user.supports_guest_queries is True

def test_message_guest_fields():
    msg = Message(id=1, guest_query_id="query_123")
    assert msg.guest_query_id == "query_123"

def test_chat_permissions_react():
    perms = ChatPermissions(can_react_to_messages=True)
    assert perms.can_react_to_messages is True
