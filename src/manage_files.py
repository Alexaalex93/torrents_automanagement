# -*- coding: utf-8 -*-
"""
Created on Thu Jul 29 10:12:38 2021

@author: alexf
"""

import os
from send_message import SendMessage
import sys

def upload_to_backup_drive(rclone_path, script_path, source_path, remote_name, remote_folder, category, original_file_name):

    send_message = SendMessage(script_path)
    try:
        send_message.to_log_bot('INFO', f'Iniciando subida a team backup [{original_file_name}]')

        if os.path.isdir(source_path):
            rclone_sintax = f'{rclone_path} copy \"{source_path}\" --ignore-existing \"{remote_name}:{remote_folder}/{category}/{original_file_name}\"'
        else:
            rclone_sintax = f'{rclone_path} copy \"{source_path}\" --ignore-existing \"{remote_name}:{remote_folder}/{category}\"'

        os.system(rclone_sintax)

        send_message.to_log_bot('INFO', f'Archivo subido a team backup [{original_file_name}]')

    except Exception as exc:
        print('ERROR', f'Error con archivo [{original_file_name}] en funcion upload_to_backup_drive(), Error: {str(exc)}')
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno)

        send_message.to_log_bot('ERROR', f'Error con archivo [{original_file_name}] en funcion upload_to_backup_drive(), Error: {str(exc)}')
        send_message.to_log_bot('ERROR', f'{exc_type}, {fname}, {exc_tb.tb_lineno}')

def upload_to_drive(**kwargs):

    send_message = SendMessage(kwargs['script_path'])
    try:

        send_message.to_log_bot('INFO', f'Iniciando subida a team definitivo [{kwargs["original_file_name"]}]')

        os.system(f'{kwargs["rclone_path"]} copy \"{kwargs["tmp_path"]}\" --ignore-existing \"{kwargs["remote_name"]}:{kwargs["remote_folder"]}/{kwargs["folder_name"]}\"')

        send_message.to_log_bot('INFO', f'Archivo subido a team definitivo [{kwargs["original_file_name"]}]')
    except Exception as exc:
        print('ERROR', f'Error con archivo [{kwargs["original_file_name"]}] en funcion upload_to_drive(), Error: {str(exc)}')
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno)

        send_message.to_log_bot('ERROR', f'Error con archivo [{kwargs["original_file_name"]}] en funcion upload_to_drive(), Error: {str(exc)}')
        send_message.to_log_bot('ERROR', f'{exc_type}, {fname}, {exc_tb.tb_lineno}')