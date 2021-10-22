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
import time

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

def modify_movies_json(movies_json_path, tmp_path):

    with open(movies_json_path, 'r') as jsonFile:
        data_config = json.load(jsonFile)

    with open(movies_json_path, 'w') as jsonFile:
       data_config['movieDataSource'].append(tmp_path)

       data_config['nfoFilenames'] = [ "FILENAME_NFO" ]
       data_config['posterFilenames'] = [ "FILENAME_POSTER" ]
       data_config['fanartFilenames'] = [ "FILENAME_FANART" ]
       data_config['extraFanartFilenames'] = [ "FILENAME_EXTRAFANART" ]
       data_config['bannerFilenames'] = [ "FILENAME_BANNER" ]
       data_config['clearartFilenames'] = [ "FILENAME_CLEARART" ]
       data_config['thumbFilenames'] = [ "FILENAME_LANDSCAPE" ]
       data_config['logoFilenames'] = [ "FILENAME_LOGO" ]
       data_config['keyartFilenames'] = [ "FILENAME_KEYART" ]
       data_config['artworkScrapers'] = [ "tmdb", "mpdbtv", "imdb", "fanarttv", "ffmpeg" ]
       data_config['writeCleanNfo'] = True
       data_config['nfoLanguage'] = 'es'
       data_config['renamerPathname'] = '${title} ${- ,edition,} (${year})'
       data_config['renamerFilename'] = ''
       data_config['movieScraper'] = 'tmdb'
       data_config['scraperLanguage'] = 'es'
       data_config['certificationCountry'] = 'ES'
       data_config['releaseDateCountry'] = 'ES'
       data_config['ratingSources'] = 'imdb'
       data_config['scraperMetadataConfig'] = [ "ID", "TITLE", "ORIGINAL_TITLE", "TAGLINE", "PLOT", "YEAR", "RELEASE_DATE", "RATING", "TOP250", "RUNTIME", "CERTIFICATION", "GENRES", "SPOKEN_LANGUAGES", "COUNTRY", "PRODUCTION_COMPANY", "TAGS", "COLLECTION", "TRAILER", "ACTORS", "PRODUCERS", "DIRECTORS", "WRITERS", "POSTER", "FANART", "BANNER", "CLEARART", "THUMB", "LOGO", "CLEARLOGO", "DISCART", "KEYART", "EXTRAFANART", "EXTRATHUMB", "ID", "TITLE", "ORIGINAL_TITLE", "TAGLINE", "PLOT", "YEAR", "RELEASE_DATE", "RATING", "TOP250", "RUNTIME", "CERTIFICATION", "GENRES", "SPOKEN_LANGUAGES", "COUNTRY", "PRODUCTION_COMPANY", "TAGS", "COLLECTION", "TRAILER", "ACTORS", "PRODUCERS", "DIRECTORS", "WRITERS", "POSTER", "FANART", "BANNER", "CLEARART", "THUMB", "LOGO", "CLEARLOGO", "DISCART", "KEYART", "EXTRAFANART", "EXTRATHUMB" ]
       data_config['scraperFallback'] = True
       data_config['imageScraperLanguage'] = 'es'


       json.dump(data_config, jsonFile, indent=4)


def scrap_movies(**kwargs):

    modify_movies_json(f"{kwargs['script_path']}/utilities/tinyMediaManager/data/movies.json", kwargs["tmp_path"])

    exports_folder = f'{kwargs["script_path"]}/utilities/tinyMediaManager/{kwargs["hash_folder"]}'
    if os.path.isdir(exports_folder):
        shutil.rmtree(exports_folder)
    os.mkdir(exports_folder)

    os.system(f'{kwargs["script_path"]}/utilities/tinyMediaManager/tinyMediaManager movie -u --scrapeAll --renameAll -e -eT=movies_to_json -eP=\"{exports_folder}\"')

    cont = 1

    while not os.path.isfile(f'{exports_folder}/movies.json'):

        os.system(f'{kwargs["script_path"]}/utilities/tinyMediaManager/tinyMediaManager movie -e -eT=movies_to_json -eP=\"{exports_folder}\"')
        if cont % 10 != 0:
            send_message = SendMessage(kwargs['script_path'])
            send_message.to_log_bot('ERROR', f'No se ha podido generar el archivo movies.json [{kwargs["file"]}]')

            break
        cont += 1
    folder_name, resolution, poster_path, plot, imdb_rating, imdb_id = rename_files(json_path = f'{exports_folder}/movielist.json', tmp_path=kwargs['tmp_path'], script_path=kwargs['script_path'], category=kwargs['category'], file=kwargs['file'])

    shutil.rmtree(exports_folder)

    with open(f"{kwargs['script_path']}/utilities/tinyMediaManager/data/movies.json", 'r') as jsonFile:
        data_config = json.load(jsonFile)

    with open(f"{kwargs['script_path']}/utilities/tinyMediaManager/data/movies.json", 'w') as jsonFile:
        data_config['movieDataSource'].remove(kwargs["tmp_path"])
        json.dump(data_config, jsonFile, indent=4)
    return folder_name, resolution, poster_path, plot, imdb_rating, imdb_id

