import telebot
from config import *
from logic import *

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def handle_start(message):
    bot.send_message(message.chat.id, "Привет! Я бот, который может показывать города на карте. Напиши /help для списка команд.")
@bot.message_handler(commands=['help'])
def handle_help(message):
    bot.send_message(message.chat.id, "Доступные команды:/start, /help, /show_city [city], /remember_city [city], /show_my_cities, /marker_color [color], /marker_point [point]")
@bot.message_handler(commands=['marker_color'])
def marker_color(message):
    username = message.from_user.username
    color = message.text.split()[-1]
    manager.add_color_marker(username, color)
    bot.send_message(message.chat.id, "Маркер успешно добавлен!")
@bot.message_handler(commands=['marker_point'])
def marker_point(message):
    username = message.from_user.username
    point = message.text.split()[-1]
    manager.add_point_marker(username, point)
    bot.send_message(message.chat.id, "Маркер успешно добавлен!")
@bot.message_handler(commands=['show_city'])
def handle_show_city(message):
    city_name = message.text.split()[-1]
    filename = f"{message.chat.id}.jpg"
    user = message.from_user.username
    manager.create_grapf(filename, [city_name], user)
    file = open(filename, "rb")
    bot.send_photo(message.chat.id, photo=file)
@bot.message_handler(commands=['remember_city'])
def handle_remember_city(message):
    username = message.from_user.username
    city_name = message.text.split()[-1]
    
    if manager.add_city(username, city_name):
        bot.send_message(message.chat.id, f'Город {city_name} успешно сохранен!')
    else:
        bot.send_message(message.chat.id, 'Такого города я не знаю. Убедись, что он написан на английском!')

@bot.message_handler(commands=['show_my_cities'])
def handle_show_visited_cities(message):
    cities = manager.select_cities(message.chat.id)
    bot.send_message(message.chat.id, f"Ваши города - {cities}")

if __name__=="__main__":
    manager = DB_Map(DB)
    bot.polling(print("Bot started."), none_stop=True)
