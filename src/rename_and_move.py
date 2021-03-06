# -*- coding: utf-8 -*-
"""
Created on Mon Apr 11 12:17:15 2022

@author: AlexPC
"""

# -*- coding: utf-8 -*-
"""
Created on Thu Jul 29 13:01:27 2021

@author: alexf
"""
import glob
import os
import shutil
from send_message import SendMessage
import re
import sys

def get_name_from_parenthesis_and_bracket_format(original_file_name):

    everything_from_last_parenthesis_with_4digits_inside_to_end = re.findall(r'(?!.*[^(]\(\d{4}\)).*\.mkv', original_file_name)[0]
    everything_after_last_parenthesis_with_4digits_inside_to_end = re.findall(r'(?<=\(\d{4}\)).*\.mkv', everything_from_last_parenthesis_with_4digits_inside_to_end)[0]

    movie_name = original_file_name.replace(everything_after_last_parenthesis_with_4digits_inside_to_end, '.mkv')
    folder_name = movie_name.replace('.mkv', '')

    return movie_name, folder_name

def get_name_from_dot_separated_format(original_file_name):

    everything_after_year_to_end = re.search(r'\b(?!.*\(?(19|20)\d{2}\)?(\.|\s)).*\.mkv', original_file_name)[0]
    folder_name = original_file_name.replace(everything_after_year_to_end, '.mkv')
    year_plus_extension = re.search(r'\(?(19|20)\d{2}\)?\.mkv', folder_name)[0]
    year = re.findall(r'\d{4}', year_plus_extension)[0]
    folder_name = folder_name.replace(year_plus_extension, f'({year})')
    #Removing dot separation
    folder_name = folder_name.replace('.', ' ').replace('  ', ' ')
    movie_name = f'{folder_name}.mkv'

    return movie_name, folder_name

def get_series_name_olimpo_format(original_file_name):

    season_episode = {'seasons':[], 'episode':None}

    remove_brackets = r'\s?\[.*?\]\s?'
    remove_series_tags = r'((?i)\((miniserie|serie|documental).*?\)|(?i)(miniserie|serie|documental)((de )?tv)?)'
    remove_season_and_episonde_until_end = r'(\s?(\-\s)?)?(?i)s\d+(e\d+)?.*'
    replace_mutiples_spaces_by_one = r'\s{2,}'

    get_year = r'\(?(20|19)\d{2}\)?'
    get_season_episode = r'(?i)s\d+(\-(s)?\d+)*(e\d+)?'
    file_with_no_brackets = re.sub(remove_brackets, '', original_file_name)
    file_with_no_series_tags = re.sub(remove_series_tags, '', file_with_no_brackets)

    if re.search(get_season_episode, file_with_no_series_tags):
        season_episode_raw = re.search(get_season_episode, file_with_no_series_tags)[0]
        if '-' in season_episode_raw:
            season_episode['seasons'] = [int(re.sub(r'(?i)s', '', season)) for season in season_episode_raw.split('-')]
        else:
            season = re.search(r'(?i)s\d+', season_episode_raw)[0].lower().replace('s', '')
            season_episode['seasons'] = [int(season)]

            if 'e' in season_episode_raw.lower():
                episode = re.search(r'(?i)e\d+', season_episode_raw)[0].lower().replace('e', '')
                season_episode['episode'] = int(episode)

    file_with_no_season = re.sub(remove_season_and_episonde_until_end, '', file_with_no_series_tags)


    if  re.search(get_year, file_with_no_season):
        raw_year = re.search(get_year, file_with_no_season)[0]
        year = '(' + re.sub(r'\(|\s|\)', '', raw_year) + ')'

        folder_name =  re.sub(get_year + '.*', '', file_with_no_season)
        folder_name = f'{folder_name.strip()} {year}'
    else:
        folder_name = file_with_no_season
    folder_name = re.sub(replace_mutiples_spaces_by_one, ' ', folder_name)

    return folder_name, season_episode


def rename_and_move(**kwargs):

    send_message = SendMessage(kwargs['script_path'])

    try:
        ##Separar peliculas de series. Si es pelicula ver si esta en una carpeta o no
        if 'series' in kwargs['category'].lower():
            if 'hd-olimpo' in kwargs['tracker'].lower():
                folder_name, season_episode = get_series_name_olimpo_format(kwargs['original_file_name'])

            send_message.to_log_bot('INFO', f'Moviendo a carpeta temporal [{kwargs["original_file_name"]}]')

            os.mkdir(f'{kwargs["tmp_path"]}/{folder_name}')

            #Cojo todos los mkv esten o no en subcarpetas y le quito toda la morralla que haya despues de la temporada y episodio
            if os.path.isdir(kwargs["source_path"]):

                shutil.copytree(kwargs["source_path"] + '/', f'{kwargs["tmp_path"]}/{folder_name}/', dirs_exist_ok=True)

                for mkv in  glob.glob(f'{kwargs["tmp_path"]}/{folder_name}/*.mkv'):
                    os.rename(mkv, re.sub(r'\b(?!.*(\s?(\-\s)?)?(?i)s\d+(e\d+)?).*\.mkv', '.mkv', mkv))
            else:

                file_name = os.path.split(kwargs["source_path"])[1]
                file_name = re.sub(r'\b(?!.*(\s?(\-\s)?)?(?i)s\d+(e\d+)?).*\.mkv', '.mkv' , file_name)

                shutil.copy(kwargs["source_path"], f'{kwargs["tmp_path"]}/{folder_name}/{file_name}')

            send_message.to_log_bot('INFO', f'Movido a carpeta temporal [{kwargs["original_file_name"]}]')

            return {'folder_name':folder_name, 'season_episode':season_episode}
        else:
            if os.path.isdir(kwargs['source_path']):
                return 'hola'
            else:
                if 'hd-olimpo' in kwargs['tracker'].lower():
                    movie_name, folder_name = get_name_from_parenthesis_and_bracket_format(kwargs['original_file_name'])
                elif 'privatehd' in kwargs['tracker'].lower():
                    movie_name, folder_name = get_name_from_dot_separated_format(kwargs['original_file_name'])

                send_message.to_log_bot('INFO', f'Moviendo a carpeta temporal [{kwargs["original_file_name"]}]')

                os.mkdir(f'{kwargs["tmp_path"]}/{folder_name}')
                shutil.copy(kwargs['source_path'], f'{kwargs["tmp_path"]}/{folder_name}/{movie_name}')
                send_message.to_log_bot('INFO', f'Movido a carpeta temporal [{kwargs["original_file_name"]}]')

                return {'folder_name':folder_name, 'movie_name':movie_name}

    except Exception as exc:
        print('ERROR', f'Error con archivo [{kwargs["original_file_name"]}] en funcion rename_and_move(), Error: {str(exc)}')
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno)

        send_message.to_log_bot('ERROR', f'Error con archivo [{kwargs["original_file_name"]}] en funcion rename_and_move(), Error: {str(exc)}')
        send_message.to_log_bot('ERROR', f'{exc_type}, {fname}, {exc_tb.tb_lineno}')