def modify_tvshows_json(tvshows_json_path, tmp_path):
    with open(tvshows_json_path, 'r') as jsonFile:
            data_config = json.load(jsonFile)

    with open(tvshows_json_path, 'w') as jsonFile:
        data_config['tvShowDataSource'].append(tmp_path)

        data_config['nfoFilenames'] = ["TV_SHOW"]
        data_config['posterFilenames'] = ["POSTER"]
        data_config['fanartFilenames'] = ["FANART"]
        data_config['bannerFilenames'] = ["BANNER"]
        data_config['clearartFilenames'] = ["CLEARART"]
        data_config['thumbFilenames'] = ["THUMB"]
        data_config['clearlogoFilenames'] = ["CLEARLOGO"]
        data_config['logoFilenames'] = ["LOGO"]
        data_config['characterartFilenames'] = ["CHARACTERART"]
        data_config['keyartFilenames'] = ["KEYART"]
        data_config['seasonPosterFilenames'] = ["SEASON_POSTER"]
        data_config['seasonBannerFilenames'] = ["SEASON_BANNER"]
        data_config['seasonThumbFilenames'] = ["SEASON_THUMB"]
        data_config['episodeNfoFilenames'] = ["FILENAME"]
        data_config['episodeThumbFilenames'] = ["FILENAME_THUMB"]

        data_config['nfoLanguage'] = 'es'
        data_config['scraper'] = 'imdb'
        data_config['scraperLanguage'] = 'es'
        data_config['certificationCountry'] = 'ES'
        data_config['releaseDateCountry'] = 'ES'
        data_config['tvShowScraperMetadataConfig'] = [ "ID", "TITLE", "ORIGINAL_TITLE", "PLOT", "YEAR", "AIRED", "STATUS", "RATING", "RUNTIME", "CERTIFICATION", "GENRES", "COUNTRY", "STUDIO", "TAGS", "TRAILER", "SEASON_NAMES", "ACTORS", "POSTER", "FANART", "BANNER", "CLEARART", "THUMB", "LOGO", "CLEARLOGO", "DISCART", "KEYART", "CHARACTERART", "EXTRAFANART", "SEASON_POSTER", "SEASON_BANNER", "SEASON_THUMB", "THEME", "ID", "TITLE", "ORIGINAL_TITLE", "PLOT", "YEAR", "AIRED", "STATUS", "RATING", "RUNTIME", "CERTIFICATION", "GENRES", "COUNTRY", "STUDIO", "TAGS", "TRAILER", "SEASON_NAMES", "ACTORS", "POSTER", "FANART", "BANNER", "CLEARART", "THUMB", "LOGO", "CLEARLOGO", "DISCART", "KEYART", "CHARACTERART", "EXTRAFANART", "SEASON_POSTER", "SEASON_BANNER", "SEASON_THUMB", "THEME" ]
        data_config['episodeScraperMetadataConfig'] = [ "TITLE", "ORIGINAL_TITLE", "PLOT", "AIRED_SEASON_EPISODE", "DVD_SEASON_EPISODE", "DISPLAY_SEASON_EPISODE", "AIRED", "RATING", "TAGS", "ACTORS", "DIRECTORS", "WRITERS", "PRODUCERS", "THUMB", "TITLE", "ORIGINAL_TITLE", "PLOT", "AIRED_SEASON_EPISODE", "DVD_SEASON_EPISODE", "DISPLAY_SEASON_EPISODE", "AIRED", "RATING", "TAGS", "ACTORS", "DIRECTORS", "WRITERS", "PRODUCERS", "THUMB" ]
        data_config['imageScraperLanguage'] = 'es'
        data_config['subtitleScraperLanguage'] = 'es'
        data_config['preferredRating'] = 'imdb'
        data_config['artworkScrapers'] = ["imdb", "tmdb", "tvdb", "ffmpeg", "fanarttv", "anidb" ]
        data_config['writeCleanNfo'] = True
        data_config['seasonArtworkFallback'] = True



        json.dump(data_config, jsonFile, indent=4)

def scrap_series(**kwargs):

    modify_tvshows_json(f"{kwargs['script_path']}/utilities/tinyMediaManager/data/tvShows.json", kwargs["tmp_path"])

    exports_folder = f'{kwargs["script_path"]}/utilities/tinyMediaManager/{kwargs["hash_folder"]}'
    if  os.path.isdir(exports_folder):
        shutil.rmtree(exports_folder)
    os.mkdir(exports_folder)
    os.system(f'{kwargs["script_path"]}/utilities/tinyMediaManager/tinyMediaManager tvshow -u --scrapeAll --renameAll -e -eT=tvshows_to_json -eP=\"{exports_folder}\"')

    cont = 1

    while not os.path.isfile(f'{exports_folder}/tvShows.json'):
        os.system(f'{kwargs["script_path"]}/utilities/tinyMediaManager/tinyMediaManager tvshow -e -eT=tvshows_to_json -eP=\"{exports_folder}\"')

        if cont % 10 != 0:
            send_message = SendMessage(kwargs['script_path'])
            send_message.to_log_bot('ERROR', f'No se ha podido generar el archivo tvShows.json [{kwargs["file"]}]')

            break
        time.sleep(5)
        cont += 1

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