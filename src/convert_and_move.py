# -*- coding: utf-8 -*-
"""
Created on Thu Jul 29 13:01:27 2021

@author: alexf
"""

import os
import shutil
from send_message import SendMessage
import re 

def check_extension(**kwargs):
    send_message = SendMessage()

    try:
        source_path = kwargs["source_path"]
        scrap_folder = '/scrap_movies' if not kwargs['series'] else '/scrap_series'
        tmp_path = '/'.join(source_path.split('/')[:-2]) + scrap_folder
        if not os.path.isdir(tmp_path):
            os.makedirs(tmp_path)
    
        if not os.path.splitext(source_path)[1] == '.mkv' and not os.path.splitext(source_path)[1] == '.iso': #Si no es un archivo iso o mkv
            if 'BDMV' in os.listdir(source_path): #Si tenemos la carpeta BDMV en las subcarpetas
                name = os.path.split(source_path)[1]
                final_name = name.replace(' ', '_').replace('(', '').replace(')','').replace('[','').replace(']','')
                
                send_message.to_log_bot('INFO', 'Iniciando conversion a iso')
                os.system(f'genisoimage -udf -allow-limited-size -input-charset "utf-8" -v -J -r -V {final_name} -o "{tmp_path}/{final_name}.iso" "{kwargs["source_path"]}"')
                send_message.to_log_bot('INFO', 'FullBluray convertido a iso')
    
                os.rename(re.sub('(?i)hdo', '', re.sub('\[.*\]', '',f'{tmp_path}/{final_name}', f'{tmp_path}/{final_name}')).replace('-', '_').replace(' ', '_').replace('+', '').replace('_.', '.'))
                file_name = final_name.replace('-', '_').replace(' ', '_').replace('+', '').replace('.', '')
                file_name = re.sub('(?i)hdo', '', re.sub('\[.*\]', '', file_name)).replace('_.', '.')
            else: #Si no tenemos la carpeta BDMV en las subcarpetas, pueden ser series
                shutil.copytree(source_path, f'{tmp_path}/{os.path.split(source_path)[1]}')
                file_name = os.path.split(source_path)[1]
        else:   
            send_message.to_log_bot('INFO', f'Moviendo archivo a carpeta temporal [{kwargs["file"]}]')
            file_name = os.path.split(source_path)[1].replace('-', '_').replace(' ', '_').replace('+', '')
            file_name = re.sub('(?i)hdo', '', re.sub('\[.*\]', '', file_name)).replace('_.', '.')
            shutil.copy(source_path, f'{tmp_path}/{file_name}')
        send_message.to_log_bot('INFO', f'Archivo movido a carpeta temporal [{kwargs["file"]}]')
    except Exception as exc:
        send_message.to_log_bot('ERROR', f'Error con archivo [{kwargs["file"]}] en funcion check_extension(), Error: {str(exc)}')
    return tmp_path, file_name

#python3 /scripts/torrents_automanagement/src/main.py -p "/downloads/series_fhd_webdl/Atracadores (2021) S01 [PACK][NF WEB-DL 1080p AVC ES-EN DD+ 5.1 Subs][HDO]"  -c "series_fhd_webdl"