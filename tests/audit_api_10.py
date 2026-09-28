import os
import sys
import traceback

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

results = {"OK": [], "MISSING": [], "PARTIAL": [], "ERROR": []}

def check(label, fn):
    try:
        result = fn()
        if result is True:
            results["OK"].append(label)
        elif result is False:
            results["MISSING"].append(label)
        elif result == "PARTIAL":
            results["PARTIAL"].append(label)
        else:
            results["OK"].append(label)
    except Exception as e:
        results["ERROR"].append(f"{label}: {e}")

# Import everything
from pyrogram import types, enums, raw, Client

# ===== BOT API 10.0 =====

# Guest Mode
check("User.supports_guest_queries", lambda: hasattr(types.User(id=1, first_name="X"), "supports_guest_queries"))
check("Message.guest_bot_caller_user", lambda: hasattr(types.Message(id=1), "guest_bot_caller_user"))
check("Message.guest_bot_caller_chat", lambda: hasattr(types.Message(id=1), "guest_bot_caller_chat"))
check("Message.guest_query_id", lambda: hasattr(types.Message(id=1), "guest_query_id"))
check("types.SentGuestMessage", lambda: hasattr(types, "SentGuestMessage"))
check("Client.answer_guest_query", lambda: hasattr(Client("x"), "answer_guest_query"))

# Chat Management
check("ChatPermissions.can_react_to_messages", lambda: hasattr(types.ChatPermissions(), "can_react_to_messages"))
check("Poll.members_only", lambda: hasattr(types.Poll(
    id="x", question="Q", options=[], total_voter_count=0,
    is_closed=False, is_anonymous=True, type=enums.PollType.REGULAR, allows_multiple_answers=False
), "members_only"))
check("Poll.country_codes", lambda: hasattr(types.Poll(
    id="x", question="Q", options=[], total_voter_count=0,
    is_closed=False, is_anonymous=True, type=enums.PollType.REGULAR, allows_multiple_answers=False
), "country_codes"))
check("Client.delete_all_message_reactions", lambda: hasattr(Client("x"), "delete_all_message_reactions"))
check("Client.delete_message_reaction", lambda: hasattr(Client("x"), "delete_message_reaction"))

# Live Photos
check("types.LivePhoto", lambda: hasattr(types, "LivePhoto"))
check("types.InputMediaLivePhoto", lambda: hasattr(types, "InputMediaLivePhoto"))
check("types.PaidMediaLivePhoto", lambda: hasattr(types, "PaidMediaLivePhoto"))
check("types.InputPaidMediaLivePhoto", lambda: hasattr(types, "InputPaidMediaLivePhoto"))
check("Message.live_photo", lambda: hasattr(types.Message(id=1), "live_photo"))
check("ExternalReplyInfo.live_photo", lambda: hasattr(types.ExternalReplyInfo(
    origin=types.MessageOriginUser(date=0, sender_user=types.User(id=1, first_name="X"))
), "live_photo"))
check("Client.send_live_photo", lambda: hasattr(Client("x"), "send_live_photo"))

# Bot Access Settings
check("types.BotAccessSettings", lambda: hasattr(types, "BotAccessSettings"))
check("Client.get_managed_bot_access_settings", lambda: hasattr(Client("x"), "get_managed_bot_access_settings"))
check("Client.set_managed_bot_access_settings", lambda: hasattr(Client("x"), "set_managed_bot_access_settings"))
check("Client.get_user_personal_chat_messages", lambda: hasattr(Client("x"), "get_user_personal_chat_messages"))

# ===== BOT API 10.1 =====

# Rich Text Classes
for cls_name in ["RichTextBold", "RichTextItalic", "RichTextUnderline", "RichTextStrikethrough",
                  "RichTextSpoiler", "RichTextDateTime", "RichTextTextMention", "RichTextSubscript",
                  "RichTextSuperscript", "RichTextMarked", "RichTextCode", "RichTextCustomEmoji",
                  "RichTextMathematicalExpression", "RichTextUrl", "RichTextEmailAddress",
                  "RichTextPhoneNumber", "RichTextBankCardNumber", "RichTextMention", "RichTextHashtag",
                  "RichTextCashtag", "RichTextBotCommand", "RichTextAnchor", "RichTextAnchorLink",
                  "RichTextReference", "RichTextReferenceLink"]:
    check(f"types.{cls_name}", lambda n=cls_name: hasattr(types, n))

