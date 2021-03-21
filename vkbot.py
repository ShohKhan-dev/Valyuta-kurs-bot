import json, urllib
from urllib.request import Request, urlopen
import telebot
import time
from telebot import types

url = "https://nbu.uz/uz/exchange-rates/json/"

response = urllib.request.urlopen(url)

data = json.loads(response.read())
usz = {"title": "O'zbekiston so'mi", 'code': "USZ", "cb_price": "1"}
data.append(usz)

name = [n['title'] for n in data]


bot = telebot.TeleBot(token = '1616823598:AAFAW1TluZerp4JQ3PQsDJtnbgqSbjyeg6I')

first = True
second = False

from_cur = 0
to_cur = 0

from_name = ""
to_name = ""


one = types.KeyboardButton("O'zbekiston so'mi")
two = types.KeyboardButton("AQSh dollari")
        
three = types.KeyboardButton("Rossiya rubli")
four = types.KeyboardButton("Yevro")
        
five = types.KeyboardButton("Koreya respublikasi voni")
six = types.KeyboardButton("Xitoy yuani")
        
seven = types.KeyboardButton("Qozog‘iston tengesi")
eight = types.KeyboardButton("Turkiya lirasi")

back = types.KeyboardButton("Orqaga")
        

        
        
def check(country):
    global name
    
    if country in name:
        return True
    return False


@bot.message_handler(commands=['start'])

def starting(message):
    global one, two, three, four, five, six, seven, eight

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)


    markup.add(one, two)
    markup.add(three, four)
    markup.add(five, six)
    markup.add(seven, eight)
    
    bot.send_message(message.chat.id,'Bu bot Valyuta kurslar. Valyuta tanlang',reply_markup=markup, parse_mode='markdown')

    


@bot.message_handler(content_types=['text'], func = lambda message: check(message.text) and first)

def get_from(message):
    global first, one, two, three, four, five, six, seven, eight, back, from_cur, from_name
    
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    
    markup.add(one, two)
    markup.add(three, four)
    markup.add(five, six)
    markup.add(seven, eight)

    markup.add(back)

    for i in data:
        if i['title'] == message.text:
            from_name = message.text
            from_cur = float(i['cb_price'])
            break

    bot.send_message(message.chat.id,'Endi almashtiradigon valyuta tanlang for: ' + message.text,reply_markup=markup, parse_mode='markdown')
    first = False
        
    

    

@bot.message_handler(content_types=['text'], func = lambda message: check(message.text) and not first)

def get_to(message):
    global first, second, to_cur, to_name
    first = True
    second = True
    
    for i in data:
        if i['title'] == message.text:
            to_name = message.text
            to_cur = float(i['cb_price'])
            break

    bot.send_message(message.chat.id,'valueni kirit: ')
    




@bot.message_handler(content_types=['text'], func = lambda message: message.text.replace('.','',1).isdigit() and first and second)

def get_value(message):
    global from_cur, to_cur, from_name, to_name


    value = float(message.text)
    currency = (from_cur/to_cur) * value

    usul = from_name + ' -> ' + to_name+ '\n'

    
    bot.send_message(message.chat.id, usul+'converted: '+ str(currency))




@bot.message_handler(content_types=['text'], func = lambda message: message.text.replace('.','',1).isdigit())
def get_value(message):
    global from_cur, to_cur, first, second

    if not first or not second:
        bot.send_message(message.chat.id,"Iltimos avval valyuta kurlarini tanlang!")



        
@bot.message_handler(content_types=['text'], func = lambda message: not message.text.replace('.','',1).isdigit() and first and second)
def get_value(message):

    bot.send_message(message.chat.id,"Iltimos faqat konvertatsiya qilinadigon summa kiriting!\nMasalan: 100 yoki 100.45")



    
@bot.message_handler(content_types=['text'], func = lambda message: not check(message.text))
def get_value(message):
    global from_cur, to_cur, first, second

    bot.send_message(message.chat.id,"Iltimos avval valyuta kurlarini tanlang!")
        



    

while True:
    try:
        bot.polling()
    except Exception:
        time.sleep(15)


