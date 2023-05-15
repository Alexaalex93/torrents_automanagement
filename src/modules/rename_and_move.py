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
import re


def get_name_from_parenthesis_and_bracket_format(original_file_name):
    # This function extracts and processes the movie name from a name structure in parenthesis and brackets format.

    everything_from_last_parenthesis_with_4digits_inside_to_end = re.findall(r'(?!.*[^(]\(\d{4}\)).*\.mkv', original_file_name)[0]
    everything_after_last_parenthesis_with_4digits_inside_to_end = re.findall(r'(?<=\(\d{4}\)).*\.mkv', everything_from_last_parenthesis_with_4digits_inside_to_end)[0]

    movie_name = original_file_name.replace(everything_after_last_parenthesis_with_4digits_inside_to_end, '.mkv')
    folder_name = movie_name.replace('.mkv', '')

    return movie_name, folder_name

def get_name_from_dot_separated_format(original_file_name):
    # This function extracts and processes the movie name from a name structure in dot separated format.

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
    # This function extracts and processes the series name from a name structure in Olimpo format.

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

def handle_series(original_file_name, tracker, source_path, hash_folder_path, logger):
    # This function handles series files, copying and renaming them as needed.

    logger.debug(f'Valores de entrada de handle_series original_file_name: {original_file_name}, tracker: {tracker}, source_path: {source_path}, hash_folder_path: {hash_folder_path}')

    if 'hd-olimpo' in tracker.lower():

        folder_name, season_episode = get_series_name_olimpo_format(original_file_name)
    folder_to_scrap_path = f'{hash_folder_path}/{folder_name}'
    os.mkdir(folder_to_scrap_path)

    if os.path.isdir(source_path):

        for file in glob.glob(f"{source_path.replace('[', '*[').replace(']', ']*').replace('*[', '[[]').replace(']*', '[]]')}/*.mkv"):

            file_name = os.path.split(file)[1]
            file_name = re.sub(r'\b(?!.*(\s?(\-\s)?)?(?i)s\d+(e\d+)?).*\.mkv', '.mkv', file_name)
            shutil.copy(file, f'{hash_folder_path}/{folder_name}/{file_name}')

        for mkv in glob.glob(f'{hash_folder_path}/{folder_name}/*.mkv'):

            os.rename(mkv, re.sub(r'\b(?!.*(\s?(\-\s)?)?(?i)s\d+(e\d+)?).*\.mkv', '.mkv', mkv))
    else:

        file_name = os.path.split(source_path)[1]
        file_name = re.sub(r'\b(?!.*(\s?(\-\s)?)?(?i)s\d+(e\d+)?).*\.mkv', '.mkv', file_name)
        shutil.copy(source_path, f'{hash_folder_path}/{folder_name}/{file_name}')


def handle_movies(original_file_name, tracker, source_path, hash_folder_path, logger):
    # This function handles movie files, copying and renaming them as needed.

    logger.debug(f'Input variables for handle_movies original_file_name: {original_file_name}, tracker: {tracker}, source_path: {source_path}, hash_folder_path: {hash_folder_path}')

    if 'hd-olimpo' in tracker.lower():

        movie_name, folder_name = get_name_from_parenthesis_and_bracket_format(original_file_name)

    elif 'privatehd' in tracker.lower():

        movie_name, folder_name = get_name_from_dot_separated_format(original_file_name)

    folder_to_scrap_path = f'{hash_folder_path}/{folder_name}'
    os.mkdir(folder_to_scrap_path)

    if os.path.isdir(source_path):

        for file in glob.glob(f"{source_path}/*.mkv"):

            shutil.copy(file, f'{hash_folder_path}/{folder_name}/{movie_name}')
    else:

        shutil.copy(source_path, f'{hash_folder_path}/{folder_name}/{movie_name}')


def rename_and_move(original_file_name, hash_folder_path, source_path, category, tracker, logger):
    # This function determines whether the file is a series or a movie and calls the appropriate function to handle it.

    if 'series' in category.lower():

         handle_series(original_file_name=original_file_name,
                               tracker=tracker,
                               source_path=source_path,
                               hash_folder_path=hash_folder_path, logger=logger )
    else:

        handle_movies(original_file_name=original_file_name,
                               tracker=tracker,
                               source_path=source_path,
                               hash_folder_path=hash_folder_path, logger=logger)
