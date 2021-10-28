# -*- coding: utf-8 -*-
"""
Created on Fri May 28 15:39:00 2021

@author: alexf
"""
import json
import telegram
import time
from datetime import date

class SendMessage():

    def __init__(self, script_path):
        with open(f'{script_path}/configuration/bot_configuration.json') as file:
            token_id_configuration = json.load(file)

        self.chat_id_logs = token_id_configuration['chat_id_logs']

        bot_token_channel = token_id_configuration['bot_token_channel']
        bot_token_logs = token_id_configuration['bot_token_logs']

        self.bot_channel = telegram.Bot(token=bot_token_channel)
        self.bot_logs = telegram.Bot(token=bot_token_logs)
        self.chat_id_channel = token_id_configuration['chat_id_channel']
        self.chat_id_logs = token_id_configuration['chat_id_logs']

    def to_log_bot(self, level, message):

        try:
           current_time = time.strftime("%H:%M:%S", time.localtime())
           today = date.today().strftime("%d-%m-%Y")
           formatted_message = f'{today} {current_time} - {level} - {message}'
           self.bot_logs.send_message(chat_id=self.chat_id_logs, text=formatted_message, timeout=5)
        except Exception as exc:
           self.to_log_bot('ERROR', f'Class: SendMessage, Function: to_log_bot(), Error:{str(exc)}')
           print(str(exc))

    def to_telegram_channel(self, **kwargs):

        try:
            markup = telegram.InlineKeyboardMarkup([[telegram.InlineKeyboardButton(text='IMDB link', url=f'https://www.imdb.com/title/{kwargs["imdb_id"]}')]])

            caption_text = f"*{kwargs['folder_name']}*\n\n*Resolución:* {kwargs['resolution']}\n\n*IMDB Rating:* {kwargs['imdb_rating']}\n\n*Plot:* {kwargs['plot']}\n\n"
            self.bot_channel.send_photo(chat_id=self.chat_id_channel,  photo=open(kwargs['poster_path'], 'rb'), caption=caption_text, parse_mode=telegram.ParseMode.MARKDOWN, timeout=5, reply_markup=markup)

        except Exception as exc:
            self.to_log_bot('ERROR', f'Class: SendMessage, Function: to_telegram_channel(), Error:{str(exc)}')