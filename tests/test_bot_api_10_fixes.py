import asyncio
import io
import pytest
from pyrogram import types, raw, enums
from pyrogram.types.messages_and_media.rich_message import RichMessageButton, InputRichMessageMedia, InputRichMessage
from pyrogram.types.messages_and_media.rich_text import RichTextButton, RichText
from pyrogram.types.messages_and_media.rich_block import (
    RichBlock,
    InputRichBlockExpandableBlockQuotation,
    RichBlockExpandableBlockQuotation,
    InputRichBlockBlockQuotation,
    RichBlockBlockQuotation,
    InputRichBlockTable,
    RichBlockTable,
    RichBlockTableCell,
)


@pytest.mark.asyncio
async def test_rich_text_button_url_and_callback():
    # 1. URL button direct
    btn_url = RichTextButton(text="Open Web", url="https://kurigram.icu")
    assert btn_url.url == "https://kurigram.icu"
    raw_url = btn_url.write()
    assert isinstance(raw_url, raw.types.TextUrl)
    assert raw_url.url == "https://kurigram.icu"

    # Roundtrip parse
    parsed_url = RichTextButton._parse(None, raw_url)
    assert isinstance(parsed_url, RichTextButton)
    assert parsed_url.url == "https://kurigram.icu"

    # 2. Callback button direct
    btn_cb = RichTextButton(text="Click Action", callback_data="cb_test_123")
    assert btn_cb.callback_data == "cb_test_123"
    raw_cb = btn_cb.write()
    assert isinstance(raw_cb, raw.types.TextUrl)
    assert raw_cb.url == "tg://btn?data=cb_test_123"

    # Roundtrip parse
    parsed_cb = RichTextButton._parse(None, raw_cb)
    assert isinstance(parsed_cb, RichTextButton)
    assert parsed_cb.callback_data == "cb_test_123"

    # 3. Via RichMessageButton object
    rmb_url = RichMessageButton(text="Docs", url="https://docs.kurigram.icu")
    rt_rmb_url = RichTextButton(text="Docs", button=rmb_url)
    assert rt_rmb_url.url == "https://docs.kurigram.icu"
    raw_rmb_url = rt_rmb_url.write()
    assert raw_rmb_url.url == "https://docs.kurigram.icu"

    rmb_cb = RichMessageButton(text="Like", callback_data="like_post")
    rt_rmb_cb = RichTextButton(text="Like", button=rmb_cb)
    assert rt_rmb_cb.callback_data == "like_post"
    raw_rmb_cb = rt_rmb_cb.write()
    assert raw_rmb_cb.url == "tg://btn?data=like_post"

    # 4. Dict parsing
    parsed_dict_url = RichTextButton._parse(None, {"text": "A", "url": "https://a.com"})
    assert parsed_dict_url.url == "https://a.com"

    parsed_dict_cb = RichTextButton._parse(None, {"text": "B", "callback_data": "data_b"})
    assert parsed_dict_cb.callback_data == "data_b"


@pytest.mark.asyncio
async def test_rich_block_expandable_block_quotation_preserved():
    # Expandable quote must NOT downgrade to normal blockquote
    exp_quote = InputRichBlockExpandableBlockQuotation(
        text=RichText("This is an expandable quotation body."),
        credit=RichText("Source Author")
    )
    raw_exp = await exp_quote.write()
    assert isinstance(raw_exp, raw.types.PageBlockBlockquote)
    assert raw_exp.collapsed is True
    assert raw_exp.expandable is True

    # Deserialization must yield RichBlockExpandableBlockQuotation
    parsed_exp = RichBlock._parse(None, raw_exp)
    assert isinstance(parsed_exp, RichBlockExpandableBlockQuotation)
    assert parsed_exp.text.text == "This is an expandable quotation body."
    assert parsed_exp.credit.text == "Source Author"

    # Standard blockquote must serialize as collapsed=False and parse as RichBlockBlockQuotation
    std_quote = InputRichBlockBlockQuotation(
        text=RichText("Standard non-expandable quote."),
        credit=RichText("Author")
    )
    raw_std = await std_quote.write()
    assert isinstance(raw_std, raw.types.PageBlockBlockquote)
    assert raw_std.collapsed is False

    parsed_std = RichBlock._parse(None, raw_std)
    assert isinstance(parsed_std, RichBlockBlockQuotation)
    assert not isinstance(parsed_std, RichBlockExpandableBlockQuotation)
    assert parsed_std.text.text == "Standard non-expandable quote."


