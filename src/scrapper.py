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

def rename_files(**kwargs):

    try:
        with open(kwargs['json_path'], encoding='utf-8') as data_file:
            data = data_file.read().replace('\\\\', '/').replace('\/', '/').replace('//', '/').replace(',}', '}').replace(',]', ']')
            data_content = json.loads(data)
        movie_path = glob.glob(f'{kwargs["tmp_path"]}/*')[0]
        data = data_content[movie_path]
        folder_name = data['next_title'].replace('?', '').replace(':', '')

        for file in glob.glob(f'{movie_path}/*'):
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
            new_name = f'{path}//{folder_name} [{data["resolution"]} {kwargs["category"]} {video_codec} {data["audio_metadata"][0]["codec"]}] [{data["video_bitrate"]}] [{dual_audios_subs}] [ID {data["tmdb_id"]}]'
            if extension == '.jpg':
                new_name += re.search(r'-(poster|fanart|banner|clearart|thumb|landscape|logo|clearlogo|disc|discart|keyart)\.jpg', file).group(0)
            else:
                new_name += extension
            os.rename(file, new_name)
        return folder_name, data['resolution'], glob.glob(f'{kwargs["tmp_path"]}/{folder_name}/*-poster.jpg')[0], data['plot'], data['imdb_rating'], data['imdb_id']

    except Exception as exc:

        send_message = SendMessage(kwargs['script_path'])
        send_message.to_log_bot('ERROR', f'Error con archivo [{kwargs["file"]}] en funcion rename_files(), Error: {str(exc)}')


def scrap_movies(**kwargs):

    with open(f"{kwargs['script_path']}/utilities/tinyMediaManager/data/movies.json", 'r') as jsonFile:
        data_config = json.load(jsonFile)

    with open(f"{kwargs['script_path']}/utilities/tinyMediaManager/data/movies.json", 'w') as jsonFile:
       data_config['movieDataSource'].append(f'{kwargs["tmp_path"]}')
       json.dump(data_config, jsonFile, indent=4)

    exports_folder = f'{kwargs["script_path"]}/utilities/tinyMediaManager/{kwargs["hash_folder"]}}}'
    os.mkdir(exports_folder)

    os.system(f'{kwargs["script_path"]}/utilities/tinyMediaManager/tinyMediaManager movie -u --scrapeAll --renameAll -e -eT=movies_to_json -eP=\"{exports_folder}\"')

    folder_name, resolution, poster_path, plot, imdb_rating, imdb_id = rename_files(json_path = f'{exports_folder}/movielist.json', tmp_path=kwargs['tmp_path'], script_path=kwargs['script_path'], category=kwargs['category'], file=kwargs['file'])

    shutil.rmtree(exports_folder)

    with open(f"{kwargs['script_path']}/utilities/tinyMediaManager/data/movies.json", 'r') as jsonFile:
        data_config = json.load(jsonFile)

    with open(f"{kwargs['script_path']}/utilities/tinyMediaManager/data/movies.json", 'w') as jsonFile:
        data_config['movieDataSource'].remove(kwargs["tmp_path"])
        json.dump(data_config, jsonFile, indent=4)
    return folder_name, resolution, poster_path, plot, imdb_rating, imdb_id


def scrap_series(**kwargs):

    with open(f"{kwargs['script_path']}/utilities/tinyMediaManager/data/tvShows.json", 'r') as jsonFile:
        data_config = json.load(jsonFile)

    with open(f"{kwargs['script_path']}/utilities/tinyMediaManager/data/tvShows.json", 'w') as jsonFile:
        data_config['tvShowDataSource'].append(kwargs["tmp_path"])
        json.dump(data_config, jsonFile, indent=4)

    exports_folder = f'{kwargs["script_path"]}/utilities/tinyMediaManager/{kwargs["hash_folder"]}'

    os.mkdir(exports_folder)
    os.system(f'{kwargs["script_path"]}/utilities/tinyMediaManager/tinyMediaManager tvshow -u --scrapeAll --renameAll -e -eT=tvshows_to_json -eP=\"{exports_folder}\"')


    with open(f'{exports_folder}/tvshows.json', encoding='utf-8') as data_file:
        data = data_file.read().replace('\\\\', '/').replace('\/', '/').replace('//', '/').replace(',}', '}').replace(',]', ']')
        data_content = json.loads(data)

    data_json = data_content[glob.glob(f'{kwargs["tmp_path"]}/*')[0]]

    series_name = data_json['next_title'].replace('?', '').replace(':', '')

    shutil.rmtree(exports_folder)


    with open(f"{kwargs['script_path']}/utilities/tinyMediaManager/data/tvShows.json", 'r') as jsonFile:
        data_config = json.load(jsonFile)

    with open(f"{kwargs['script_path']}/utilities/tinyMediaManager/data/tvShows.json", 'w') as jsonFile:
        data_config['tvShowDataSource'].remove(kwargs["tmp_path"])
        json.dump(data_config, jsonFile, indent=4)


    return series_name, data_json['resolution'], glob.glob(f'{kwargs["tmp_path"]}/{series_name}/poster.jpg')[0], data_json['plot'], data_json['imdb_rating'], data_json['imdb_id']