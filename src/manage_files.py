# -*- coding: utf-8 -*-
"""
Created on Thu Jul 29 10:12:38 2021

@author: alexf
"""

import os
from send_message import SendMessage

def upload_to_backup_drive(rclone_path, source_path, remote_name, remote_folder, category, file):
    send_message = SendMessage()
    try:
        send_message.to_log_bot('INFO', f'Iniciando subida a team backup [{file}]')
        os.system(f'{rclone_path} copy \"{source_path}\" --ignore-existing \"{remote_name}:{remote_folder}/{category}\"')
        send_message.to_log_bot('INFO', f'Archivo subido a team backup [{file}]')

    except Exception as exc:
        send_message.to_log_bot('ERROR', f'Error con archivo [{file}] en funcion upload_to_backup_drive(), Error: {str(exc)}')


def upload_to_drive(**kwargs):
    send_message = SendMessage()
    try:
        send_message.to_log_bot('INFO', f'Iniciando subida a team definitivo [{kwargs["file"]}]')
        os.system(f'{kwargs["rclone_path"]} copy \"{kwargs["tmp_path"]}\" \"{kwargs["remote_name"]}:{kwargs["remote_folder"]}/{kwargs["folder_name"]}\"')
        send_message.to_log_bot('INFO', f'Archivo subido a team definitivo [{kwargs["file"]}]')
    except Exception as exc:
        send_message.to_log_bot('ERROR', f'Error con archivo [{kwargs["file"]}] en funcion upload_to_drive(), Error: {str(exc)}')