# Rich Block Classes
for cls_name in ["RichBlockParagraph", "RichBlockSectionHeading", "RichBlockPreformatted",
                  "RichBlockFooter", "RichBlockDivider", "RichBlockMathematicalExpression",
                  "RichBlockAnchor", "RichBlockList", "RichBlockBlockQuotation",
                  "RichBlockExpandableBlockQuotation", "RichBlockPullQuotation", "RichBlockCollage",
                  "RichBlockSlideshow", "RichBlockTable", "RichBlockDetails", "RichBlockMap",
                  "RichBlockAnimation", "RichBlockAudio", "RichBlockDocument", "RichBlockPhoto",
                  "RichBlockVideo", "RichBlockVoiceNote", "RichBlockThinking", "RichBlockButtons",
                  "RichBlockCaption", "RichBlockListItem", "RichBlockTableCell"]:
    check(f"types.{cls_name}", lambda n=cls_name: hasattr(types, n))

# RichMessage
check("types.RichMessage", lambda: hasattr(types, "RichMessage"))
check("types.InputRichMessage", lambda: hasattr(types, "InputRichMessage"))
check("types.InputRichMessageContent", lambda: hasattr(types, "InputRichMessageContent"))
check("Message.rich_message", lambda: hasattr(types.Message(id=1), "rich_message"))
check("Client.send_rich_message", lambda: hasattr(Client("x"), "send_rich_message"))
check("Client.send_rich_message_draft", lambda: hasattr(Client("x"), "send_rich_message_draft"))

# Join Request Queries
check("User.supports_join_request_queries", lambda: hasattr(types.User(id=1, first_name="X"), "supports_join_request_queries"))
check("Client.answer_chat_join_request_query", lambda: hasattr(Client("x"), "answer_chat_join_request_query"))
check("Client.send_chat_join_request_web_app", lambda: hasattr(Client("x"), "send_chat_join_request_web_app"))

# ===== BOT API 10.2 =====

# Rich Messages additions
check("types.InputRichMessageMedia", lambda: hasattr(types, "InputRichMessageMedia"))
check("types.InputMediaVoiceNote", lambda: hasattr(types, "InputMediaVoiceNote"))
check("types.InputRichBlockListItem", lambda: hasattr(types, "InputRichBlockListItem"))

# Input Rich Block Classes
for cls_name in ["InputRichBlockParagraph", "InputRichBlockSectionHeading", "InputRichBlockPreformatted",
                  "InputRichBlockFooter", "InputRichBlockDivider", "InputRichBlockMathematicalExpression",
                  "InputRichBlockAnchor", "InputRichBlockList", "InputRichBlockBlockQuotation",
                  "InputRichBlockPullQuotation", "InputRichBlockCollage", "InputRichBlockSlideshow",
                  "InputRichBlockTable", "InputRichBlockDetails", "InputRichBlockMap",
                  "InputRichBlockAnimation", "InputRichBlockAudio", "InputRichBlockPhoto",
                  "InputRichBlockVideo", "InputRichBlockVoiceNote", "InputRichBlockThinking"]:
    check(f"types.{cls_name}", lambda n=cls_name: hasattr(types, n))

# Ephemeral Messages
check("types.EphemeralMessageParameters", lambda: hasattr(types, "EphemeralMessageParameters"))
check("EphemeralMessageParameters.receiver_user_id", lambda: hasattr(
    types.EphemeralMessageParameters(receiver_user_id=1, callback_query_id="x"), "receiver_user_id"))
check("EphemeralMessageParameters.callback_query_id", lambda: hasattr(
    types.EphemeralMessageParameters(receiver_user_id=1, callback_query_id="x"), "callback_query_id"))
check("EphemeralMessageParameters.replace_callback_query_message", lambda: hasattr(
    types.EphemeralMessageParameters(receiver_user_id=1, callback_query_id="x"), "replace_callback_query_message"))
