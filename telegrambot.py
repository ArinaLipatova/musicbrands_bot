import telebot
import sqlite3
from telebot import types
import os
import sys

TOKEN = "6433147215:AAGRB3r8phkKPm_QDOjMbW5sT1Y_gzBaOos"
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def handle_start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item_find = types.KeyboardButton("Find")
    item_start = types.KeyboardButton("Start")
    item_stop = types.KeyboardButton("Stop")
    item_restart = types.KeyboardButton("Restart")
    markup.row(item_find, item_start)
    markup.row(item_stop, item_restart)

@bot.message_handler(func=lambda message: True)
def handle_commands(message):
    if message.text.lower() == 'find' or message.text.lower() == '/find':
        bot.send_message(
            message.chat.id,
            "Введите имя для поиска:"
        )
        bot.register_next_step_handler(message, find_by_name)
    elif message.text.lower() == 'start' or message.text.lower() == '/start':
        bot.send_message(
            message.chat.id,
            "Привет! Я бот для поиска и информации о брендах музыкальных инструментов. "
            "Для поиска по имени используйте панель кнопок или введите /find для поиска по типу инструментов /find_type"
        )
    elif message.text.lower() == 'find_type' or message.text.lower() == '/find_type':
        bot.send_message(
            message.chat.id,
            "Введите тип инструмента, например, клавишные: "
        )
        bot.register_next_step_handler(message, find_by_type)
    elif message.text.lower() == 'stop' or message.text.lower() == '/stop':
        bot.send_message(
            message.chat.id,
            "Бот остановлен"
        )
    elif message.text.lower() == 'restart' or message.text.lower() == '/restart':
        bot.send_message(
            message.chat.id,
            "Бот будет перезапущен"
        )
        restart_bot()
    else:
        bot.send_message(
            message.chat.id,
            "Неизвестная команда. Выберите команду с клавиатуры."
        )

def find_by_name(message):
    user_id = message.from_user.id
    name_to_find = message.text

    # Создаем соединение и курсор внутри функции
    conn = sqlite3.connect('telegrambot.db')
    cursor = conn.cursor()

    # Выполняем SQL-запрос для поиска данных по имени
    cursor.execute('SELECT '
                   'name, '
                   'country, '
                   'year, '
                   'type, '
                   'website '
                   'FROM brands WHERE name=?', (name_to_find,))
    result = cursor.fetchone()

    if result:
        name, country, year, type, website = result
        bot.reply_to(message, f"Результат поиска:\n"
                              f"Имя: {name}\n"
                              f"Страна: {country}\n"
                              f"Год основания: {year}\n"
                              f"Тип инструментов: {type}\n"
                              f"Ссылка на официальный сайт: {website}\n")
    else:
        bot.reply_to(message, "Нет данных для указанного имени.")

    # Закрываем соединение после использования
    conn.close()

def find_by_type(message):
    user_id = message.from_user.id
    type_to_find = message.text

    # Создаем соединение и курсор внутри функции
    conn = sqlite3.connect('telegrambot.db')
    cursor = conn.cursor()

    # Выполняем SQL-запрос для поиска данных по типу инструмента
    cursor.execute('SELECT '
                   'name, '
                   'country, '
                   'year, '
                   'type, '
                   'website '
                   'FROM brands WHERE type=?', (type_to_find,))
    results = cursor.fetchall()

    if results:
        response = "Результат поиска:\n"
        for result in results:
            name, country, year, type, website = result
            response += f"Имя: {name}\n" \
                        f"Страна: {country}\n" \
                        f"Год основания: {year}\n" \
                        f"Тип инструментов: {type}\n" \
                        f"Ссылка на официальный сайт: {website}\n\n"
        bot.reply_to(message, response)
    else:
        bot.reply_to(message, "Нет данных для указанного типа инструмента.")

    # Закрываем соединение после использования
    conn.close()

def restart_bot():
    print("Перезапуск бота...")
    python = sys.executable
    os.execl(python, python, *sys.argv)

bot.polling()