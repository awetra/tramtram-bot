from flask import Flask, request

from telegram_bot import TelegramBot
from config import TOKEN
import request_processing


app = Flask(__name__)

bot = TelegramBot(TOKEN)
bot.set_webhook('https://tramtram-bot.herokuapp.com')


@app.route('/', methods=['POST'])
def index():
    if request.method == 'POST':
        data, is_callback_query = request_processing.get_message_or_callback_query(request.json)

        if is_callback_query:
            chat_id = data['callback_query']['message']['chat']['id']
            callback_data = data['callback_query']['data']
            message_id = data['callback_query']['message']['message_id']
            # Парсинг названия остановки
            name_station = data['callback_query']['message']['text'].split('\n')[0][7:]

            if callback_data == 'update_station':
                # Обновление сообщения о времени трамваев для определённой станции
                request_processing.show_stations(bot, chat_id, name_station, message_id, edit_message=True)
        else:
            chat_id, message_text = data['chat']['id'], data['text'] 
            
            if message_text == '/start':
                # Приветствие пользователя
                request_processing.start(bot, chat_id, user_fname=data['from']['first_name'])
            elif message_text == '/help':
                # Указание, как пользоваться ботом
                request_processing.help(bot, chat_id)
            elif message_text == '/stations':
                # Вывод букв/цифр, с которых начинаются остановки
                request_processing.show_letters_stations(bot, chat_id)
            else:
                # Вывод конкретн-ых/ой останов-ок/ки по запросу пользователя
                request_processing.show_stations(bot, chat_id, name_station=message_text)

    return 'Telegram - @ekb_transport_bot'


if __name__ == '__main__':
    app.run(debug=True)


