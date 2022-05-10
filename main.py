import random
import time
import requests
from config import BOT_API, MAIN_ADMIN, HELPER_LIST, ADMINS
from random import choice
import telebot
import database
import keyboards

bot = telebot.TeleBot(BOT_API)
db = database
keyboard = keyboards

#  Глобальные переменные
working = False
a, b = random.randrange(10000), random.randrange(10000)
prim = random.choice([(f'{a} + {b}', a + b), (f'{a} - {b}', a - b), (f'{a} * {b}', a * b)])
trade = False

#  КОМАНДЫ АДМИНА

@bot.message_handler(commands=['alert'])
def alert(message):
    if message.chat.id == MAIN_ADMIN:
        if ';' in message.text:
            text = message.text.split()[1]
            text = text.split(';')
            count = 0
            p = requests.get(text[1])
            out = open("temp.jpg", "wb")
            out.write(p.content)
            out.close()
            for i in db.users():
                try:
                    bot.send_photo(i[0], open('temp.jpg', 'rb'), caption=text[0], parse_mode='html')
                    time.sleep(0.3)
                    count += 1
                except:
                    raise
            bot.send_message(message.chat.id, f'Сообщений доставлено - {count}')
        else:
            text = message.text.split()[1]
            count = 0
            for i in db.users():
                try:
                    bot.send_message(i[0], text)
                    time.sleep(0.3)
                    count += 1
                except:
                    raise
            bot.send_message(message.chat.id, f'Сообщений доставлено - {count}')


@bot.message_handler(commands=['ban'])
def ban(message):
    if message.chat.id in HELPER_LIST or message.chat.id == MAIN_ADMIN:
        try:
            ll = message.text.split(' ')
            db.ban(ll[1], ll[2])
            info = db.get_info(ll[1])
            if info[0][6] == 1:
                bot.send_message(message.chat.id, 'Вы разбанили юзера.')
            else:
                bot.send_message(message.chat.id, 'Вы забанили юзера.')


        except:
            bot.send_message(message.chat.id, 'Ошибка!')


@bot.message_handler(commands=['setmoney'])
def set_money(message):
    if message.chat.id == MAIN_ADMIN or message.chat.id in ADMINS:
        kor = message.text.split()
        db.set_money(kor[1], kor[2])
        bot.send_message(message.chat.id, 'Успешно!')


@bot.message_handler(commands=['info'])
def info(message):
    if message.chat.id == MAIN_ADMIN or message.chat.id in ADMINS:
        idd = message.text.split()[1]
        info = db.get_info(idd)[0]
        bot.send_message(message.chat.id,
        f'<b>{info[4]}</b>\n________________________\nБаланс равен {str(info[1])}\n{str(info[2])}\
 LVL копания\nДата регистрации: {str(info[3])}\n________________________\n', parse_mode='HTML')


#  РЯД КОМАНД ОБЫЧНОГО ПОЛЬЗОВАНИЯ
@bot.message_handler(commands=['start'])
def welcome(message):
    if not db.check_atz(message.chat.id):
        bot.send_message(message.chat.id, f'Добро пожаловать <b>{message.from_user.first_name}</b>', parse_mode='HTML',
                         reply_markup=keyboard.main_k())
    else:
        bot.send_message(message.chat.id, f'Добро пожаловать <b>{message.from_user.first_name}</b>', parse_mode='HTML',
                         reply_markup=keyboard.autor_k())
        db.autorization(message.chat.id, message)
        mess = bot.send_message(message.chat.id, 'Для продолжения работы с ботом прочтите правила\n БЛА БЛА БЛА',
                                reply_markup=keyboard.rules_k())
        db.set_id_mess(message.chat.id, mess.message_id)


