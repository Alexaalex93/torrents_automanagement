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

def everything_from_last_parenthesis_with_4digits_inside_to_end(filename):
    return re.findall(r'(?!.*[^(]\(\d{4}\)).*\.mkv', filename)[0]

def everything_after_last_parenthesis_with_4digits_inside_to_end(everything_from_last_parenthesis):
    return re.findall(r'(?<=\(\d{4}\)).*\.mkv', everything_from_last_parenthesis)[0]

def get_name_from_parenthesis_and_bracket_format(original_file_name, logger):
    everything_from_last = everything_from_last_parenthesis_with_4digits_inside_to_end(original_file_name)
    logger.debug(f'everything_from_last: {everything_from_last}')
    everything_after_last = everything_after_last_parenthesis_with_4digits_inside_to_end(everything_from_last)
    logger.debug(f'everything_after_last: {everything_after_last}')

    name_trimmed = original_file_name.replace(everything_after_last, '.mkv')
    logger.debug(f'name_trimmed: {name_trimmed}')

    folder_name = name_trimmed.replace('.mkv', '')
    logger.debug(f'folder_name: {folder_name}')

    return folder_name


def everything_after_year_to_end(filename):
    return re.search(r'\b(?!.*\(?(19|20)\d{2}\)?(\.|\s)).*\.mkv', filename)[0]

def year_plus_extension(filename):
    return re.search(r'\(?(19|20)\d{2}\)?\.mkv', filename)[0]

def get_name_from_dot_separated_format(original_file_name, logger):
    everything_after = everything_after_year_to_end(original_file_name)
    logger.debug(f'everything_after: {everything_after}')

    folder_name = original_file_name.replace(everything_after, '.mkv')
    logger.debug(f'folder_name: {folder_name}')

    year_plus_ext = year_plus_extension(folder_name)
    logger.debug(f'year_plus_ext: {year_plus_ext}')

    year = re.findall(r'\d{4}', year_plus_ext)[0]
    logger.debug(f'year: {year}')

    folder_name = folder_name.replace(year_plus_ext, f'({year})')
    logger.debug(f'folder_name: {folder_name}')

    folder_name = folder_name.replace('.', ' ').replace('  ', ' ')
    logger.debug(f'folder_name: {folder_name}')

    return folder_name



def remove_brackets(filename):
    return re.sub(r'\s?\[.*?\]\s?', '', filename)

def remove_series_tags(filename):
    return re.sub(r'(?i)((\((miniserie|serie|documental).*?\)|(miniserie|serie|documental)((de )?tv)?))', '', filename)

def remove_season_and_episode(filename):
    return re.sub(r'(?i)(\s?(\-\s)?)?s\d+(e\d+)?.*', '', filename)

def get_season_episode(filename):
    match = re.search(r'(?i)s\d+(\-(s)?\d+)*(e\d+)?', filename)
    if match:
        return match[0]
    return None

def get_year(filename):
    match = re.search(r'\(?(20|19)\d{2}\)?', filename)
    if match:
        return match[0]
    return None

def replace_multiple_spaces(filename):
    return re.sub(r'\s{2,}', ' ', filename)

def get_series_name_olimpo_format(original_file_name, logger):

    file_with_no_brackets = remove_brackets(original_file_name)
    logger.debug(f'file_with_no_brackets: {file_with_no_brackets}')

    file_with_no_series_tags = remove_series_tags(file_with_no_brackets)
    logger.debug(f'file_with_no_series_tags: {file_with_no_series_tags}')

    file_with_no_season = remove_season_and_episode(file_with_no_series_tags)
    logger.debug(f'file_with_no_season: {file_with_no_season}')

    season_episode = get_season_episode(file_with_no_series_tags)
    logger.debug(f'season_episode: {season_episode}')

    year = get_year(file_with_no_season)
    logger.debug(f'year: {year}')

    folder_name = file_with_no_season
    logger.debug(f'folder_name: {folder_name}')

    if year:
        folder_name =  re.sub(year + '.*', '', file_with_no_season)
        logger.debug(f'folder_name: {folder_name}')

        folder_name = f'{folder_name.strip()} {year}'
        logger.debug(f'folder_name: {folder_name}')

    folder_name = replace_multiple_spaces(folder_name)
    logger.debug(f'folder_name: {folder_name}')

    name_trimmed = f'{folder_name} {season_episode}.mkv'
    logger.debug(f'name_trimmed: {name_trimmed}')

    return folder_name


def determine_file_structure(original_file_name, tracker, logger):
    if 'hd-olimpo' in tracker.lower():
        return get_series_name_olimpo_format(original_file_name, logger) if 'S' in original_file_name else get_name_from_parenthesis_and_bracket_format(original_file_name, logger)
    elif 'privatehd' in tracker.lower():
        return get_name_from_dot_separated_format(original_file_name, logger)

def handle_file(original_file_name, tracker, source_path, hash_folder_path, logger, is_series):
    logger.debug(f'Input variables for handle_file original_file_name: {original_file_name}, tracker: {tracker}, source_path: {source_path}, hash_folder_path: {hash_folder_path}')

    folder_name = determine_file_structure(original_file_name, tracker, logger)

    folder_to_scrap_path = f'{hash_folder_path}/{folder_name}'
    logger.debug(f'folder_to_scrap_path: {folder_to_scrap_path}')

    os.makedirs(folder_to_scrap_path, exist_ok=True)
    file_name = f'{folder_name}.mkv'
    if os.path.isdir(source_path):
        for file in glob.glob(f"{source_path}/*.mkv"):

            if is_series: #revisar estos casos
                file_name = os.path.split(file)[1]
                file_name = re.sub(r'\b(?!.*(\s?(\-\s)?)?(?i)s\d+(e\d+)?).*\.mkv', '.mkv', file_name)
                logger.debug(f'file_name: {file_name}')

            shutil.copy(file, f'{hash_folder_path}/{folder_name}/{file_name}')
            logger.debug(f'shutil.copy({file}, {hash_folder_path}/{folder_name}/{file_name})')

    else:
        if is_series:
            file_name = re.sub(r'\b(?!.*(\s?(\-\s)?)?(?i)s\d+(e\d+)?).*\.mkv', '.mkv', file_name)
        shutil.copy(source_path, f'{hash_folder_path}/{folder_name}/{file_name}')
        logger.debug(f'shutil.copy({source_path}, {hash_folder_path}/{folder_name}/{file_name}')

def handle_series(original_file_name, tracker, source_path, hash_folder_path, logger):
    handle_file(original_file_name, tracker, source_path, hash_folder_path, logger, True)

def handle_movies(original_file_name, tracker, source_path, hash_folder_path, logger):
    handle_file(original_file_name, tracker, source_path, hash_folder_path, logger, False)

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
