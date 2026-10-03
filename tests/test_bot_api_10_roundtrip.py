import pytest
from pyrogram import types, enums, raw

@pytest.mark.asyncio
async def test_roundtrip_rich_text():
    # Bold
    bold = types.RichTextBold("bold text")
    raw_bold = bold.write()
    assert isinstance(raw_bold, raw.types.TextBold)
    read_bold = types.RichText.read(raw_bold)
    assert isinstance(read_bold, types.RichTextBold)
    assert read_bold.text == "bold text"

    # Italic
    italic = types.RichTextItalic("italic text")
    raw_italic = italic.write()
    assert isinstance(raw_italic, raw.types.TextItalic)
    read_italic = types.RichText.read(raw_italic)
    assert isinstance(read_italic, types.RichTextItalic)
    assert read_italic.text == "italic text"

    # Code
    code = types.RichTextCode("code snippet")
    raw_code = code.write()
    assert isinstance(raw_code, raw.types.TextFixed)
    read_code = types.RichText.read(raw_code)
    assert isinstance(read_code, types.RichTextCode)
    assert read_code.text == "code snippet"

    # Url
    url = types.RichTextUrl("click here", url="https://example.com")
    raw_url = url.write()
    assert isinstance(raw_url, raw.types.TextUrl)
    assert raw_url.url == "https://example.com"
    read_url = types.RichText.read(raw_url)
    assert isinstance(read_url, types.RichTextUrl)
    assert read_url.url == "https://example.com"

@pytest.mark.asyncio
async def test_roundtrip_rich_blocks():
    # Paragraph
    p = types.RichBlockParagraph(text=types.RichTextBold("Para content"))
    raw_p = await p.write()
    assert isinstance(raw_p, raw.types.PageBlockParagraph)
    read_p = types.RichBlock.read(raw_p)
    assert isinstance(read_p, types.RichBlockParagraph)
    assert read_p.text.text == "Para content"

    # Preformatted
    pref = types.RichBlockPreformatted(text=types.RichText("print(1)"), language="python")
    raw_pref = await pref.write()
    assert isinstance(raw_pref, raw.types.PageBlockPreformatted)
    assert raw_pref.language == "python"
    read_pref = types.RichBlock.read(raw_pref)
    assert isinstance(read_pref, types.RichBlockPreformatted)
    assert read_pref.language == "python"

    # Header
    h = types.RichBlockSectionHeading(text=types.RichText("Header 1"), size="h1")
    raw_h = await h.write()
    assert isinstance(raw_h, raw.types.PageBlockHeader)
    read_h = types.RichBlock.read(raw_h)
    assert isinstance(read_h, types.RichBlockSectionHeading)

    # Subheader
    h2 = types.RichBlockSectionHeading(text=types.RichText("Header 2"), size="h2")
    raw_h2 = await h2.write()
    assert isinstance(raw_h2, raw.types.PageBlockSubheader)
    read_h2 = types.RichBlock.read(raw_h2)
    assert isinstance(read_h2, types.RichBlockSectionHeading)

    # Divider
    div = types.RichBlockDivider()
    raw_div = await div.write()
    assert isinstance(raw_div, raw.types.PageBlockDivider)
    read_div = types.RichBlock.read(raw_div)
    assert isinstance(read_div, types.RichBlockDivider)

    # Anchor
    anc = types.RichBlockAnchor(name="section-1")
    raw_anc = await anc.write()
    assert isinstance(raw_anc, raw.types.PageBlockAnchor)
    assert raw_anc.name == "section-1"
    read_anc = types.RichBlock.read(raw_anc)
    assert isinstance(read_anc, types.RichBlockAnchor)
    assert read_anc.name == "section-1"

    # Math
    math = types.RichBlockMathematicalExpression(text="E=mc^2")
    raw_math = await math.write()
    assert isinstance(raw_math, raw.types.PageBlockMath)
    assert raw_math.source == "E=mc^2"
    read_math = types.RichBlock.read(raw_math)
    assert isinstance(read_math, types.RichBlockMathematicalExpression)
    assert read_math.text.text == "E=mc^2"

    # Thinking
    th = types.RichBlockThinking(text=types.RichText("Thinking deeply..."))
    raw_th = await th.write()
    assert isinstance(raw_th, raw.types.PageBlockThinking)
    read_th = types.RichBlock.read(raw_th)
    assert isinstance(read_th, types.RichBlockThinking)

    # Details
    details = types.RichBlockDetails(
        title=types.RichText("Details Title"),
        blocks=[types.RichBlockParagraph(text=types.RichText("Inside details"))],
        is_open=True
    )
    raw_details = await details.write()
    assert isinstance(raw_details, raw.types.PageBlockDetails)
    read_details = types.RichBlock.read(raw_details)
    assert isinstance(read_details, types.RichBlockDetails)
    assert len(read_details.blocks) == 1

@pytest.mark.asyncio
async def test_roundtrip_table():
    cell1 = types.RichBlockTableCell(text=types.RichText("Cell 1"), align="center", is_header=True)
    raw_cell = await cell1.write()
    assert isinstance(raw_cell, raw.types.PageTableCell)
    assert raw_cell.align_center is True
    assert raw_cell.header is True
    read_cell = types.RichBlockTableCell.read(raw_cell)
    assert read_cell.align == "center"
    assert read_cell.is_header is True

    tbl = types.RichBlockTable(cells=[[cell1]], is_bordered=True, is_striped=False)
    raw_tbl = await tbl.write()
    assert isinstance(raw_tbl, raw.types.PageBlockTable)
    assert raw_tbl.bordered is True
    read_tbl = types.RichBlock.read(raw_tbl)
    assert isinstance(read_tbl, types.RichBlockTable)
    assert read_tbl.is_bordered is True
    assert len(read_tbl.cells) == 1
    assert len(read_tbl.cells[0]) == 1

