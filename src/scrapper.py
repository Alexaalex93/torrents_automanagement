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

def rename_movies(**kwargs):

    try:
        with open(kwargs['json_path'], encoding='utf-8') as data_file:

            data = data_file.read().replace('\\\\', '/').replace('\/', '/').replace('//', '/').replace(',}', '}').replace(',]', ']')
            data = json.loads(data)

        folder_name = f'{data["title"]} ({data["year"]})'.replace('?', '').replace(':', '')

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

        for file in glob.glob(f'{kwargs["tmp_path"]}/*/*'):

            path, name = os.path.split(file)

            extension = os.path.splitext(file)[1]
            new_name = f'{path}/{folder_name} [{data["resolution"]} {kwargs["source_tag"]} {video_codec} {data["audio_metadata"][0]["codec"].replace("/", "-")}] [{data["video_bitrate"]}] [{dual_audios_subs}] {{tmdb-{data["tmdb_id"]}}}'
            if extension == '.jpg':
                new_name += re.search(r'-(poster|fanart|banner|clearart|thumb|landscape|logo|clearlogo|disc|discart|keyart)\.jpg', file).group(0)
            else:
                new_name += extension
            os.rename(file, new_name)
        os.rename(path, f'{path} {{tmdb-{data["tmdb_id"]}}}')

        poster_path = glob.glob(f'{kwargs["tmp_path"]}/*/*poster*')[0] if glob.glob(f'{kwargs["tmp_path"]}/*/*poster*') else None

        return data['resolution'], poster_path, data['plot'], data['imdb_rating'], data['imdb_id']

    except Exception as exc:

        send_message = SendMessage(kwargs['script_path'])
        send_message.to_log_bot('ERROR', f'Error con archivo [{kwargs["original_file_name"]}] en funcion rename_movies(), Error: {str(exc)}')


def get_series_information(**kwargs):

    try:
        with open(kwargs['json_path'], encoding='utf-8') as data_file:
            data = data_file.read().replace('\\\\', '/').replace('\/', '/').replace('//', '/').replace(',}', '}').replace(',]', ']')
            data = json.loads(data)

        poster_path = glob.glob(f'{kwargs["tmp_path"]}/*/*poster*')[0] if glob.glob(f'{kwargs["tmp_path"]}/*/*poster*') else None

        return data['resolution'], poster_path, data['plot'], data['imdb_rating'], data['imdb_id']

    except Exception as exc:

        send_message = SendMessage(kwargs['script_path'])
        send_message.to_log_bot('ERROR', f'Error con archivo [{kwargs["original_file_name"]}] en funcion get_series_information(), Error: {str(exc)}')

def scrap(**kwargs):

    exports_folder = f'/downloads/exports/{kwargs["hash_folder"]}'

    if not os.path.isdir('/downloads/exports/'):
        os.mkdir('/downloads/exports/')

    if os.path.isdir(exports_folder):
        shutil.rmtree(exports_folder)
    os.mkdir(exports_folder)

    if 'series' in kwargs['category']:
        docker_folder = 'tvshows'
        tmm_command = 'tvshow'
    else:
        docker_folder = 'movies'
        tmm_command = 'movie'
    export_script = f'{docker_folder}_to_json'

    print(f'docker run --rm -e LANG=C.UTF-8 -e LC_ALL=C.UTF-8 --name="{kwargs["hash_folder"]}" -v "{kwargs["global_path"]}/{kwargs["tmp_path"]}:/{docker_folder}" -v "{kwargs["global_path"]}/downloads/exports/{kwargs["hash_folder"]}:/exports" {kwargs["docker_tmm_image"]} /tmm/tinyMediaManager/tinyMediaManager {tmm_command} -u --scrapeAll --renameAll -e -eT={export_script} -eP=/exports')
    os.system(f'docker run --rm -e LANG=C.UTF-8 -e LC_ALL=C.UTF-8 --name="{kwargs["hash_folder"]}" -v "{kwargs["global_path"]}/{kwargs["tmp_path"]}:/{docker_folder}" -v "{kwargs["global_path"]}/downloads/exports/{kwargs["hash_folder"]}:/exports" {kwargs["docker_tmm_image"]} /tmm/tinyMediaManager/tinyMediaManager {tmm_command} -u --scrapeAll --renameAll -e -eT={export_script} -eP=/exports')

    if 'series' in kwargs['category']:
        resolution, poster_path, plot, imdb_rating, imdb_id = get_series_information(json_path = f'{exports_folder}/tvshows.json', tmp_path=kwargs['tmp_path'], script_path=kwargs['script_path'], original_file_name=kwargs['original_file_name'])
    else:
        resolution, poster_path, plot, imdb_rating, imdb_id = rename_movies(json_path = f'{exports_folder}/movielist.json', tmp_path=kwargs['tmp_path'], source_tag=kwargs['source_tag'], script_path=kwargs['script_path'], original_file_name=kwargs['original_file_name'])

    shutil.rmtree(exports_folder)

    return resolution, poster_path, plot, imdb_rating, imdb_id