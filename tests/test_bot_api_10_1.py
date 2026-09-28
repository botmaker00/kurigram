import pytest
import asyncio
from pyrogram import types, enums, raw

def test_rich_text_types_exist():
    assert hasattr(types, "RichText")
    assert hasattr(types, "RichTextBold")
    assert hasattr(types, "RichTextItalic")
    assert hasattr(types, "RichTextUnderline")
    assert hasattr(types, "RichTextStrikethrough")
    assert hasattr(types, "RichTextSpoiler")
    assert hasattr(types, "RichTextCode")
    assert hasattr(types, "RichTextUrl")
    assert hasattr(types, "RichTextEmailAddress")
    assert hasattr(types, "RichTextPhoneNumber")
    assert hasattr(types, "RichTextBankCardNumber")
    assert hasattr(types, "RichTextMention")
    assert hasattr(types, "RichTextTextMention")
    assert hasattr(types, "RichTextHashtag")
    assert hasattr(types, "RichTextCashtag")
    assert hasattr(types, "RichTextBotCommand")
    assert hasattr(types, "RichTextAnchor")
    assert hasattr(types, "RichTextAnchorLink")
    assert hasattr(types, "RichTextReference")
    assert hasattr(types, "RichTextReferenceLink")
    assert hasattr(types, "RichTextCustomEmoji")
    assert hasattr(types, "RichTextMathematicalExpression")
    assert hasattr(types, "RichTextSubscript")
    assert hasattr(types, "RichTextSuperscript")
    assert hasattr(types, "RichTextMarked")
    assert hasattr(types, "RichTextDateTime")
    assert hasattr(types, "RichTextButton")

def test_input_rich_text_aliases():
    assert hasattr(types, "InputRichText")
    assert hasattr(types, "InputRichTextBold")
    assert hasattr(types, "InputRichTextUrl")
    assert hasattr(types, "InputRichTextCode")
    assert hasattr(types, "InputRichTextCustomEmoji")

def test_rich_block_types_exist():
    block_classes = [
        "RichBlockParagraph", "RichBlockSectionHeading", "RichBlockPreformatted",
        "RichBlockFooter", "RichBlockDivider", "RichBlockMathematicalExpression",
        "RichBlockAnchor", "RichBlockList", "RichBlockBlockQuotation",
        "RichBlockExpandableBlockQuotation", "RichBlockPullQuotation", "RichBlockCollage",
        "RichBlockSlideshow", "RichBlockTable", "RichBlockDetails", "RichBlockMap",
        "RichBlockAnimation", "RichBlockAudio", "RichBlockDocument", "RichBlockPhoto",
        "RichBlockVideo", "RichBlockVoiceNote", "RichBlockThinking", "RichBlockButtons",
        "RichBlockCaption", "RichBlockListItem", "RichBlockTableCell"
    ]
    for cls in block_classes:
        assert hasattr(types, cls), f"Missing {cls}"

@pytest.mark.asyncio
async def test_input_media_link():
    assert hasattr(types, "InputMediaLink")
    media = types.InputMediaLink(url="https://example.com", force_large_media=True)
    raw_media = await media.write()
    assert isinstance(raw_media, raw.types.InputMediaWebPage)
    assert raw_media.url == "https://example.com"
    assert raw_media.force_large_media is True

def test_web_app_init_data():
    assert hasattr(types, "WebAppInitData")
    data = types.WebAppInitData(query_id="qid", chat_join_request_query_id="req123")
    assert data.query_id == "qid"
    assert data.chat_join_request_query_id == "req123"

    parsed = types.WebAppInitData.read({"query_id": "qid2", "chat_join_request_query_id": "req456"})
    assert parsed.query_id == "qid2"
    assert parsed.chat_join_request_query_id == "req456"

@pytest.mark.asyncio
async def test_rich_message_serialization():
    assert hasattr(types, "InputRichMessage")
    block1 = types.InputRichBlockParagraph(text=types.RichTextBold("Hello world"))
    block2 = types.InputRichBlockDivider()
    msg = types.InputRichMessage(blocks=[block1, block2])
    raw_msg = await msg.write()
    assert isinstance(raw_msg, raw.types.InputRichMessage)
    assert len(raw_msg.blocks) == 2
    assert isinstance(raw_msg.blocks[0], raw.types.PageBlockParagraph)
    assert isinstance(raw_msg.blocks[1], raw.types.PageBlockDivider)
