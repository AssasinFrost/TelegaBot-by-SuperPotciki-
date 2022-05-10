from telebot import types


def autor_k():
    autor_k = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton('Автор', url='t.me/pulser_coder1')
    btn2 = types.InlineKeyboardButton('Автор', url='t.me/fu3go99')
    autor_k.add(btn1, btn2)
    return autor_k


def rules_k():
    rules_k = types.InlineKeyboardMarkup()
    rules_k.add(types.InlineKeyboardButton('Ознакомлен', callback_data='RULES'))
    return rules_k


def main_k():
    main_k = types.ReplyKeyboardMarkup()
    but1 = types.KeyboardButton('Раскопки')
    but2 = types.KeyboardButton('Магазин')
    but3 = types.KeyboardButton('Информация')
    but4 = types.KeyboardButton('Помощь')
    but5 = types.KeyboardButton('Обменник')
    main_k.add(but1, but2, but3, but4, but5)
    return main_k


def buy_k(encounteer):
    buy_k = types.InlineKeyboardMarkup()
    buy_k.add(types.InlineKeyboardButton(
        f'Купить улучшение X{encounteer + 1} за {int((encounteer * (1.5 ** encounteer)) * 5000)}',
        callback_data='ShopBuyNewLevel'))
    return buy_k

def return_to_menu_k():
    return_to_menu_k = types.ReplyKeyboardMarkup()
    but = types.KeyboardButton('Вернуться в меню.')
    return_to_menu_k.add(but)
    return return_to_menu_k

def stop_k():
    stop_k = types.ReplyKeyboardMarkup()
    but = types.KeyboardButton('СТОП')
    stop_k.add(but)
    return stop_k