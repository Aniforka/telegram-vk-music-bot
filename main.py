import telebot
import vk_audio
import pandas as pd
from requests import get

count_p = {}
audios_p = {}
kind_p = {}
const_p = {}
ids_p = {}
saves_p = {}
g_p = {}

token = ''

bot = telebot.TeleBot(token)

def edit_c(message):
    try:
        c = int(message.text)
    except Exception:
        markup = telebot.types.InlineKeyboardMarkup()
        key_menu = telebot.types.InlineKeyboardButton(text='Вернуться в меню', callback_data='general_menu')
        markup.add(key_menu)
        bot.send_message(chat_id=message.chat.id, text='Вы ввели не число!', reply_markup=markup)
    else:
        if(c <= 0):
            markup = telebot.types.InlineKeyboardMarkup()
            key_menu = telebot.types.InlineKeyboardButton(text='Вернуться в меню', callback_data='general_menu')
            markup.add(key_menu)
            bot.send_message(chat_id=message.chat.id, text='Вы ввели не положительное число!', reply_markup=markup)
        else:
            const_p[message.chat.id] = c
            markup = telebot.types.InlineKeyboardMarkup()
            key_menu = telebot.types.InlineKeyboardButton(text='Вернуться в меню', callback_data='general_menu')
            markup.add(key_menu)
            bot.send_message(chat_id=message.chat.id, text='Вы успешно ввели число!', reply_markup=markup)

def find_title(zap):
    vk = vk_audio.VkAudio(login='+971502771131', password='12345das')
    data = vk.search(zap)
    audios = data.Audios

    return audios

def find_artist(nickname):
    vk = vk_audio.VkAudio(login='+971502771131', password='12345das')
    audios = vk.load_artist(artist_nickname=nickname).Audios

    return audios

def find_artist_beta(nickname):
    vk = vk_audio.VkAudio(login='+971502771131', password='12345das')
    data = vk.search(nickname)
    audios = data.Audios
    audios_r = []
    ns = ''

    for s1 in nickname.split(' '):
        ns += s1.lower()
    for au in audios:
        s = ''
        for s1 in au['artist'].split(' '):
            s += s1.lower()
        if(s.find(ns) != -1):
            audios_r.append(au)

    return audios_r

def create_markup(c, k, audios, save):
    markup = telebot.types.InlineKeyboardMarkup()

    if(save):
        key_save = telebot.types.InlineKeyboardButton(text='✅', callback_data='save')
    else:
        key_save = telebot.types.InlineKeyboardButton(text='❌', callback_data='save')

    if(k == c-1 and k < len(audios)-1):
        key_menu = telebot.types.InlineKeyboardButton(text='Меню', callback_data='general_menu')
        key_next = telebot.types.InlineKeyboardButton(text='⟶', callback_data='next')
        markup.add(key_menu, key_next, key_save)
    elif(k > c-1 and k < len(audios)-1):
        key_previous = telebot.types.InlineKeyboardButton(text='⟵', callback_data='previous')
        key_menu = telebot.types.InlineKeyboardButton(text='Меню', callback_data='general_menu')
        key_next = telebot.types.InlineKeyboardButton(text='⟶', callback_data='next')
        markup.add(key_previous, key_menu, key_next, key_save)
    elif(k > c-1 and k == len(audios)-1):
        key_previous = telebot.types.InlineKeyboardButton(text='⟵', callback_data='previous')
        key_menu = telebot.types.InlineKeyboardButton(text='Меню', callback_data='general_menu')
        markup.add(key_previous, key_menu, key_save)
    else:
        key_menu = telebot.types.InlineKeyboardButton(text='Меню', callback_data='general_menu')
        markup.add(key_menu)

    return markup



@bot.message_handler(commands=['start'])
def start_message(message):
    markup = telebot.types.InlineKeyboardMarkup()
    key_menu = telebot.types.InlineKeyboardButton(text='Меню', callback_data='general_menu')
    markup.add(key_menu)
    bot.send_message(chat_id=message.chat.id, text='Добро пожаловать в Music Bot!', reply_markup=markup)



