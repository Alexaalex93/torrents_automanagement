# -*- coding: utf-8 -*-
"""
Created on Thu Jul 29 13:01:27 2021

@author: alexf
"""

import os
import shutil
from send_message import SendMessage

def check_extension(**kwargs):
    send_message = SendMessage()

    source_path = kwargs["source_path"]
    tmp_path = '/'.join(source_path.split('/')[:-2])+ '/scrap'
    if not os.path.isdir(tmp_path):
        os.makedirs(tmp_path)

    if not os.path.splitext(source_path)[1] == '.mkv' and not os.path.splitext(source_path)[1] == '.iso':
        if 'BDMV' in os.listdir(source_path):
            #print(os.path.split(kwargs["source_path"])[1])
            name = os.path.split(source_path)[1]
            final_name = name.replace(' ', '_').replace('(', '').replace(')','').replace('[','').replace(']','')

            os.system(f'genisoimage -udf -allow-limited-size -input-charset "utf-8" -v -J -r -V {final_name} -o "{tmp_path}/{final_name}.iso" "{kwargs["source_path"]}"')
            send_message.to_log_bot('INFO', 'FullBluray convertido a iso')

            file_name = final_name
    else:
        file_name = os.path.split(source_path)[1]
        shutil.copy(source_path, f'{tmp_path}/{file_name}')
    send_message.to_log_bot('INFO', 'Archivo movido a carpeta temporal')

    return tmp_path, file_name