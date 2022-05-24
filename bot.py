from telegram.ext import Updater
prod = False
if prod:
    from secret import token
    updater = Updater(token=token, use_context=True)
else:
    updater = Updater(token="2108324100:AAGXQWr1qD4VmJl4qpBV7YGuz5ilHlAkgHs", use_context=True)

dispatcher = updater.dispatcher

import logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)

from telegram import Update
from telegram.ext import CallbackContext

from random import randint

replies = ["Ты что реально на это подписан?",
           "Не пости либертоду, не позорься."]

tg_replies = ['Вы упомянули трансгуманизм. Вы Артём Александров?', 
            'Вы упомянули трансгуманизм. Попробуйте писать сообщения короче.']

from datetime import datetime
class Timer():
    timers = {}
    interval = 2 #minutes between replies EDIT AT YOUR LIKING
    def __init__(self, label):
        if label in Timer.timers.keys():
            self.last_invoked = Timer.timers[label].last_invoked #inelegant way to retriev class ;) 
            self.label = label
            return
        self.last_invoked = datetime(2010, 9, 12, 11, 19, 54) #random copypaste, setting far date to allow first triggering
        self.label = label
        Timer.timers[label] = self
    def check(self):
        if (datetime.now()-self.last_invoked).total_seconds()/60>Timer.interval:
            print(self.label, self.last_invoked)
            self.last_invoked = datetime.now()
            return True
        return False

from telegram.ext import MessageHandler, Filters
def chat_sender_handler(update: Update, context: CallbackContext):
    message = update.message
    if message is None:
        return
    sender = message.from_user

    # mention generation
    if sender is not None:
        mention = sender.username
        if mention is None:
            mention = ''
            if sender.first_name:
                mention+=sender.first_name
            if sender.last_name:
                mention+=' '+sender.last_name
            mention = mention.strip()
        else:
            mention = "@"+mention

    if message.sender_chat:
        context.bot.ban_chat_sender_chat(chat_id=update.effective_chat.id, sender_chat_id=message.sender_chat.id)
        context.bot.send_message(chat_id=update.effective_chat.id, text=f"Забанил новый канал Имя: {message.sender_chat.title} - Тег: {message.sender_chat.username}!")
    elif message.forward_from_chat:
        if message.forward_from_chat.id in (-1001522560514,-1001513669961):
            context.bot.deleteMessage(chat_id=update.message.chat.id, message_id=update.message.message_id)
            if Timer('label0').check():
                context.bot.send_message(chat_id=update.effective_chat.id, text=f"{mention} "+replies[randint(0,len(replies)-1)])
    elif message.text:
        if 'twitter.com/svtv_news' in message.text:
            context.bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
            if Timer('label1').check():
                context.bot.send_message(chat_id=update.effective_chat.id, text=f"{mention} "+replies[randint(0,len(replies)-1)])
        elif "либерт" in message.text.lower():
            if Timer('label2').check():
                context.bot.send_message(reply_to_message_id=message.message_id, chat_id=update.effective_chat.id, text="Вы упомянули либертарианство. Если вы либертарианец, то вас принудительно вакцинируют.")
        elif "светов" in message.text.lower():
            if Timer('label3').check():
                context.bot.send_message(reply_to_message_id=message.message_id, chat_id=update.effective_chat.id, text="Вы упомянули Светова.... Зачем?")
        elif "трансгум" in message.text.lower() or "трансгум" in message.text.lower():
            if Timer('label4').check():
                context.bot.send_message(reply_to_message_id=message.message_id, chat_id=update.effective_chat.id, text=tg_replies[randint(0,len(tg_replies)-1)])
dispatcher.add_handler(MessageHandler(Filters.update, chat_sender_handler))


updater.start_polling()
