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
    send_message = SendMessage(kwargs['script_path'])

    try:
        source_path = kwargs["source_path"]

        if not os.path.splitext(source_path)[1] == '.mkv' and not os.path.splitext(source_path)[1] == '.iso' and 'BDMV' in os.listdir(source_path): #Si no es un archivo iso o mkv y que haya la carmeta BDMV en las subcarpetas
            #Implementar correctamente
            name = os.path.split(source_path)[1]
            final_name = name.replace(' ', '_').replace('(', '').replace(')','').replace('[','').replace(']','')

            send_message.to_log_bot('INFO', 'Iniciando conversion a iso')
            os.system(f'genisoimage -udf -allow-limited-size -input-charset "utf-8" -v -J -r -V {final_name} -o "{kwargs["tmp_path"]}/{final_name}.iso" "{kwargs["source_path"]}"')

            send_message.to_log_bot('INFO', 'FullBluray convertido a iso')

            os.rename(re.sub('(?i)hdo', '', re.sub('\[.*\]', '',f'{kwargs["tmp_path"]}/{final_name}', f'{kwargs["tmp_path"]}/{final_name}')).replace('-', '_').replace(' ', '_').replace('+', '').replace('_.', '.').replace('...', ''))
            file_name = final_name.replace('-', '_').replace(' ', '_').replace('+', '').replace('.', '')
            file_name = re.sub('(?i)hdo', '', re.sub('\[.*\]', '', file_name)).replace('_.', '.').replace('...', '')


        else:

            if os.path.isdir(source_path): #Si es temporada completa
                send_message.to_log_bot('INFO', f'Moviendo carpeta a carpeta temporal [{kwargs["file"]}]')

                new_folder_name = re.sub(r'(?i)((?!(\(\d+\)))\(miniserie(.+?)?\)|\[(.+?)]|hdo|\_\.|\.\.\.|\+|iso|s\d+(e\d+)?)', '', os.path.split(source_path)[1])

                shutil.copytree(source_path, f'{kwargs["tmp_path"]}/{new_folder_name}')
            else:

                send_message.to_log_bot('INFO', f'Moviendo archivo a carpeta temporal [{kwargs["file"]}]')

                path, file = os.path.split(source_path)
                file = re.sub(r'\-', '_', re.sub(r'(?i)((?!(\(\d+\)))\(miniserie(.+?)?\)|\[(.+?)]|hdo|\_\.|\.\.\.|\+|iso', '', file))

                shutil.copy(source_path, f'{kwargs["tmp_path"]}/{file}')

        send_message.to_log_bot('INFO', f'Archivo movido a carpeta temporal [{kwargs["file"]}]')
    except Exception as exc:
        send_message.to_log_bot('ERROR', f'Error con archivo [{kwargs["file"]}] en funcion check_extension(), Error: {str(exc)}')
    return file_name

#python3 /scripts/torrents_automanagement/src/main.py -p "/downloads/series_fhd_webdl/Atracadores (2021) S01 [PACK][NF WEB-DL 1080p AVC ES-EN DD+ 5.1 Subs][HDO]"  -c "series_fhd_webdl"