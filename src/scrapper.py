# -*- coding: utf-8 -*-
"""
Created on Sat Jul 31 15:18:36 2021

@author: alexf
"""

import os
import json
import glob
import re
import shutil

from send_message import SendMessage

def get_new_file_path(tmp_path, file_name, file):
    try:
        new_file_path = os.path.split(glob.glob(f'{tmp_path}/*/{file_name}')[0])[0].replace('\\', '/')
    except Exception as exc:
        send_message = SendMessage()
        send_message.to_log_bot('ERROR', f'Error con archivo [{file}] en funcion get_new_file_path(), Error: {str(exc)}')
    return new_file_path

def rename_files(**kwargs):
    try:
        with open(kwargs['json_path'], encoding='utf-8') as data_file:
            data = data_file.read().replace('\\\\', '/').replace('\/', '/').replace('//', '/').replace(',}', '}').replace(',]', ']')
            data_content = json.loads(data)
        data = data_content[kwargs['new_path']]
        for file in glob.glob(f'{kwargs["new_path"]}/*'):
            path, name = os.path.split(file)
            video_codec = data['video_codec'].replace('h', 'x')
            dual_audios_subs = ''
            spanish_lan = False
            english_lan = False
            for audios in data['audio_metadata']:
                if audios['language'] == 'eng':
                    english_lan = True
                if audios['language'] == 'spa':
                    spanish_lan = True
            if english_lan and spanish_lan:
                dual_audios_subs = 'Dual + '
            if data['subtitles']:
                dual_audios_subs+='Subs'
            extension = os.path.splitext(file)[1]
            new_name = f'{path}//{data["title"].replace(":", "")} ({data["year"]}) [{data["resolution"]} {kwargs["category"]} {video_codec} {data["audio_metadata"][0]["codec"]}] [{data["video_bitrate"]}] [{dual_audios_subs}] [ID {data["tmdb_rating"]}]'
            if extension == '.jpg':
                new_name += re.search(r'-(poster|fanart|banner|clearart|thumb|landscape|logo|clearlogo|disc|discart|keyart)\.jpg', file).group(0)
            else:
                new_name += extension
            os.rename(file, new_name)
        return kwargs['new_path'], os.path.split(kwargs['new_path'])[1], data['resolution'], glob.glob(f'{kwargs["new_path"]}/*-poster.jpg')[0], data['plot'], data['tagline'], data['imdb_rating']

    except Exception as exc:
        send_message = SendMessage()
        send_message.to_log_bot('ERROR', f'Error con archivo [{kwargs["file"]}] en funcion rename_files(), Error: {str(exc)}')
        

def scrap_movies(**kwargs):
    exports_folder = f'{kwargs["script_path"]}/utilities/tinyMediaManager/exports_{kwargs["file_name"].replace(" ", "_")}'
    os.system(f'{kwargs["script_path"]}/utilities/tinyMediaManager/tinyMediaManager movie -u --scrapeAll --renameAll -e -eT=movies_to_json -eP=\"{exports_folder}\"')
    new_path = get_new_file_path(kwargs['tmp_path'], kwargs['file_name'], kwargs['file'])#Cambiar por path relativo
    return rename_files(json_path = f'{exports_folder}/movielist.json', category=kwargs['category'], new_path=new_path, file=kwargs['file'])

#, folder_name, resolution, poster_path, plot, imdb_rating, imbd_id
def get_series_folder(**kwargs):
    try:
        #kwargs = {'json_path':"C:/Users/AlexPC/Downloads/tvshows (4).json"}
        #"C:/Users/AlexPC/Downloads/tvshows.json"
        with open(kwargs['json_path'], encoding='utf-8') as data_file:
            data = data_file.read().replace('\\\\', '/').replace('\/', '/').replace('//', '/').replace(',}', '}').replace(',]', ']')
            data_content = json.loads(data)
        data = data_content[kwargs['tmp_file_path']]

        return data['next_title'], data['resolution'], data['plot'], data['imdb_rating'], data['imdb_id']

    except Exception as exc:
        send_message = SendMessage()
        send_message.to_log_bot('ERROR', f'Error con archivo [{kwargs["file"]}] en funcion get_series_folder(), Error: {str(exc)}')
        
def scrap_series(**kwargs):
    #kwargs = {'file_name':'Atracadores (2021) S01 [PACK][NF WEB-DL 1080p AVC ES-EN DD+ 5.1 Subs][HDO]'}
    exports_folder = f'{kwargs["script_path"]}/utilities/tinyMediaManager/exports_{kwargs["file_name"].replace(" ", "_")}'
    #os.mkdir(exports_folder)
    os.system(f'{kwargs["script_path"]}/utilities/tinyMediaManager/tinyMediaManager tvshow -u --scrapeAll -e -eT=tvshows_to_json -eP=\"{exports_folder}\"')
    print(f'{exports_folder}/tvshows.json')
    print(f'{kwargs["tmp_path"]}/{kwargs["file_name"]}')
    print(kwargs['file'])
    folder_name, resolution, plot, imdb_rating, imdb_id = get_series_folder(json_path=f'{exports_folder}/tvshows.json', tmp_file_path=f'{kwargs["tmp_path"]}/{kwargs["file_name"]}', file=kwargs['file'])
    os.system(f'{kwargs["script_path"]}/utilities/tinyMediaManager/tinyMediaManager tvshow --renameAll')
    shutil.rmtree(exports_folder)
    #print(glob.glob(f'{kwargs["tmp_path"]}/{folder_name}/*-poster.jpg'))
    print(f'{kwargs["tmp_path"]}/{folder_name}/*poster.jpg')
    return f'{kwargs["tmp_path"]}/{folder_name}', folder_name, resolution, glob.glob(f'{kwargs["tmp_path"]}/{folder_name}/*poster.jpg')[0], plot, imdb_rating, imdb_id
    
