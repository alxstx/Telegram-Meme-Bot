import telebot
from PIL import Image
from telebot import types
import time
import datetime as dt
import os
import threading


# you can deploy this bot on Heroku
bot = telebot.TeleBot('your token')
txt = '''
This is a meme bot. He sends you memes and you can
rate them. If you press 😂 he will only send you a new meme.
If you press 😶 he will delete this meme and send you a new. If you 
write "enough for today" in the chat the bot will stop sending you memes, 
if you send then "i need memes" he will send you memes again
If you want to change the language of the memes: write /lang
and choose the language you want
The source code you can see on Github on this account: alxstx
Also you can check my instagram: alx_stx 

'''
txtrus = '''
Это мем бот. Он тебе отправляет различные мемы который ты 
можешь оценить. Если ты нажимаешь на 😂 под мемом бот тебе отправляет новый
мем. А если ты нажимаешь на 😶 он удаляет этот  мем и присылает тебе новый. Если ты 
напишешь "я устал смотреть мемы" в чат то бот перестанет тебе присылать мемы,
если ты ему после этого напишешь "мне нужны мемы" он возобновит отправку мемов.
Если ты хочешь поменять язык на инглиш: напиши боту /lang и выбери язык
Исходный код будет на Гитхабе на этом аккаунте: alxstx
Также ты можень подписаться на автора в инсте: alx_stx ПОДПИШИСЬ плиз🙏
'''
picturesrus = []
pictureseng = []
enough_list = []
meme_counter_list = []
set_lang = ['English']


def photo_handler(photo, lang='eng'):
    pict = Image.open(photo)
    if lang == 'rus':
        picturesrus.append(pict)
    else:
        pictureseng.append(pict)


def add_photos():
    for i in os.listdir('memesworldclass'):
        photo_handler(photo='memesworldclass/' + i)  # you have to change the path


def add_rusphotos():
    for j in os.listdir('pcixoff'):
        photo_handler(photo='pcixoff/' + j,
                      lang='rus')  # you have to change the path


t = threading.Thread(target=add_photos)
tt = threading.Thread(target=add_rusphotos)
t.start()
tt.start()


def photo_sender(message):
    mark = types.InlineKeyboardMarkup(row_width=2, )
    btn1 = types.InlineKeyboardButton(text='😂', callback_data='funny')
    btn2 = types.InlineKeyboardButton(text='😶', callback_data='lame')
    mark.add(btn1, btn2)
    time.sleep(1)
    if 'Russian' in set_lang:
        if picturesrus == []:
            add_rusphotos()
        else:
            bot.send_photo(message.chat.id, picturesrus[0], reply_markup=mark)
            del picturesrus[0]
    else:
        if pictureseng == []:
            add_photos()
        else:
            bot.send_photo(message.chat.id, pictureseng[0], reply_markup=mark)
            del pictureseng[0]


@bot.message_handler(commands=['start', 'help'])
def start_text(message):
    mark = types.InlineKeyboardMarkup(row_width=2, )
    btn1 = types.InlineKeyboardButton(text='По русски плз', callback_data='russia')
    btn2 = types.InlineKeyboardButton(text='OK', callback_data='thisisokay')
    mark.add(btn1, btn2)
    bot.send_message(message.chat.id, txt, reply_markup=mark)
    meme_counter_list.append('watched')


@bot.message_handler(commands=['lang'])
def set_lange(message):
    mark = types.InlineKeyboardMarkup(row_width=2, )
    btn1 = types.InlineKeyboardButton(text='English🇬🇧', callback_data='inglish')
    btn2 = types.InlineKeyboardButton(text='Russian🇷🇺', callback_data='russkiya')
    mark.add(btn1, btn2)
    time.sleep(1)
    bot.send_message(message.chat.id, text='Choose a language🤔', reply_markup=mark)


@bot.message_handler(content_types=['text'])
def send_meme(message):
    if message.text:
        if 'Russian' in set_lang:
            bot.send_message(message.chat.id, text='Достаточно мемов на сегодня?')
        else:
            bot.send_message(message.chat.id, text='Enough memes for today?')


@bot.callback_query_handler(func=lambda mess: True)
def callback(call):
    if call.data == 'russia':
        set_lang.clear()
        set_lang.append('Russian')
        bot.delete_message(call.message.chat.id, call.message.message_id)
        bot.send_message(call.message.chat.id, txtrus)
        photo_sender(call.message)
    elif call.data == 'thisisokay':
        bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id, reply_markup=None)
        set_lang.clear()
        set_lang.append('English')
        photo_sender(call.message)
    if call.data == 'funny':
        if dt.datetime.now().hour == 00 or 0:
            meme_counter_list.clear()
        bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id, reply_markup=None)
        if meme_counter_list.count('watched') == 50:
            if 'Russian' not in set_lang:
                bot.send_message(call.message.chat.id, 'You already watched 50 memes! Is it not enough for today?')
            else:
                bot.send_message(call.message.chat.id, 'Ты уже посмотрел 50 МЕМОВ! Может хватит?')
            time.sleep(5)
            meme_counter_list.append('watched')

        elif meme_counter_list.count('watched') > 99 and meme_counter_list.count('watched') % 10 == 0:
            if 'Russian' in set_lang:
                photo = Image.open('kot.jpeg')
                bot.send_photo(call.message.chat.id, photo)
                bot.send_message(call.message.chat.id, 'Перестань смотреть мемы, ИДИ РАБОТАЙ!!!')
                time.sleep(5)
            else:
                photo = Image.open('badmeme.jpg')
                bot.send_photo(call.message.chat.id, photo)
                bot.send_message(call.message.chat.id, 'Stop watching memes, GO WORK!!!')
                time.sleep(5)
        if not bool(enough_list):
            photo_sender(call.message)
            meme_counter_list.append('watched')
    elif call.data == 'lame':
        bot.delete_message(call.message.chat.id, call.message.message_id)
        if not bool(enough_list):
            photo_sender(call.message)
            meme_counter_list.append('watched')
    if call.data == 'inglish':
        set_lang.clear()
        set_lang.append('English')
        bot.delete_message(call.message.chat.id, call.message.message_id)
    elif call.data == 'russkiya':
        set_lang.clear()
        set_lang.append('Russian')
        bot.delete_message(call.message.chat.id, call.message.message_id)


bot.polling(none_stop=True, interval=0)
