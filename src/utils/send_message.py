# -*- coding: utf-8 -*-
"""
Created on Fri May 28 15:39:00 2021

@author: alexf
"""
import json
import os
import requests

class SendMessage():

    def __init__(self, bot_configuration_path, templates_path):

        with open(bot_configuration_path) as file:
            token_id_configuration = json.load(file)

        self.chat_id_logs = token_id_configuration['chat_id_logs']
        self.chat_id_channel = token_id_configuration['chat_id_channel']

        self.bot_token_channel = token_id_configuration['bot_token_channel']
        self.bot_token_logs = token_id_configuration['bot_token_logs']

        self.templates_path = templates_path
        self.templates = {}


    def load_template(self, template_name):

        template_file = f'{self.templates_path}/{template_name}.txt'
        if os.path.exists(template_file):
            with open(template_file, 'r') as file:
                self.templates[template_name] = file.read()
        else:
            raise ValueError(f"Template '{template_name}' not found.")


    def get_template(self, template_name):

        if template_name not in self.templates:
            self.load_template(template_name)
        return self.templates[template_name]



    def get_chat_id(self, template_name):

        if 'log' in template_name.lower():
            return self.chat_id_logs
        elif 'channel' in template_name.lower():
            return self.chat_id_channel
        else:
            raise ValueError("Unable to determine chat_id from the template name.")



    def send(self, template_name, photo=None, **kwargs):

        level = None
        if kwargs.get('level'):
           level = kwargs.get('level')
        template = self.get_template(template_name).format(**kwargs)
        chat_id = self.get_chat_id(template_name)
        parse_mode = 'Markdown' if template_name != 'log_message_template' else None

        if photo:
            self.send_photo(chat_id=chat_id, photo=photo, caption=template, parse_mode=parse_mode, level=level)
        else:
            self.send_text(chat_id=chat_id, text=template, parse_mode=parse_mode, level=level)

    def send_text(self, chat_id, text, parse_mode, level):

        bot_token = self.bot_token_channel if chat_id == self.chat_id_channel else self.bot_token_logs
        url = f'https://api.telegram.org/bot{bot_token}/sendMessage'
        payload = {'chat_id': chat_id, 'text': text, 'parse_mode': parse_mode}
        response = requests.post(url, data=payload)
        return response.json()


    def send_photo(self, chat_id, photo, caption, parse_mode, level):

        bot_token = self.bot_token_channel if chat_id == self.chat_id_channel else self.bot_token_logs
        url = f'https://api.telegram.org/bot{bot_token}/sendPhoto'
        payload = {'chat_id': chat_id, 'caption': caption, 'parse_mode': parse_mode}
        with open(photo, 'rb') as file:
            files = {'photo': file}
            response = requests.post(url, data=payload, files=files)
        return response.json()
