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
        can_send_welcome_messages=True,
        can_manage_direct_messages=True,
        can_manage_tags=True
    )
    raw_rights = rights.write()
    assert isinstance(raw_rights, raw.types.ChatAdminRights)
    assert raw_rights.send_welcome_messages is True
    assert raw_rights.manage_direct_messages is True
    assert raw_rights.manage_ranks is True

    read_rights = types.ChatAdministratorRights.read(raw_rights)
    assert read_rights.can_send_welcome_messages is True
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
