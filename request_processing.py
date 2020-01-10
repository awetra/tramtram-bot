from datetime import datetime
import json
import random

import pytz

import interface_text
import parsing_trams


def get_message_or_callback_query(request_data):
    try:
        return (request_data['message'], False)
    except KeyError:
        return (request_data, True)



def start(bot, chat_id, user_fname):
    responce_text = f'\U0001F305 Добрый день, {user_fname}! {interface_text.WELCOME}'
    bot.send_message({
        'chat_id': chat_id,
        'text': responce_text
    })


def help(bot, chat_id):
    bot.send_message({
        'chat_id': chat_id,
        'text': interface_text.HELPING
    })


def show_letters_stations(bot, chat_id):
    letters_stations = parsing_trams.get_letters_stations()
    bot.send_message({
        'chat_id': chat_id,
        'text': interface_text.LETTERS_STATIONS,
        'reply_markup': json.dumps({
            'keyboard': [[{'text': letter}] for letter in letters_stations],
            'resize_keyboard': True,
            'one_time_keyboard': True
        })
    })


def show_stations(bot, chat_id, name_station, message_id=None, edit_message=False):
    stations = parsing_trams.get_page_stations(name_station.strip().lower())
    if not stations:
        # Если не нашлось станций по указанной станции
        bot.send_message({
            'chat_id': chat_id,
            'text': '\U0001F3C7 ' + random.choice(interface_text.NO_STATIONS)
        })
    elif len(stations) == 1:
        # Если нашлась одна станция, то пользователь ввёл полное её название
        station = stations.popitem()
        name_station, href_station = station[0], station[1]['href']
        trams_traffic = parsing_trams.get_traffic_station(href_station)
        responce_text = f'\U0001F69C ост. <b>{name_station}</b>\n\n'

        if not trams_traffic:
            # Если данных о времени трамваев нет
            responce_data = {
                'chat_id': chat_id,
                'text': responce_text + interface_text.NO_TRAMS
            }

            if not edit_message:
                bot.send_message(responce_data)
            else:
                responce_data['message_id'] = message_id
                bot.edit_message_text(responce_data)
        else:
            time_now = datetime.now(tz=pytz.timezone('Asia/Yekaterinburg')).strftime('%H:%M')
            responce_text += f'{interface_text.DRIVE_UP_TRAMS} <b>{time_now}</b>:\n\n'
            for tram, time in trams_traffic.items():
                responce_text += f'{tram} - {time}\n'
            
            responce_data = {
                'chat_id': chat_id,
                'text': responce_text,
                'reply_markup': json.dumps({
                    'inline_keyboard': [[{'text': 'Обновить', 'callback_data': 'update_station'}]],
                })
            }

            if not edit_message:
                bot.send_message(responce_data)
            else:
                responce_data['message_id'] = message_id
                bot.edit_message_text(responce_data)
    else:
        # Если нашлось больше одной станции, то выводятся эти станции
        bot.send_message({
            'chat_id': chat_id,
            'text': interface_text.CHOICE_STATION,
            'reply_markup': json.dumps({
                'keyboard': [[{'text': station}] for station in stations],
                'resize_keyboard': True,
                'one_time_keyboard': True
            })
        })