@pytest.mark.asyncio
async def test_rich_block_table_is_compact_preserved():
    table = InputRichBlockTable(
        cells=[
            [RichBlockTableCell(RichText("Col 1"), is_header=True), RichBlockTableCell(RichText("Col 2"), is_header=True)],
            [RichBlockTableCell(RichText("Val 1")), RichBlockTableCell(RichText("Val 2"))],
        ],
        is_bordered=True,
        is_striped=False,
        is_compact=True
    )
    raw_table = await table.write()
    assert isinstance(raw_table, raw.types.PageBlockTable)
    assert raw_table.bordered is True
    assert raw_table.striped is False
    assert raw_table.compact is True

    # Binary TL write and read
    wire_bytes = raw_table.write()
    deserialized_raw_table = raw.types.PageBlockTable.read(io.BytesIO(wire_bytes[4:]))  # Skip 4-byte constructor ID
    assert deserialized_raw_table.bordered is True
    assert deserialized_raw_table.compact is True

    # High-level parse
    parsed_table = RichBlock._parse(None, deserialized_raw_table)
    assert isinstance(parsed_table, RichBlockTable)
    assert parsed_table.is_bordered is True
    assert parsed_table.is_compact is True

    # Check is_compact=False
    table_normal = InputRichBlockTable(
        cells=[[RichBlockTableCell(RichText("A"))]],
        is_compact=False
    )
    raw_table_normal = await table_normal.write()
    assert raw_table_normal.compact is False
    wire_bytes_normal = raw_table_normal.write()
    deserialized_normal = raw.types.PageBlockTable.read(io.BytesIO(wire_bytes_normal[4:]))
    assert deserialized_normal.compact is False
    parsed_normal = RichBlock._parse(None, deserialized_normal)
    assert parsed_normal.is_compact is False


@pytest.mark.asyncio
async def test_tg_document_id_rich_message_media_handling():
    # 1. InputRichMessageMedia with tg://document?id= URI
    raw_doc = raw.types.InputDocument(id=11223344, access_hash=55667788, file_reference=b"ref")
    media_item = InputRichMessageMedia(id="tg://document?id=doc_attach_1", media=raw_doc)
    raw_file = await media_item.write()

    assert isinstance(raw_file, raw.types.InputRichFileDocument)
    assert raw_file.id == "doc_attach_1"
    assert raw_file.document.id == 11223344

    # 2. Document object passed into InputRichMessage
    doc_obj = types.Document(
        file_id="doc_file_id_xyz",
        file_unique_id="u_xyz",
        file_name="report.pdf",
        mime_type="application/pdf",
        file_size=2048,
        date=1727500000
    )
    rich_msg = InputRichMessage(
        markdown="Download [Report](tg://document?id=report_doc)",
        media=[
            InputRichMessageMedia(id="report_doc", media=doc_obj)
        ]
    )
    raw_rich_msg = await rich_msg.write()
    assert isinstance(raw_rich_msg, raw.types.InputRichMessageMarkdown)
    assert len(raw_rich_msg.files) == 1
    assert isinstance(raw_rich_msg.files[0], raw.types.InputRichFileDocument)
    assert raw_rich_msg.files[0].id == "report_doc"

    # 3. InputRichMessage with blocks
    rich_msg_blocks = InputRichMessage(
        blocks=[],
        media=[
            InputRichMessageMedia(id="tg://document?id=my_doc", media=doc_obj)
        ]
    )
    raw_rich_blocks = await rich_msg_blocks.write()
    assert isinstance(raw_rich_blocks, raw.types.InputRichMessage)
    assert len(raw_rich_blocks.documents) == 1
    assert len(raw_rich_blocks.photos) == 0  # Must NOT be misrouted as photo!
    assert isinstance(raw_rich_blocks.documents[0], raw.base.InputDocument)


@pytest.mark.asyncio
async def test_save_file_worker_error_and_cancellation():
    from unittest.mock import AsyncMock, MagicMock
    from pyrogram.client import Client

    client = Client("mock_session", in_memory=True)
    client.storage = MagicMock()
    client.storage.dc_id = AsyncMock(return_value=2)
    client.rnd_id = MagicMock(return_value=12345678)
    client.save_file_semaphore = asyncio.Semaphore(1)
    client.loop = asyncio.get_running_loop()
    client.executor = None
    client.me = MagicMock(is_premium=False)

    # 1. Test worker RPC error stops workers without leaks
    mock_session = MagicMock()
    mock_session.invoke = AsyncMock(side_effect=RuntimeError("Simulated RPC upload failure"))
    client.get_session = AsyncMock(return_value=mock_session)
    client.get_media_sessions = AsyncMock(return_value=[mock_session])

    dummy_data = b"X" * (1024 * 1024)  # 1 MB test buffer
    file_io = io.BytesIO(dummy_data)
    file_io.name = "test.bin"

    with pytest.raises(RuntimeError, match="Simulated RPC upload failure"):
        await client.save_file(path=file_io)

    # Verify no tasks were leaked
    await asyncio.sleep(0.05)
    current_tasks = [t for t in asyncio.all_tasks() if not t.done()]
    # All save_file internal workers must be completed/cancelled
    for t in current_tasks:
        assert "worker" not in t.get_name().lower()

    # 2. Test cancellation stops cleanly
    async def hang_invoke(rpc):
        await asyncio.sleep(10)

    mock_session_hang = MagicMock()
    mock_session_hang.invoke = hang_invoke
    client.get_session = AsyncMock(return_value=mock_session_hang)
    client.get_media_sessions = AsyncMock(return_value=[mock_session_hang])

    file_io2 = io.BytesIO(dummy_data)
    file_io2.name = "test_cancel.bin"

    save_task = asyncio.create_task(client.save_file(path=file_io2))
    await asyncio.sleep(0.05)  # Let workers spawn
    save_task.cancel()

    with pytest.raises(asyncio.CancelledError):
        await save_task

    # Verify all workers are closed
    await asyncio.sleep(0.05)
    remaining_tasks = [t for t in asyncio.all_tasks() if not t.done()]
    for t in remaining_tasks:
        assert "worker" not in t.get_name().lower()