@pytest.mark.asyncio
async def test_roundtrip_caption():
    cap = types.RichBlockCaption(text="Photo caption", credit="Author")
    raw_cap = await cap.write()
    assert isinstance(raw_cap, raw.types.PageCaption)
    read_cap = types.RichBlockCaption.read(raw_cap)
    assert isinstance(read_cap, types.RichBlockCaption)
    assert read_cap.text.text == "Photo caption"
    assert read_cap.credit.text == "Author"

@pytest.mark.asyncio
async def test_roundtrip_admin_rights():
    rights = types.ChatAdministratorRights(
        can_manage_chat=True,
        can_manage_direct_messages=True,
        can_manage_tags=True
    )
    raw_rights = rights.write()
    assert isinstance(raw_rights, raw.types.ChatAdminRights)
    assert raw_rights.manage_direct_messages is True
    assert raw_rights.manage_ranks is True

    read_rights = types.ChatAdministratorRights.read(raw_rights)
    assert read_rights.can_send_welcome_messages is False
    assert read_rights.can_manage_direct_messages is True
    assert read_rights.can_manage_tags is True

@pytest.mark.asyncio
async def test_roundtrip_inline_button_disabled():
    btn = types.InlineKeyboardButton("Test", disabled=True)
    raw_btn = await btn.write()
    read_btn = types.InlineKeyboardButton.read(raw_btn)
    assert read_btn.disabled is True
    assert read_btn.text == "Test"

@pytest.mark.asyncio
async def test_roundtrip_rich_message():
    block = types.InputRichBlockParagraph(text=types.RichTextBold("Hello world"))
    btn = types.RichMessageButton(text="Link", url="https://google.com")
    btn_block = types.RichBlockButtons(buttons=[[btn]])
    msg = types.InputRichMessage(blocks=[block, btn_block])
    raw_msg = await msg.write()
    assert isinstance(raw_msg, raw.types.InputRichMessage)
    assert len(raw_msg.blocks) == 2

    read_msg = types.RichMessage.read(raw_msg)
    assert isinstance(read_msg, types.RichMessage)
    assert len(read_msg.blocks) == 2
    assert isinstance(read_msg.blocks[0], types.RichBlockParagraph)
    assert isinstance(read_msg.blocks[1], types.RichBlockButtons)


@pytest.mark.asyncio
async def test_roundtrip_input_rich_message_media():
    # Test InputRichMessageMedia write & read
    photo = raw.types.InputPhoto(id=12345, access_hash=67890, file_reference=b"ref")
    media_item = types.InputRichMessageMedia(id="img_1", media=photo)
    raw_file = await media_item.write()
    assert isinstance(raw_file, raw.types.InputRichFilePhoto)
    assert raw_file.id == "img_1"
    assert raw_file.photo.id == 12345

    read_media = types.InputRichMessageMedia.read(raw_file)
    assert isinstance(read_media, types.InputRichMessageMedia)
    assert read_media.id == "img_1"
    assert read_media.media.id == 12345

    # Test InputRichMessage with media write & read
    doc = raw.types.InputDocument(id=54321, access_hash=9876, file_reference=b"doc_ref")
    doc_media_item = types.InputRichMessageMedia(id="doc_1", media=doc)

    rich_msg = types.InputRichMessage(
        blocks=[types.InputRichBlockDivider()],
        media=[media_item, doc_media_item],
    )
    raw_rich_msg = await rich_msg.write()
    assert isinstance(raw_rich_msg, raw.types.InputRichMessage)
    assert len(raw_rich_msg.photos) == 1
    assert raw_rich_msg.photos[0].id == 12345
    assert len(raw_rich_msg.documents) == 1
    assert raw_rich_msg.documents[0].id == 54321

    # Deserialization from raw.types.InputRichMessage preserves media
    read_rich_msg = types.InputRichMessage.read(raw_rich_msg)
    assert isinstance(read_rich_msg, types.InputRichMessage)
    assert read_rich_msg.media is not None
    assert len(read_rich_msg.media) == 2
    assert read_rich_msg.media[0].id == "12345"
    assert read_rich_msg.media[1].id == "54321"

    # Markdown format with embedded files
    md_msg = types.InputRichMessage(
        markdown="Look at this [media](tg://photo?id=img_1)",
        media=[media_item],
    )
    raw_md = await md_msg.write()
    assert isinstance(raw_md, raw.types.InputRichMessageMarkdown)
    assert raw_md.files is not None
    assert len(raw_md.files) == 1
    assert raw_md.files[0].id == "img_1"

    read_md = types.InputRichMessage.read(raw_md)
    assert read_md.media is not None
    assert len(read_md.media) == 1
    assert read_md.media[0].id == "img_1"


@pytest.mark.asyncio
async def test_roundtrip_rich_block_document():
    # InputRichBlockDocument write to raw.types.PageBlockDocument
    caption = types.RichBlockCaption(text=types.RichText("Annual Report 2026"))
    input_doc_block = types.InputRichBlockDocument(
        document=999888,
        caption=caption,
    )
    raw_block = await input_doc_block.write()
    assert isinstance(raw_block, raw.types.PageBlockDocument)
    assert raw_block.document_id == 999888
    assert raw_block.caption is not None

    # Deserialization back to RichBlockDocument
    parsed_block = types.RichBlock._parse(None, raw_block)
    assert isinstance(parsed_block, types.RichBlockDocument)
    assert parsed_block.document == 999888
    assert parsed_block.caption is not None
    assert parsed_block.caption.text.text == "Annual Report 2026"

