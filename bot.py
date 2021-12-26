from telegram.ext import Updater
from secret import token
updater = Updater(token=token, use_context=True)

dispatcher = updater.dispatcher

import logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)

from telegram import Update
from telegram.ext import CallbackContext


from telegram.ext import MessageHandler, Filters
def chat_sender_handler(update: Update, context: CallbackContext):
    message = update.message
    if message.sender_chat:
        context.bot.ban_chat_sender_chat(chat_id=update.effective_chat.id, sender_chat_id=message.sender_chat.id)
        context.bot.send_message(chat_id=update.effective_chat.id, text=f"Забанил новый канал Имя: {message.sender_chat.title} - Тег: {message.sender_chat.username}!")
dispatcher.add_handler(MessageHandler(Filters.update, chat_sender_handler))


updater.start_polling()
