#  Pyrogram - Telegram MTProto API Client Library for Python
#  Copyright (C) 2017-present Dan <https://github.com/delivrance>
#
#  This file is part of Pyrogram.
#
#  Pyrogram is free software: you can redistribute it and/or modify
#  it under the terms of the GNU Lesser General Public License as published
#  by the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  Pyrogram is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU Lesser General Public License for more details.
#
#  You should have received a copy of the GNU Lesser General Public License
#  along with Pyrogram.  If not, see <http://www.gnu.org/licenses/>.

from typing import Optional, Union

import pyrogram
from pyrogram import raw, types


class SendRichMessage:
    async def send_rich_message(
        self: "pyrogram.Client",
        chat_id: Union[int, str],
        rich_message: Union["types.InputRichMessage", str, "raw.base.InputRichMessage"],
        business_connection_id: Optional[str] = None,
        message_thread_id: Optional[int] = None,
        direct_messages_topic_id: Optional[int] = None,
        disable_notification: Optional[bool] = None,
        protect_content: Optional[bool] = None,
        allow_paid_broadcast: Optional[bool] = None,
        message_effect_id: Optional[int] = None,
        suggested_post_parameters: Optional["types.SuggestedPostParameters"] = None,
        reply_parameters: Optional["types.ReplyParameters"] = None,
        reply_markup: Optional[Union[
            "types.InlineKeyboardMarkup",
            "types.ReplyKeyboardMarkup",
            "types.ReplyKeyboardRemove",
            "types.ForceReply"
        ]] = None,
        ephemeral_message_parameters: Optional["types.EphemeralMessageParameters"] = None,
        receiver_user_id: Optional[int] = None,
        callback_query_id: Optional[str] = None,
    ) -> "types.Message":
        """Send rich formatted messages.

        Parameters:
            chat_id (``int`` | ``str``):
                Unique identifier (int) or username (str) of the target chat.

            rich_message (:obj:`~pyrogram.types.InputRichMessage` | ``str``):
                The message to be sent.

            business_connection_id (``str``, *optional*):
                Unique identifier of the business connection on behalf of which the message will be sent.

            message_thread_id (``int``, *optional*):
                Unique identifier for the target message thread.

            direct_messages_topic_id (``int``, *optional*):
                Identifier of the direct messages topic.

            disable_notification (``bool``, *optional*):
                Sends the message silently.

            protect_content (``bool``, *optional*):
                Protects the contents of the sent message from forwarding and saving.

            allow_paid_broadcast (``bool``, *optional*):
                Pass True to allow up to 1000 messages per second.

            message_effect_id (``int``, *optional*):
                Unique identifier of the message effect to be added to the message.

            suggested_post_parameters (:obj:`~pyrogram.types.SuggestedPostParameters`, *optional*):
                Parameters of the suggested post to send.

            reply_parameters (:obj:`~pyrogram.types.ReplyParameters`, *optional*):
                Description of the message to reply to.

            reply_markup (:obj:`~pyrogram.types.InlineKeyboardMarkup` | :obj:`~pyrogram.types.ReplyKeyboardMarkup` | :obj:`~pyrogram.types.ReplyKeyboardRemove` | :obj:`~pyrogram.types.ForceReply`, *optional*):
                Additional interface options.

            ephemeral_message_parameters (:obj:`~pyrogram.types.EphemeralMessageParameters`, *optional*):
                Parameters of the ephemeral message.

            receiver_user_id (``int``, *optional*):
                Unique identifier of the user who will receive the message.

            callback_query_id (``str``, *optional*):
                Identifier of the callback query which triggered the message.

        Returns:
            :obj:`~pyrogram.types.Message`: On success, the sent Message is returned.
        """
        # Convert types.InputRichMessage to raw/str if needed
        raw_rich = rich_message
        is_rtl = None
        skip_entity_detection = None
        if isinstance(rich_message, types.InputRichMessage):
            is_rtl = rich_message.is_rtl
            skip_entity_detection = rich_message.skip_entity_detection
            if rich_message.markdown:
                raw_rich = rich_message.markdown
            elif rich_message.html:
                raw_rich = rich_message.html
            else:
                raw_rich = rich_message

        return await self.send_message(
            chat_id=chat_id,
            text=None,
            rich_message=raw_rich,
            is_rtl=is_rtl,
            skip_entity_detection=skip_entity_detection,
            business_connection_id=business_connection_id,
            message_thread_id=message_thread_id,
            direct_messages_topic_id=direct_messages_topic_id,
            disable_notification=disable_notification,
            protect_content=protect_content,
            allow_paid_broadcast=allow_paid_broadcast,
            effect_id=message_effect_id,
            suggested_post_parameters=suggested_post_parameters,
            reply_parameters=reply_parameters,
            reply_markup=reply_markup,
            ephemeral_message_parameters=ephemeral_message_parameters,
            receiver_user_id=receiver_user_id,
            callback_query_id=callback_query_id,
        )
