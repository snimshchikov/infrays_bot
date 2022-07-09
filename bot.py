from random import randint
import os
import logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)

from aiogram import Bot, Dispatcher, executor, types

from db import DB
from secret import TOKEN

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

db = DB(os.path.join('.','db','bot.db'))

replies = ["Ты что реально на это подписан?",
           "Не пости либертоду, не позорься."]

legion_replies = ["Новости Легиона, остаются в канале Легиона."]

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
swears = [
    "говно",
    "залупа",
    "отрыжка пидораса",
    "хер",
    "пидор",
    "да.\nПизда",
    "хуй",
    "малафья",
    "Анус Потрепидзе",
    "днище ебаное",
    "светист ебаный",
    "дочка конееба",
    "овощ гнилой",
]
prefix_swears = [
    "Алгоритмы подсказали, что ты ",
    "Ты кстати ",
    "Миру мир, а ты ",
    "В огороде бузина, а ты ",
    "Сейчас я вам покажу откуда на Беларусь готовилось нападение. И если бы не ты ",
]
@dp.message_handler()
async def chat_sender_handler(message: types.Message):
    if message is None:
        return
    sender = message.from_user

    first_last_names = ""
    if sender.first_name:
        first_last_names+=sender.first_name
    if sender.last_name:
        first_last_names+=' '+sender.last_name
    first_last_names = first_last_names.strip()
    # mention generation
    if sender is not None:
        mention = sender.username
        if mention is None:
            mention = first_last_names
        else:
            mention = "@"+mention
    if message.chat.id in {-1001176998310,-1001154772762}: #ID OF KATZBOTS and TEST CHANNEL
        await db.add_message(sender.id, first_last_names, message.date.timestamp(), message.text)
    if message.sender_chat:
        await bot.ban_chat_sender_chat(chat_id=message.chat.id, sender_chat_id=message.sender_chat.id)
        await bot.send_message(chat_id=message.chat.id, text=f"Забанил новый канал Имя: {message.sender_chat.title} - Тег: {message.sender_chat.username}!")
    elif message.forward_from_chat and message.chat.id in {-1001176998310,-1001154772762}:
        if message.forward_from_chat.id in {-1001522560514,-1001513669961}: # SVTV news and I don't know what else
            await message.delete()
            if Timer('label0').check():
                await bot.send_message(chat_id=message.chat.id, text=f"{mention} "+replies[randint(0,len(replies)-1)])
        elif message.forward_from_chat.id in {-1001227769643,}: # legion id
            await message.delete()
            if Timer('label_legion').check():
                await bot.send_message(chat_id=message.chat.id, text=f"{mention} "+legion_replies[randint(0,len(legion_replies)-1)])
    elif message.text and message.chat.id in {-1001176998310,-1001154772762}:
        if randint(0,20)==1:
            await message.reply(text=prefix_swears[randint(0,len(prefix_swears)-1)]+swears[randint(0,len(swears)-1)]+' 😉')
        lower_text = message.text.lower()
        if 'twitter.com/svtv_news' in lower_text or 'svtv.org' in lower_text:
            await message.delete()
            if Timer('label1').check():
                await bot.send_message(chat_id=message.chat.id, text=f"{mention} "+replies[randint(0,len(replies)-1)])
        elif "либерт" in lower_text:
            if Timer('label2').check():
                await message.reply(text="Вы упомянули либертарианство. Если вы либертарианец, то вас принудительно вакцинируют.")
        elif "светов" in lower_text:
            if Timer('label3').check():
                await message.reply(text="Вы упомянули Светова.... Зачем?")
        elif "трансгум" in lower_text or "трансгум" in lower_text:
            if Timer('label4').check():
                await message.reply(text=tg_replies[randint(0,len(tg_replies)-1)])
        elif "иноаг" in lower_text and not message.forward_from_chat:
            if Timer('label5').check():
                await message.reply(text=
                    "ДАННОЕ СООБЩЕНИЕ (МАТЕРИАЛ) СОЗДАНО И (ИЛИ) РАСПРОСТРАНЕНО ИНОСТРАННЫМ СРЕДСТВОМ МАССОВОЙ "+\
                    "ИНФОРМАЦИИ, ВЫПОЛНЯЮЩИМ ФУНКЦИИ ИНОСТРАННОГО АГЕНТА, И (ИЛИ) РОССИЙСКИМ ЮРИДИЧЕСКИМ ЛИЦОМ, "+\
                    "ВЫПОЛНЯЮЩИМ ФУНКЦИИ ИНОСТРАННОГО АГЕНТА"
                )
if __name__ == '__main__':
    executor.start_polling(dp)