check("BotCommand.is_ephemeral", lambda: hasattr(
    types.BotCommand(command="x", description="y", is_ephemeral=True), "is_ephemeral"))
check("Message.receiver_user", lambda: hasattr(types.Message(id=1), "receiver_user"))
check("Message.ephemeral_message_id", lambda: hasattr(types.Message(id=1), "ephemeral_message_id"))
check("ReplyParameters.ephemeral_message_id", lambda: hasattr(
    types.ReplyParameters(message_id=1, ephemeral_message_id=5), "ephemeral_message_id"))
check("Client.edit_ephemeral_message_text", lambda: hasattr(Client("x"), "edit_ephemeral_message_text"))
check("Client.edit_ephemeral_message_media", lambda: hasattr(Client("x"), "edit_ephemeral_message_media"))
check("Client.edit_ephemeral_message_caption", lambda: hasattr(Client("x"), "edit_ephemeral_message_caption"))
check("Client.edit_ephemeral_message_reply_markup", lambda: hasattr(Client("x"), "edit_ephemeral_message_reply_markup"))
check("Client.delete_ephemeral_message", lambda: hasattr(Client("x"), "delete_ephemeral_message"))

# Communities
check("types.Community", lambda: hasattr(types, "Community"))
check("types.CommunityChatAdded", lambda: hasattr(types, "CommunityChatAdded"))
check("types.CommunityChatRemoved", lambda: hasattr(types, "CommunityChatRemoved"))
check("Message.community_chat_added", lambda: hasattr(types.Message(id=1), "community_chat_added"))
check("Message.community_chat_removed", lambda: hasattr(types.Message(id=1), "community_chat_removed"))

# Subscriptions
check("types.BotSubscriptionUpdated", lambda: hasattr(types, "BotSubscriptionUpdated"))

# ===== BOT API 10.3 =====

# Rich Message Buttons
check("types.RichMessageButton", lambda: hasattr(types, "RichMessageButton"))
check("types.RichTextButton", lambda: hasattr(types, "RichTextButton"))
check("types.RichBlockButtons", lambda: hasattr(types, "RichBlockButtons"))
check("types.InputRichBlockButtons", lambda: hasattr(types, "InputRichBlockButtons"))

# Table is_compact
check("RichBlockTable.is_compact field", lambda: hasattr(types.RichBlockTable(cells=[]), "is_compact"))
check("InputRichBlockTable.is_compact field", lambda: hasattr(types.InputRichBlockTable(cells=[]), "is_compact"))

# Expandable Quotation
check("types.RichBlockExpandableBlockQuotation", lambda: hasattr(types, "RichBlockExpandableBlockQuotation"))
check("types.InputRichBlockExpandableBlockQuotation", lambda: hasattr(types, "InputRichBlockExpandableBlockQuotation"))

# Document
check("types.RichBlockDocument", lambda: hasattr(types, "RichBlockDocument"))
check("types.InputRichBlockDocument", lambda: hasattr(types, "InputRichBlockDocument"))

# Disabled Button
check("types.DisabledButton", lambda: hasattr(types, "DisabledButton"))
check("InlineKeyboardButton.disabled", lambda: hasattr(
    types.InlineKeyboardButton(text="x", disabled=True), "disabled"))

# Force Reply
check("InlineKeyboardMarkup.force_reply", lambda: hasattr(
    types.InlineKeyboardMarkup(inline_keyboard=[[]], force_reply=types.ForceReply(selective=False)), "force_reply"))
check("ReplyKeyboardMarkup.force_reply", lambda: hasattr(
    types.ReplyKeyboardMarkup(keyboard=[[]], force_reply=types.ForceReply(selective=False)), "force_reply"))

# can_stop / keep_on_stop in sendMessageDraft
def check_send_msg_draft_params():
    import inspect
    app = Client("x")
    if hasattr(app, "send_message_draft"):
        fn = getattr(app.send_message_draft, "__wrapped__", app.send_message_draft)
        return "can_stop" in inspect.signature(fn).parameters
    return False

