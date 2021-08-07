# -*- coding: utf-8 -*-
"""
Created on Sat Jul 31 15:18:36 2021

@author: alexf
"""

import os
import json
import glob
import re

def get_new_file_path(tmp_path, file_name):

    return  os.path.split(glob.glob(f'{tmp_path}/*/{file_name}')[0])[0].replace('\\', '/')

def rename_files(**kwargs):

    with open(kwargs['json_path'], encoding='utf-8') as data_file:
        data = data_file.read().replace('\\', '/').replace(',}', '}').replace(',]', ']')
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

    return kwargs['new_path'], os.path.split(kwargs['new_path'])[1], data['resolution'], glob.glob(f'{kwargs["new_path"]}/*-poster.jpg')[0], data['plot'], data['tagline']

def scrap_movies(**kwargs):
    os.system('../utilities/tinyMediaManager/tinyMediaManager movie -u --scrapeAll --renameAll -e -eT=Movies_to_json -eP="./exports"')
    new_path = get_new_file_path(kwargs['tmp_path'], kwargs['file_name'])
    return rename_files(json_path = './exports/movielist.json', category=kwargs['category'], new_path=new_path)