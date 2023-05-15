# -*- coding: utf-8 -*-
"""
Created on Mon May  1 10:50:13 2023

@author: alexf
"""
import logging

from .send_message import SendMessage

class TelegramLogHandler(logging.Handler):

    def __init__(self, bot_configuration_path, templates_path, unique_id, level=logging.NOTSET):
        super().__init__(level)
        self.send_message = SendMessage(bot_configuration_path, templates_path)
        self.unique_id = unique_id

    def emit(self, record):
        try:

            log_entry = self.format(record)
            self.send_message.send('log_message_template', log_msg=log_entry, level=record.levelname, unique_id=self.unique_id)

        except Exception:
            self.handleError(record)