@bot.message_handler(content_types=['text'])
def send_text(message):
    global kind_p
    global saves_p
    if(saves_p.get(message.chat.id) == None):
        saves_p[message.chat.id] = False

    f = True

    if(kind_p.get(message.chat.id) == None):
        markup = telebot.types.InlineKeyboardMarkup()
        key_title = telebot.types.InlineKeyboardButton(text='По названию', callback_data='title')
        key_menu = telebot.types.InlineKeyboardButton(text='Вернуться в меню', callback_data='general_menu')
        key_artist = telebot.types.InlineKeyboardButton(text='По исполнителю', callback_data='artist')
        markup.add(key_title, key_menu, key_artist)
        bot.send_message(chat_id=message.chat.id, text='Вы не выбрали режим поиска!', reply_markup=markup)

    else:
        global ids_p
        global const_p
        global audios_p
        global count_p

        if(const_p.get(message.chat.id) == None):
            const_p[message.chat.id] = 1

        if(kind_p.get(message.chat.id) == 'title'):
            try:
                audios_p[message.chat.id] = find_title(message.text)
                audios = audios_p[message.chat.id]
            except Exception:
                markup = telebot.types.InlineKeyboardMarkup()
                key_menu = telebot.types.InlineKeyboardButton(text='Вернуться в меню', callback_data='general_menu')
                markup.add(key_menu)
                bot.send_message(chat_id=message.chat.id, text='Невозможно найти песню.', reply_markup=markup)
                f = False

        if(kind_p.get(message.chat.id) == 'artist'):
            s = ''

            for s1 in message.text.split(' '):
                s += s1.lower()

            try:
                audios_p[message.chat.id] = find_artist(s)
                audios = audios_p[message.chat.id]
            except Exception:
                try:
                    audios_p[message.chat.id] = find_artist_beta(message.text)
                    audios = audios_p[message.chat.id]
                except Exception:
                    markup = telebot.types.InlineKeyboardMarkup()
                    key_menu = telebot.types.InlineKeyboardButton(text='Вернуться в меню', callback_data='general_menu')
                    markup.add(key_menu)
                    bot.send_message(chat_id=message.chat.id, text='Невозможно найти исполнителя.', reply_markup=markup)
                    f = False

        if(f):
            c = const_p[message.chat.id]

            count_p[message.chat.id] = 0
            k = count_p[message.chat.id]
            ids = []

            for i in range(c):
                if(k <= len(audios)-1):
                    title = audios[k]['title']
                    performer = audios[k]['artist']
                    duration = audios[k]['duration']
                    url = audios[k]['url']
                    mess_id = bot.send_message(chat_id=message.chat.id, text='Ищем песню…\nПожалуйста, подождите 3-5 сек.').id

                    if(i+1 == c or k == len(audios)-1):
                        ids.append(bot.send_audio(chat_id=message.chat.id, title=title, performer=performer, duration=duration, audio=get(url).content, reply_markup=create_markup(c, k, audios, saves_p[message.chat.id])).id)
                    else:
                        ids.append(bot.send_audio(chat_id=message.chat.id, title=title, performer=performer, duration=duration, audio=get(url).content).id)
                    
                    bot.delete_message(chat_id=message.chat.id, message_id=mess_id)

                    k += 1
                    count_p[message.chat.id] += 1
                    ids_p[message.chat.id] = ids



