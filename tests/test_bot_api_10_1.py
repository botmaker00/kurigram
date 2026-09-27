import pytest
from pyrogram.types import RichMessage, ChatJoinRequest, User
from pyrogram import raw

def test_rich_message_parsing():
    raw_rm = raw.types.RichMessage(
        rtl=True,
        part=False,
        blocks=[raw.types.PageBlockParagraph(text=raw.types.TextPlain(text="Hello"))],
        photos=[],
        documents=[]
    )
    parsed = RichMessage._parse(None, raw_rm)
    assert parsed.rtl is True
    assert parsed.part is False
    assert len(parsed.blocks) == 1

def test_chat_join_request_query_id():
    cjr = ChatJoinRequest(
        chat=None,
        from_user=User(id=123, first_name="Test"),
        date=None,
        query_id="query_999"
    )
    assert cjr.query_id == "query_999"
