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

def clean_series_episode_name(episode_name, tracker, logger):

    file_name, file_extension = os.path.splitext(episode_name)
    epiosode_name_cleaned = None

    if 'hd-olimpo' in tracker:
        match = re.search(r'^(.*?)( \((\d{4})\))?( S(\d{2})(E(\d{2}))?(?:-S(\d{2}))?)?.*', file_name)
        if match:
            title = match.group(1).replace('.', ' ').strip()
            season = match.group(3)
            episode = match.group(5)
            epiosode_name_cleaned = f'{title} S{season}E{episode}{file_extension}'

        else:
            logger.info(f'Could not parse series info: {episode_name}')

    elif 'hd-privatehd' in tracker:
        match = re.search(r'^(.*?)[.]([sS](\d{2}))([eE](\d{2}))?.*', file_name)
        if match:
            title = match.group(1).replace('.', ' ').strip()
            season = match.group(3)
            episode = match.group(5)
            epiosode_name_cleaned = f'{title} S{season}E{episode}{file_extension}'

        else:
            logger.info(f'Could not parse series info: {file_name}')

    return epiosode_name_cleaned

def clean_series_folder_name(folder_name, tracker, logger):

    folder_name_cleaned = None

    if 'hd-olimpo' in tracker:
        match = re.search(r'^(.*?)( \((\d{4})\))?( S(\d{2})(E(\d{2}))?(?:-S(\d{2}))?)?.*', folder_name)
        if match:
            title = match.group(1)
            year = match.group(3)
            folder_name_cleaned = f'{title} ({year})' if year else title
        else:
            logger.info(f'Could not parse series info: {folder_name}')
    elif 'hd-privatehd' in tracker:
        match = re.search(r'^([\w.\-]+)([sS](\d{2}))([eE](\d{2}))?.*', folder_name)
        if match:
            folder_name_cleaned = match.group(1).replace('.', ' ')
        else:
            logger.info(f'Could not parse series info: {folder_name}')

    return folder_name_cleaned

def clean_movies_folder_name(file_name, tracker, logger):

    folder_name_cleaned = None

    if 'hd-olimpo' in tracker:
        match = re.search(r'^([^\[\]]*) \((\d{4})\)', file_name)
        if match:
            title = match.group(1).strip()
            year = match.group(2)
            folder_name_cleaned = f'{title} ({year})' if year else title
        else:
            logger.info(f'Could not parse movie info: {file_name}')
    elif 'hd-privatehd' in tracker:
        match = re.search(r'^(.*?)(\d{4}).*', file_name)
        if match:
            title = match.group(1).replace('.', ' ').strip()
            year = match.group(2)
            folder_name_cleaned = f'{title} ({year})' if year else title
        else:
            logger.info(f'Could not parse movie info: {file_name}')

    return folder_name_cleaned

def extract_episode_season_numbers(original_file_name, tracker, logger):

    series_telegram_message = None

    if 'hd-olimpo' in tracker:
        match = re.search(r'^(.*?)( \((\d{4})\))?( S(\d{2})(E(\d{2}))?(?:-S(\d{2}))?)?.*', original_file_name)

        if match:
            title = match.group(1)
            year = match.group(3)
            season_start = match.group(5)
            episode = match.group(7)
            season_end = match.group(8)

            if episode:
                series_telegram_message = f'Title: {title}\nYear: {year}\nSeason: {season_start}\nEpisode: {episode}\nType: Single Episode'
            else:
                if season_end:
                    series_telegram_message = f'Title: {title}\nYear: {year}\nSeason: {season_start}-{season_end}\nType: Multiple Seasons'
                else:
                    series_telegram_message = f'Title: {title}\nYear: {year}\nSeason: {season_start}\nType: Full Season'
        else:
            logger.info(f'Could not parse series info: {original_file_name}')

    elif 'hd-privatehd' in tracker:

        match = re.search(r'^(.*?)( \((\d{4})\))?( [Ss](\d{2})([Ee](\d{2}))?(?:-[Ss](\d{2}))?)?.*', original_file_name)
        if match:
            title = match.group(1)
            year = match.group(3)
            season_start = match.group(5)
            episode = match.group(7)
            season_end = match.group(8)
            if episode:
                series_telegram_message = f'Title: {title}\nYear: {year}\nSeason: {season_start}\nEpisode: {episode}\nType: Single Episode'
            else:
                if season_end:
                    series_telegram_message = f'Title: {title}\nYear: {year}\nSeason: {season_start}-{season_end}\nType: Multiple Seasons'
                else:
                    series_telegram_message = f'Title: {title}\nYear: {year}\nSeason: {season_start}\nType: Full Season'
        else:
            logger.info(f'Could not parse series info: {original_file_name}')

    return series_telegram_message

def handle_series(original_file_name, tracker, source_path, hash_folder_path, logger):

    series_telegram_message = extract_episode_season_numbers(original_file_name=original_file_name, tracker=tracker, logger=logger)

    folder_name_cleaned = clean_series_folder_name(folder_name=original_file_name, tracker=tracker, logger=logger)
    logger.debug(f'folder_name_cleaned {folder_name_cleaned}')

    folder_to_scrap_path = os.path.join(hash_folder_path, folder_name_cleaned)
    logger.debug(f'folder_to_scrap_path: {folder_to_scrap_path}')

    os.makedirs(folder_to_scrap_path, exist_ok=True)

    if os.path.isdir(source_path):
        mkv_files = glob.glob(os.path.join(source_path, '**', '*.mkv'), recursive=True)
        for file in mkv_files:
            base_name = os.path.basename(file)
            episode_name = clean_series_episode_name(episode_name=base_name, tracker=tracker, logger=logger)
            shutil.copy(file, os.path.join(folder_to_scrap_path, episode_name))
    else:
        episode_name = clean_series_episode_name(episode_name=original_file_name, tracker=tracker, logger=logger)
        shutil.copy(source_path, os.path.join(folder_to_scrap_path, episode_name))

    return series_telegram_message

def handle_movies(original_file_name, tracker, source_path, hash_folder_path, logger):

    file_name, file_extension = os.path.splitext(original_file_name)

    folder_name_cleaned = clean_movies_folder_name(file_name=original_file_name, tracker=tracker, logger=logger)
    logger.debug(f'folder_name_cleaned {folder_name_cleaned}')

    folder_to_scrap_path = os.path.join(hash_folder_path, folder_name_cleaned)
    logger.debug(f'folder_to_scrap_path: {folder_to_scrap_path}')

    os.makedirs(folder_to_scrap_path, exist_ok=True)

    shutil.copy(source_path, os.path.join(folder_to_scrap_path, f'{folder_name_cleaned}{file_extension}'))

def rename_and_move(original_file_name, hash_folder_path, source_path, category, tracker, logger):
    # This function determines whether the file is a series or a movie and calls the appropriate function to handle it.
    series_telegram_message = None
    if 'series' in category.lower():

         series_telegram_message = handle_series(original_file_name=original_file_name,
                               tracker=tracker.lower(),
                               source_path=source_path,
                               hash_folder_path=hash_folder_path, logger=logger )
    else:

        handle_movies(original_file_name=original_file_name,
                               tracker=tracker,
                               source_path=source_path,
                               hash_folder_path=hash_folder_path, logger=logger)
    return series_telegram_message