@bot.callback_query_handler(func = lambda call: True)
def callback_inline(call):
    global kind_p
    global ids_p
    global saves_p

    if(call.data == 'next' or call.data == 'previous'):
        global g_p

        if(g_p.get(call.message.chat.id) == None):
            g_p[call.message.chat.id] = 0
        
        global const_p

        if(const_p.get(call.message.chat.id) == None):
            const_p[call.message.chat.id] = 1
        c = const_p[call.message.chat.id]

        global count_p

        if(count_p.get(call.message.chat.id) == None):
            count_p[call.message.chat.id] = 0
        k = count_p[call.message.chat.id] if call.data == 'next' else count_p[call.message.chat.id]-c-g_p[call.message.chat.id]

        global audios_p

        audios = audios_p[call.message.chat.id]

        if(not saves_p[call.message.chat.id]):
            for id_p in ids_p[call.message.chat.id]:
                bot.delete_message(chat_id=call.message.chat.id, message_id=id_p)

        ids = []
        g_p[call.message.chat.id] = 0

        for i in range(c):
            if(k <= len(audios)-1):
                title = audios[k]['title']
                performer = audios[k]['artist']
                duration = audios[k]['duration']
                url = audios[k]['url']
                mess_id = bot.send_message(chat_id=call.message.chat.id, text='Ищем песню…\nПожалуйста, подождите 3-5 сек.').id
                
                if(i+1 == c or k == len(audios)-1):
                    ids.append(bot.send_audio(chat_id=call.message.chat.id, title=title, performer=performer, duration=duration, audio=get(url).content, reply_markup=create_markup(c, k, audios, saves_p[call.message.chat.id])).id)
                else:
                    ids.append(bot.send_audio(chat_id=call.message.chat.id, title=title, performer=performer, duration=duration, audio=get(url).content).id)
                
                bot.delete_message(chat_id=call.message.chat.id, message_id=mess_id)

                k += 1
                count_p[call.message.chat.id] += 1
                g_p[call.message.chat.id] += 1
                ids_p[call.message.chat.id] = ids

    if(call.data == 'title'):
        kind_p[call.message.chat.id] = 'title'
        bot.send_message(chat_id=call.message.chat.id, text='Введите название песни.')

    if(call.data == 'artist'):
        kind_p[call.message.chat.id] = 'artist'
        bot.send_message(chat_id=call.message.chat.id, text='Введите имя исполнителя.')

    if(call.data == 'general_menu'):
        markup = telebot.types.InlineKeyboardMarkup()
        key_title = telebot.types.InlineKeyboardButton(text='Поиск по названию', callback_data='title')
        key_artist = telebot.types.InlineKeyboardButton(text='Поиск по исполнителю', callback_data='artist')
        key_edit = telebot.types.InlineKeyboardButton(text='Количество песен', callback_data='edit_const')
        key_boosty = telebot.types.InlineKeyboardButton(text='Boosty создателя', url='https://boosty.to/anifor')
        markup.add(key_title, key_artist, key_edit, row_width=2)
        markup.add(key_boosty)
        bot.send_message(chat_id=call.message.chat.id, text='Вы находитесь в главном меню.\nВыберите одну из предложенных функций.', reply_markup=markup)
    
    if(call.data == 'edit_const'):
        bot.send_message(chat_id=call.message.chat.id, text='Вы попали в меню изменения количества показываемых аудиозаписей во время поиска.\nВведите число.')
        bot.register_next_step_handler(message=call.message, callback=edit_c)
    
    if(call.data == 'save'):
        if(saves_p.get(call.message.chat.id) == None):
            saves_p[call.message.chat.id] = False

        saves_p[call.message.chat.id] = not saves_p[call.message.chat.id]

        mark = call.message.json['reply_markup']['inline_keyboard']
        but = []

        for buttons in mark:
            for button in buttons:
                if(button['callback_data'] == 'save'):
                    text = '✅' if saves_p[call.message.chat.id] else '❌'
                else:
                    text = button['text']
                but.append(telebot.types.InlineKeyboardButton(text=text, callback_data=button['callback_data']))

        but1 = [but]
        markup = telebot.types.InlineKeyboardMarkup(but1)
        bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.id, reply_markup=markup)

bot.polling(none_stop= True, interval= 0)