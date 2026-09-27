import pytest
from pyrogram.types import ChatAdministratorRights

def test_chat_admin_rights_welcome_messages():
    rights = ChatAdministratorRights(can_send_welcome_messages=True)
    assert rights.can_send_welcome_messages is True
