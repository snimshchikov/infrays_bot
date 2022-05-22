from telegram.ext import Updater
from secret import token
updater = Updater(token=token, use_context=True)

dispatcher = updater.dispatcher

import logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)

from telegram import Update
from telegram.ext import CallbackContext

from random import randint

replies = ["Ты что реально на это подписан?",
            "Не пости либертоду, не позорься.",
            "Миша Светов трахнул шкетов.",
            "СВТВ? Продай мать сразу пожалуйста."]

from telegram.ext import MessageHandler, Filters
def chat_sender_handler(update: Update, context: CallbackContext):
    message = update.message
    if message is None:
        return
    sender = message.from_user
    if sender is not None:
        mention = sender.username
        if mention is None:
            mention = sender.first_name + ' ' + sender.last_name
        else:
            mention = "@"+mention
    if message.sender_chat:
        context.bot.ban_chat_sender_chat(chat_id=update.effective_chat.id, sender_chat_id=message.sender_chat.id)
        context.bot.send_message(chat_id=update.effective_chat.id, text=f"Забанил новый канал Имя: {message.sender_chat.title} - Тег: {message.sender_chat.username}!")
    elif message.forward_from_chat:
        if message.forward_from_chat.id in (-1001522560514,-1001513669961):
            context.bot.deleteMessage(chat_id=update.message.chat.id, message_id=update.message.message_id)
            context.bot.send_message(chat_id=update.effective_chat.id, text=f"{mention} "+replies[randint(0,len(replies))])
    elif message.text:
        if 'twitter.com/svtv_news' in message.text:
            context.bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
            context.bot.send_message(chat_id=update.effective_chat.id, text=f"{mention} "+replies[randint(0,len(replies))])
        elif "либерт" in message.text.lower():
            context.bot.send_message(reply_to_message_id=message.message_id, chat_id=update.effective_chat.id, text="Вы упомянули либертарианство. Если вы либертарианец, то вас принудительно вакцинируют.")
        elif "светов" in message.text.lower():
            context.bot.send_message(reply_to_message_id=message.message_id, chat_id=update.effective_chat.id, text="Вы упомянули Светова.... Зачем?")
dispatcher.add_handler(MessageHandler(Filters.update, chat_sender_handler))


updater.start_polling()
