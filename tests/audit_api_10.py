import os
import sys
import inspect
import asyncio

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from pyrogram import types, enums, raw, Client

# Categories
results_10_1 = {"PASS": 0, "PARTIAL": 0, "MISSING": 0, "BROKEN": 0}
results_10_2 = {"PASS": 0, "PARTIAL": 0, "MISSING": 0, "BROKEN": 0}
results_10_3 = {"PASS": 0, "PARTIAL": 0, "MISSING": 0, "BROKEN": 0}
results_ser = {"PASS": 0, "FAIL": 0}
results_deser = {"PASS": 0, "FAIL": 0}
results_methods = {"PASS": 0, "FAIL": 0}
results_raw_tl = {"PASS": 0, "FAIL": 0}

def record_api(cat, passed):
    if passed:
        cat["PASS"] += 1
    else:
        cat["MISSING"] += 1

def record_ser(passed):
    if passed:
        results_ser["PASS"] += 1
    else:
        results_ser["FAIL"] += 1

def record_deser(passed):
    if passed:
        results_deser["PASS"] += 1
    else:
        results_deser["FAIL"] += 1

def record_method(passed):
    if passed:
        results_methods["PASS"] += 1
    else:
        results_methods["FAIL"] += 1

def record_raw(passed):
    if passed:
        results_raw_tl["PASS"] += 1
    else:
        results_raw_tl["FAIL"] += 1