def check_send_rich_draft_params():
    import inspect
    app = Client("x")
    if hasattr(app, "send_rich_message_draft"):
        fn = getattr(app.send_rich_message_draft, "__wrapped__", app.send_rich_message_draft)
        return "can_stop" in inspect.signature(fn).parameters
    return False

check("Client.send_message_draft (can_stop param)", check_send_msg_draft_params)
check("Client.send_rich_message_draft (can_stop param)", check_send_rich_draft_params)

# MessageGenerationStopped
check("types.MessageGenerationStopped", lambda: hasattr(types, "MessageGenerationStopped"))

# CommunityChatJoined
check("types.CommunityChatJoined", lambda: hasattr(types, "CommunityChatJoined"))
check("Message.community_chat_joined", lambda: hasattr(types.Message(id=1), "community_chat_joined"))

# UniqueGiftInfo fields
check("UniqueGiftInfo.text", lambda: hasattr(
    types.UniqueGiftInfo(origin="x", last_resale_currency="XTR", last_resale_amount=0, text="hi"), "text"))
check("UniqueGiftInfo.is_private", lambda: hasattr(
    types.UniqueGiftInfo(origin="x", last_resale_currency="XTR", last_resale_amount=0, is_private=False), "is_private"))

# Admin rights
check("ChatAdministratorRights.can_send_welcome_messages", lambda: hasattr(
    types.ChatAdministratorRights(can_send_welcome_messages=True), "can_send_welcome_messages"))

# send methods ephemeral params
def check_send_msg_ephemeral():
    import inspect
    app = Client("x")
    if hasattr(app, "send_message"):
        fn = getattr(app.send_message, "__wrapped__", app.send_message)
        return "ephemeral_message_parameters" in inspect.signature(fn).parameters
    return False
check("Client.send_message (ephemeral_message_parameters)", check_send_msg_ephemeral)
# Message bound methods
msg = types.Message(id=1, ephemeral_message_id=5)
check("Message.edit_ephemeral_text bound method", lambda: hasattr(msg, "edit_ephemeral_text"))
check("Message.edit_ephemeral_caption bound method", lambda: hasattr(msg, "edit_ephemeral_caption"))
check("Message.edit_ephemeral_media bound method", lambda: hasattr(msg, "edit_ephemeral_media"))
check("Message.edit_ephemeral_reply_markup bound method", lambda: hasattr(msg, "edit_ephemeral_reply_markup"))
check("Message.delete_ephemeral bound method", lambda: hasattr(msg, "delete_ephemeral"))
check("Message.reply_rich bound method", lambda: hasattr(msg, "reply_rich"))

# CallbackQuery ephemeral
cb = types.CallbackQuery(id="x", from_user=types.User(id=1, first_name="X"), chat_instance="y")
check("CallbackQuery.as_ephemeral_message_parameters", lambda: hasattr(cb, "as_ephemeral_message_parameters"))
check("CallbackQuery.reply_ephemeral", lambda: hasattr(cb, "reply_ephemeral"))

# FSInputFile / BufferedInputFile
check("types.FSInputFile", lambda: hasattr(types, "FSInputFile"))
check("types.BufferedInputFile", lambda: hasattr(types, "BufferedInputFile"))
check("types.InputMediaVoiceNote", lambda: hasattr(types, "InputMediaVoiceNote"))

print("\n" + "="*60)
print("AUDIT RESULTS:")
print("="*60)
print(f"\nOK ({len(results['OK'])}):")
for x in results["OK"]:
    print(f"  v {x}")
print(f"\nMISSING ({len(results['MISSING'])}):")
for x in results["MISSING"]:
    print(f"  X {x}")
print(f"\nPARTIAL ({len(results['PARTIAL'])}):")
for x in results["PARTIAL"]:
    print(f"  ~ {x}")
print(f"\nERRORS ({len(results['ERROR'])}):")
for x in results["ERROR"]:
    print(f"  ! {x}")

total = len(results["OK"]) + len(results["MISSING"]) + len(results["PARTIAL"]) + len(results["ERROR"])
ok = len(results["OK"])
print(f"\nTotal: {ok}/{total} ({100*ok//total if total else 0}% complete)")
sys.exit(0 if not results["MISSING"] and not results["ERROR"] else 1)