#  ОБРАБОТЧИК СООБЩЕНИЙ
@bot.message_handler(content_types=['text'])
def texting(message):
    global working
    global prim
    global info
    global trade
    if working:
        if message.text == 'СТОП':
            bot.send_message(message.chat.id, 'Раскопки окончены.', reply_markup=keyboard.main_k())
            working = False
            time.sleep(1)
            return
        elif message.text == str(prim[1]):
            bot.send_message(message.chat.id, 'Молодец, держи еще пример.')
            db.add_money(message.from_user.id, str(500 * db.get_info(message.from_user.id)[0][2]))
            a, b = random.randrange(10000), random.randrange(10000)
            prim = random.choice([(f'{a} + {b}', a + b), (f'{a} - {b}', a - b), (f'{a} * {b}', a * b)])
            bot.send_message(message.chat.id, prim[0])
        else:
            bot.send_message(message.chat.id, 'Неправильно, попробуй еще раз.')
    elif trade:
        if message.text == 'Вернуться в меню.':
            bot.send_message(message.chat.id, 'Воспользуйтесь меню снизу...', reply_markup=keyboard.main_k())
            trade = False
            return
        elif len(message.text.split()) != 2:
            bot.send_message(message.chat.id, 'Введите все по форме')
            return
        elif len(message.text.split()[1]) != 16:
            bot.send_message(message.chat.id, 'Введите правильный номер карты')
            return
        elif int(message.text.split()[0]) < 100000000000:
            bot.send_message(message.chat.id, 'Минимальная сумма для вывода 10 руб')
            return
        elif int(message.text.split()[0]) > int(db.get_info(message.from_user.id)[0][1]):
            bot.send_message(message.chat.id, f'Недостаточно средств.')
            return
        else:
            bot.send_message(message.chat.id, f'Запрос на вывод {int(message.text.split()[0]) // 10000000000} руб. получен.')
    else:
        if message.text == 'Информация':
            info = db.get_info(message.chat.id)[0]
            if message.chat.id == MAIN_ADMIN:
                admin_info = db.get_info_admin()
                bot.send_message(message.chat.id, f'Ваш баланс равен {str(info[1])}\n{str(info[2])}\
     LVL копания\nДата регистрации: {str(info[3])}\n________________________\nКол-во юзеров: \
    {admin_info[0]}\n Последний юзер: {admin_info[1][0]}')
            else:
                bot.send_message(message.chat.id, f'Ваш баланс равен {str(info[1])}\n{str(info[2])}\
     LVL копания\nДата регистрации: {str(info[3])}')
        if message.text == 'Помощь':
            msg = bot.send_message(message.chat.id, '<b>Напишите обращение чётко указав проблему, вскоре\
             с вами свяжется оператор ТП</b>', parse_mode='HTML')
            bot.register_next_step_handler(msg, help_send)

        if message.text == 'Раскопки':
            msg = bot.send_message(message.chat.id, 'Через 3 секунды начнётся игра.')
            time.sleep(1)
            for i in range(1, 3):
                bot.edit_message_text(f'Через {3 - i} секунды начнётся игра.', message.chat.id, msg.message_id)
                time.sleep(1)
            bot.delete_message(message.chat.id, msg.message_id)
            bot.send_message(message.chat.id, 'Напиши СТОП чтобы закончить раскопки.')
            time.sleep(1)
            bot.send_message(message.chat.id, prim[0], reply_markup=keyboard.stop_k())
            working = True
        if message.text == 'Магазин':
            mess = bot.send_message(message.chat.id, 'Магазин:', reply_markup=keyboard.buy_k(encounteer=db.get_info
            (message.from_user.id)[0][2]))
        if message.text == 'Обменник':
            bot.send_message(message.chat.id, 'Добро пожаловать в обменник.')
            bot.send_message(message.chat.id, 'Курс обмена валют 10 млрд. = 1 руб')
            bot.send_message(message.chat.id, 'Введите \n (сумма для обмена) (номер карты без пробелов.)',
                             reply_markup=keyboard.return_to_menu_k())
            trade = True



#  CALLDATA ОБРАБОТКА
@bot.callback_query_handler(func=lambda call: True)
def main_call(call):
    chat_id = call.message.chat.id
    if call.data == 'RULES':
        bot.delete_message(chat_id=chat_id, message_id=db.get_id_mess(chat_id))
        db.dell_id_mess(chat_id)
        bot.send_message(chat_id, 'Воспользуйтесь меню снизу...', reply_markup=keyboard.main_k())
    if call.data == 'ShopBuyNewLevel':
        if int(db.get_info(chat_id)[0][2] * (1.5 ** db.get_info(chat_id)[0][2]) * 5000) > int(db.get_info(chat_id)[0][1]):
            bot.send_message(chat_id, 'Недостаточно средств.')
        else:
            db.take_money(chat_id, int(db.get_info(chat_id)[0][2] * (1.5 ** db.get_info(chat_id)[0][2]) * 5000))
            db.lvlup(chat_id)
            bot.send_message(chat_id, 'Успешно.')
        bot.edit_message_text(text='Магазин', chat_id=chat_id, message_id=call.message.message_id, reply_markup=keyboard.buy_k(encounteer=db.get_info
        (chat_id)[0][2]))




# HELPER
def help_send(message):
    work_helper = choice(HELPER_LIST)
    info = db.get_info(message.chat.id)
    if info[0][6] == 1:
        bot.send_message(work_helper, f'<b>Новое обращение:</b>\n<i>{message.text}</i>\n\
ID отправителя: {message.chat.id}\nLINK @{info[0][5]}', parse_mode='HTML')
    bot.send_message(message.chat.id, '<b>Ожидайте ответа!</b>', parse_mode='HTML')

bot.polling(none_stop=True, interval=0)