async def run_audit():
    client = Client("audit_client")

    # ==================== BOT API 10.1 ====================
    # Rich Text types
    rich_text_classes = [
        "RichTextBold", "RichTextItalic", "RichTextUnderline", "RichTextStrikethrough",
        "RichTextSpoiler", "RichTextDateTime", "RichTextTextMention", "RichTextSubscript",
        "RichTextSuperscript", "RichTextMarked", "RichTextCode", "RichTextCustomEmoji",
        "RichTextMathematicalExpression", "RichTextUrl", "RichTextEmailAddress",
        "RichTextPhoneNumber", "RichTextBankCardNumber", "RichTextMention", "RichTextHashtag",
        "RichTextCashtag", "RichTextBotCommand", "RichTextAnchor", "RichTextAnchorLink",
        "RichTextReference", "RichTextReferenceLink"
    ]
    for cls_name in rich_text_classes:
        record_api(results_10_1, hasattr(types, cls_name))

    # Rich Block types
    rich_block_classes = [
        "RichBlockParagraph", "RichBlockSectionHeading", "RichBlockPreformatted",
        "RichBlockFooter", "RichBlockDivider", "RichBlockMathematicalExpression",
        "RichBlockAnchor", "RichBlockList", "RichBlockBlockQuotation",
        "RichBlockExpandableBlockQuotation", "RichBlockPullQuotation", "RichBlockCollage",
        "RichBlockSlideshow", "RichBlockTable", "RichBlockDetails", "RichBlockMap",
        "RichBlockAnimation", "RichBlockAudio", "RichBlockDocument", "RichBlockPhoto",
        "RichBlockVideo", "RichBlockVoiceNote", "RichBlockThinking", "RichBlockButtons",
        "RichBlockCaption", "RichBlockListItem", "RichBlockTableCell"
    ]
    for cls_name in rich_block_classes:
        record_api(results_10_1, hasattr(types, cls_name))

    # Rich Message & input content
    record_api(results_10_1, hasattr(types, "RichMessage"))
    record_api(results_10_1, hasattr(types, "InputRichMessage"))
    record_api(results_10_1, hasattr(types, "InputRichMessageContent"))
    record_api(results_10_1, hasattr(types.Message(id=1), "rich_message"))
    record_api(results_10_1, hasattr(types, "InputMediaLink"))
    record_api(results_10_1, hasattr(types, "WebAppInitData"))
    record_api(results_10_1, hasattr(types.User(id=1, first_name="X"), "supports_join_request_queries"))

    # ==================== BOT API 10.2 ====================
    # Input rich blocks
    input_rich_blocks = [
        "InputRichBlockParagraph", "InputRichBlockSectionHeading", "InputRichBlockPreformatted",
        "InputRichBlockFooter", "InputRichBlockDivider", "InputRichBlockMathematicalExpression",
        "InputRichBlockAnchor", "InputRichBlockList", "InputRichBlockBlockQuotation",
        "InputRichBlockPullQuotation", "InputRichBlockCollage", "InputRichBlockSlideshow",
        "InputRichBlockTable", "InputRichBlockDetails", "InputRichBlockMap",
        "InputRichBlockAnimation", "InputRichBlockAudio", "InputRichBlockPhoto",
        "InputRichBlockVideo", "InputRichBlockVoiceNote", "InputRichBlockThinking",
        "InputRichBlockListItem"
    ]
    for cls_name in input_rich_blocks:
        record_api(results_10_2, hasattr(types, cls_name))

    record_api(results_10_2, hasattr(types, "InputRichMessageMedia"))
    record_api(results_10_2, hasattr(types, "InputMediaVoiceNote"))
    record_api(results_10_2, hasattr(types, "EphemeralMessageParameters"))
    record_api(results_10_2, hasattr(types.BotCommand(command="c", description="d"), "is_ephemeral"))
    record_api(results_10_2, hasattr(types.Message(id=1), "receiver_user"))
    record_api(results_10_2, hasattr(types.Message(id=1), "ephemeral_message_id"))
    record_api(results_10_2, hasattr(types.ReplyParameters(message_id=1), "ephemeral_message_id"))
    record_api(results_10_2, hasattr(types, "Community"))
    record_api(results_10_2, hasattr(types, "CommunityChatAdded"))
    record_api(results_10_2, hasattr(types, "CommunityChatRemoved"))
    record_api(results_10_2, hasattr(types.Message(id=1), "community_chat_added"))
    record_api(results_10_2, hasattr(types.Message(id=1), "community_chat_removed"))
    record_api(results_10_2, hasattr(types, "BotSubscriptionUpdated"))

    # ==================== BOT API 10.3 ====================
    record_api(results_10_3, hasattr(types, "RichMessageButton"))
    record_api(results_10_3, hasattr(types, "RichTextButton"))
    record_api(results_10_3, hasattr(types, "RichBlockButtons"))
    record_api(results_10_3, hasattr(types, "InputRichBlockButtons"))
    record_api(results_10_3, hasattr(types.RichBlockTable(cells=[]), "is_compact"))
    record_api(results_10_3, hasattr(types.InputRichBlockTable(cells=[]), "is_compact"))
    record_api(results_10_3, hasattr(types, "RichBlockExpandableBlockQuotation"))
    record_api(results_10_3, hasattr(types, "InputRichBlockExpandableBlockQuotation"))
    record_api(results_10_3, hasattr(types, "RichBlockDocument"))
    record_api(results_10_3, hasattr(types, "InputRichBlockDocument"))
    record_api(results_10_3, hasattr(types, "DisabledButton"))
    record_api(results_10_3, hasattr(types.InlineKeyboardButton("x", disabled=True), "disabled"))
    record_api(results_10_3, hasattr(types.InlineKeyboardMarkup([[]]), "force_reply"))
    record_api(results_10_3, hasattr(types.ReplyKeyboardMarkup([[]]), "force_reply"))
    record_api(results_10_3, hasattr(types, "MessageGenerationStopped"))
    record_api(results_10_3, hasattr(types, "CommunityChatJoined"))
    record_api(results_10_3, hasattr(types.Message(id=1), "community_chat_joined"))
    record_api(results_10_3, hasattr(types.UniqueGiftInfo(origin="x", last_resale_currency="X", last_resale_amount=0), "text"))
    record_api(results_10_3, hasattr(types.UniqueGiftInfo(origin="x", last_resale_currency="X", last_resale_amount=0), "is_private"))
    record_api(results_10_3, hasattr(types.ChatAdministratorRights(), "can_send_welcome_messages"))

    # ==================== CLIENT METHODS ====================
    method_names = [
        "send_rich_message", "send_rich_message_draft", "send_message_draft",
        "answer_chat_join_request_query", "send_chat_join_request_web_app",
        "edit_ephemeral_message_text", "edit_ephemeral_message_media",
        "edit_ephemeral_message_caption", "edit_ephemeral_message_reply_markup",
        "delete_ephemeral_message", "send_message", "edit_message_text",
        "promote_chat_member"
    ]
    for m in method_names:
        record_method(hasattr(client, m))

    # Check method signatures
    send_draft_sig = inspect.signature(getattr(client.send_message_draft, "__wrapped__", client.send_message_draft))
    record_method("can_stop" in send_draft_sig.parameters and "keep_on_stop" in send_draft_sig.parameters)

    rich_draft_sig = inspect.signature(getattr(client.send_rich_message_draft, "__wrapped__", client.send_rich_message_draft))
    record_method("can_stop" in rich_draft_sig.parameters and "keep_on_stop" in rich_draft_sig.parameters)

    send_msg_sig = inspect.signature(getattr(client.send_message, "__wrapped__", client.send_message))
    record_method("ephemeral_message_parameters" in send_msg_sig.parameters and "rich_message" in send_msg_sig.parameters)

    # ==================== RAW TL CHECKS ====================
    record_raw(hasattr(raw.types.ChatAdminRights, "send_welcome_messages"))
    record_raw("send_welcome_messages" in raw.types.ChatAdminRights.__slots__)
    record_raw(hasattr(raw.types.ReplyInlineMarkup, "force_reply"))
    record_raw(hasattr(raw.types.ReplyKeyboardMarkup, "force_reply"))
    record_raw(hasattr(raw.types.SendMessageTextDraftAction, "can_stop"))
    record_raw(hasattr(raw.types.SendMessageTextDraftAction, "keep_on_stop"))
    record_raw(hasattr(raw.types.InputSendMessageRichMessageDraftAction, "can_stop"))
    record_raw(hasattr(raw.types.InputSendMessageRichMessageDraftAction, "keep_on_stop"))
    record_raw(hasattr(raw.types, "InputMediaWebPage"))
    record_raw(hasattr(raw.types, "MessageActionStarGiftUnique"))
    record_raw(hasattr(raw.types, "KeyboardButton"))
    record_raw(hasattr(raw.types, "InputRichMessage"))
    record_raw(hasattr(raw.types, "PageBlockParagraph"))
    record_raw(hasattr(raw.types, "PageBlockTable"))
    record_raw(hasattr(raw.types, "PageBlockDetails"))

    # ==================== SERIALIZATION (write) ====================
    # 1. InlineKeyboardButton disabled
    raw_btn = await types.InlineKeyboardButton("B", disabled=True).write()
    record_ser(isinstance(raw_btn, raw.types.KeyboardButton))

    # 2. DisabledButton
    raw_d_btn = await types.DisabledButton(text="DB").write()
    record_ser(isinstance(raw_d_btn, raw.types.KeyboardButton))

    # 3. InlineKeyboardMarkup force_reply
    raw_in_m = await types.InlineKeyboardMarkup([[]], force_reply=types.ForceReply()).write()
    record_ser(hasattr(raw_in_m, "force_reply") and isinstance(raw_in_m.force_reply, raw.types.ReplyKeyboardForceReply))

    # 4. ReplyKeyboardMarkup force_reply
    raw_rep_m = await types.ReplyKeyboardMarkup([[]], force_reply=types.ForceReply()).write()
    record_ser(hasattr(raw_rep_m, "force_reply") and isinstance(raw_rep_m.force_reply, raw.types.ReplyKeyboardForceReply))

    # 5. ChatAdministratorRights
    raw_adm = types.ChatAdministratorRights(can_send_welcome_messages=True, can_manage_direct_messages=True).write()
    record_ser(isinstance(raw_adm, raw.types.ChatAdminRights) and raw_adm.send_welcome_messages is True)

    # 6. InputMediaLink
    raw_link = await types.InputMediaLink(url="https://ex.com", force_large_media=True).write()
    record_ser(isinstance(raw_link, raw.types.InputMediaWebPage) and raw_link.force_large_media is True)

    # 7. RichText
    raw_bold = types.RichTextBold("text").write()
    record_ser(isinstance(raw_bold, raw.types.TextBold))

    raw_code = types.RichTextCode("code").write()
    record_ser(isinstance(raw_code, raw.types.TextFixed))

    raw_url = types.RichTextUrl("url", url="https://ex.com").write()
    record_ser(isinstance(raw_url, raw.types.TextUrl))

    # 8. RichBlock
    raw_p = await types.RichBlockParagraph(text=types.RichText("para")).write()
    record_ser(isinstance(raw_p, raw.types.PageBlockParagraph))

    raw_h = await types.RichBlockSectionHeading(text=types.RichText("head"), size="h1").write()
    record_ser(isinstance(raw_h, raw.types.PageBlockHeader))

    raw_pref = await types.RichBlockPreformatted(text=types.RichText("x"), language="py").write()
    record_ser(isinstance(raw_pref, raw.types.PageBlockPreformatted))

    raw_div = await types.RichBlockDivider().write()
    record_ser(isinstance(raw_div, raw.types.PageBlockDivider))

    raw_math = await types.RichBlockMathematicalExpression(text="x^2").write()
    record_ser(isinstance(raw_math, raw.types.PageBlockMath))

    raw_table = await types.RichBlockTable(cells=[[types.RichBlockTableCell(text="c")]]).write()
    record_ser(isinstance(raw_table, raw.types.PageBlockTable))

    raw_det = await types.RichBlockDetails(title=types.RichText("t"), blocks=[]).write()
    record_ser(isinstance(raw_det, raw.types.PageBlockDetails))

    raw_btns = await types.RichBlockButtons(buttons=[[types.RichMessageButton("B", url="https://ex.com")]]).write()
    record_ser(isinstance(raw_btns, raw.types.ReplyInlineMarkup))

    raw_msg = await types.InputRichMessage(blocks=[types.InputRichBlockDivider()]).write()
    record_ser(isinstance(raw_msg, raw.types.InputRichMessage))

    raw_media_msg = await types.InputRichMessage(
        blocks=[types.InputRichBlockDivider()],
        media=[types.InputRichMessageMedia(id="img", media=raw.types.InputPhoto(id=1, access_hash=2, file_reference=b""))],
    ).write()
    record_ser(isinstance(raw_media_msg, raw.types.InputRichMessage) and len(raw_media_msg.photos) == 1)

    raw_doc_blk = await types.InputRichBlockDocument(document=123, caption=types.RichBlockCaption(text=types.RichText("doc"))).write()
    record_ser(isinstance(raw_doc_blk, raw.types.PageBlockDocument) and raw_doc_blk.document_id == 123)

    # ==================== DESERIALIZATION (read / parse) ====================
    # 1. InlineKeyboardButton read disabled
    read_btn = types.InlineKeyboardButton.read(raw.types.KeyboardButton(text="B"))
    record_deser(read_btn.disabled is True and read_btn.text == "B")

    # 2. DisabledButton read
    read_d_btn = types.DisabledButton.read(raw.types.KeyboardButton(text="DB"))
    record_deser(read_d_btn.text == "DB")

    # 3. InlineKeyboardMarkup read force_reply
    read_in_m = types.InlineKeyboardMarkup.read(raw_in_m)
    record_deser(read_in_m.force_reply is not None)

    # 4. ReplyKeyboardMarkup read force_reply
    read_rep_m = types.ReplyKeyboardMarkup.read(raw_rep_m)
    record_deser(read_rep_m.force_reply is not None)

    # 5. ChatAdministratorRights read
    read_adm = types.ChatAdministratorRights.read(raw_adm)
    record_deser(read_adm.can_send_welcome_messages is True)

    # 6. WebAppInitData read
    read_init = types.WebAppInitData.read({"query_id": "q1", "chat_join_request_query_id": "req1"})
    record_deser(read_init.chat_join_request_query_id == "req1")

    # 7. UniqueGiftInfo read
    read_ug = types.UniqueGiftInfo.read({"origin": "o", "last_resale_currency": "X", "last_resale_amount": 1, "text": "gift"})
    record_deser(read_ug.text == "gift")

    # 8. CommunityChatJoined read
    read_joined = types.CommunityChatJoined.read({})
    record_deser(isinstance(read_joined, types.CommunityChatJoined))

    # 9. RichText read
    read_bold = types.RichText.read(raw_bold)
    record_deser(isinstance(read_bold, types.RichTextBold) and read_bold.text == "text")

    read_code = types.RichText.read(raw_code)
    record_deser(isinstance(read_code, types.RichTextCode) and read_code.text == "code")

    # 10. RichBlock read
    read_p = types.RichBlock.read(raw_p)
    record_deser(isinstance(read_p, types.RichBlockParagraph))

    read_h = types.RichBlock.read(raw_h)
    record_deser(isinstance(read_h, types.RichBlockSectionHeading))

    read_pref = types.RichBlock.read(raw_pref)
    record_deser(isinstance(read_pref, types.RichBlockPreformatted) and read_pref.language == "py")

    read_div = types.RichBlock.read(raw_div)
    record_deser(isinstance(read_div, types.RichBlockDivider))

    read_math = types.RichBlock.read(raw_math)
    record_deser(isinstance(read_math, types.RichBlockMathematicalExpression))

    read_table = types.RichBlock.read(raw_table)
    record_deser(isinstance(read_table, types.RichBlockTable))

    read_det = types.RichBlock.read(raw_det)
    record_deser(isinstance(read_det, types.RichBlockDetails))

    read_btns = types.RichBlock.read(raw_btns)
    record_deser(isinstance(read_btns, types.RichBlockButtons))

    read_msg = types.RichMessage.read(raw_msg)
    record_deser(isinstance(read_msg, types.RichMessage) and len(read_msg.blocks) == 1)

    read_media_msg = types.InputRichMessage.read(raw_media_msg)
    record_deser(read_media_msg.media is not None and len(read_media_msg.media) == 1 and read_media_msg.media[0].id == "1")

    read_doc_blk = types.RichBlock._parse(None, raw_doc_blk)
    record_deser(isinstance(read_doc_blk, types.RichBlockDocument) and read_doc_blk.document == 123)

    # Print Report
    print("=" * 30 + " KURIGRAM BOT API AUDIT " + "=" * 30)
    print(f"Bot API 10.1 PASS: {results_10_1['PASS']} PARTIAL: {results_10_1['PARTIAL']} MISSING: {results_10_1['MISSING']} BROKEN: {results_10_1['BROKEN']}")
    print(f"Bot API 10.2 PASS: {results_10_2['PASS']} PARTIAL: {results_10_2['PARTIAL']} MISSING: {results_10_2['MISSING']} BROKEN: {results_10_2['BROKEN']}")
    print(f"Bot API 10.3 PASS: {results_10_3['PASS']} PARTIAL: {results_10_3['PARTIAL']} MISSING: {results_10_3['MISSING']} BROKEN: {results_10_3['BROKEN']}")
    print(f"Serialization: PASS: {results_ser['PASS']} FAIL: {results_ser['FAIL']}")
    print(f"Deserialization: PASS: {results_deser['PASS']} FAIL: {results_deser['FAIL']}")
    print(f"Client Methods: PASS: {results_methods['PASS']} FAIL: {results_methods['FAIL']}")
    print(f"Raw TL: PASS: {results_raw_tl['PASS']} FAIL: {results_raw_tl['FAIL']}")
    print("=" * 84)

    total_failures = (
        results_10_1['MISSING'] + results_10_1['BROKEN'] +
        results_10_2['MISSING'] + results_10_2['BROKEN'] +
        results_10_3['MISSING'] + results_10_3['BROKEN'] +
        results_ser['FAIL'] + results_deser['FAIL'] +
        results_methods['FAIL'] + results_raw_tl['FAIL']
    )
    return total_failures == 0


if __name__ == "__main__":
    success = asyncio.run(run_audit())
    sys.exit(0 if success else 1)
