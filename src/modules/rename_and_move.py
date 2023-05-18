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

def extract_season_range(season_episode):
    pattern = r"(?:s|t|season|temporada|temp)\d+"
    matches = re.findall(pattern, season_episode, re.IGNORECASE)

    if len(matches) == 1:
        season_start = matches[0]
        season_end = None
    elif len(matches) >= 2:
        season_start = matches[0]
        season_end = matches[-1]
    else:
        season_start = None
        season_end = None

    return season_start, season_end

def extract_episode(season_episode):
    pattern = r"(?:episodio|episode|capitulo|cap|ep|c|E)\d+"
    matches = re.findall(pattern, season_episode, re.IGNORECASE)

    if len(matches) > 0:
        return matches[0]
    return None


def get_series_telegram_message(original_file_name, title, year, tracker, logger):
    logger.debug(f'get_series_telegram_message(original_file_name="{original_file_name}", tracker="{tracker}", logger="{logger}")')

    series_telegram_message = None

    if 'hd-olimpo' in tracker:

        logger.debug('Inside olimpo condition')
        season_episode_match = re.search(r'((?:s|t|season|temporada|temp)\s*?\d{1,3}(?:\s*-\s*(?:s|t|season|temporada|temp)\s*\d{1,3})?(?:\s*(?:episodio|episode|capitulo|cap|ep|c|e)\s*\d{1,3})?)', original_file_name, re.IGNORECASE)

        season_episode = season_episode_match.group(1).strip()
        season_start, season_end = extract_season_range(season_episode)
        logger.debug(f'season_start: {season_start}')
        logger.debug(f'season_end: {season_end}')

        episode = extract_episode(season_episode)
        logger.debug(f'episode: {episode}')

        if episode:
            if year:
                series_telegram_message = f'{title}\nYear: {year}\nSeason: {season_start}\nEpisode: {episode}\nType: Single Episode'
            else:
                series_telegram_message = f'{title}\nSeason: {season_start}\nEpisode: {episode}\nType: Single Episode'
        else:
            if year:
                if season_end:
                    series_telegram_message = f'{title}\nYear: {year}\nSeason: {season_start}-{season_end}\nType: Multiple Seasons'
                else:
                    series_telegram_message = f'{title}\nYear: {year}\nSeason: {season_start}\nType: Full Season'
            else:
                if season_end:
                    series_telegram_message = f'{title}\nSeason: {season_start}-{season_end}\nType: Multiple Seasons'
                else:
                    series_telegram_message = f'{title}\nSeason: {season_start}\nType: Full Season'

    elif 'hd-privatehd' in tracker:
        logger.debug('Inside privatehd condition')

        match = re.search(r'^(.*?)( \((\d{4})\))?( [Ss](\d{2})([Ee](\d{2}))?(?:-[Ss](\d{2}))?)?.*', original_file_name)
        if match:
            title = match.group(1)
            logger.debug(f'title: {title}')

            year = match.group(3)
            logger.debug(f'year: {year}')

            season_start = match.group(5)
            logger.debug(f'season_start: {season_start}')

            episode = match.group(7)
            logger.debug(f'episode: {episode}')

            season_end = match.group(8)
            logger.debug(f'season_end: {season_end}')

            if episode:
                series_telegram_message = f'{title}\nYear: {year}\nSeason: {season_start}\nEpisode: {episode}\nType: Single Episode'
            else:
                if season_end:
                    series_telegram_message = f'{title}\nYear: {year}\nSeason: {season_start}-{season_end}\nType: Multiple Seasons'
                else:
                    series_telegram_message = f'{title}\nYear: {year}\nSeason: {season_start}\nType: Full Season'
        else:
            logger.info(f'Could not parse series info: {original_file_name}')

    return series_telegram_message


def clean_series_episode_name(episode_name, tracker, logger):
    logger.debug(f'clean_series_episode_name(episode_name="{episode_name}", tracker="{tracker}", logger="{logger}")')

    file_name, file_extension = os.path.splitext(episode_name)
    logger.debug(f'file_name: {file_name}, file_extension: {file_extension}')
    epiosode_name_cleaned = None
    #(?:S|t|season|temporada|temp)\s*?\d{1,3}(?:\s*-\s*(?:S|t|season|temporada|temp)\s*\d{1,3})?(?:\s*(?:episodio|episode|capitulo|cap|ep|c|E)\s*\d{1,3})?
    #Regex para coger temporada y capitulo
    #\((?:19|20)\d{2}\)
    #Regex para capturar año
    #(^(.*?)(?:(?:(?:\((?:19|20)\d{2}\))|(?:(?:S|t|season|temporada|temp)\s*?\d{1,3}(?:\s*-\s*(?:S|t|season|temporada|temp)\s*\d{1,3})?(?:\s*(?:episodio|episode|capitulo|cap|ep|c|E)\s*\d{1,3})?))|$))|(\((?:19|20)\d{2}\))|((?:S|t|season|temporada|temp)\s*?\d{1,3}(?:\s*-\s*(?:S|t|season|temporada|temp)\s*\d{1,3})?(?:\s*(?:episodio|episode|capitulo|cap|ep|c|E)\s*\d{1,3})?)
    #Regex que captura todo siendo el titulo (que hay que hacer trim) en el grupo 2,
    if 'hd-olimpo' in tracker:
        logger.debug('Inside olimpo condition')

        title_match = re.search(r'^(.*?)(?:(?:(?:\((?:19|20)\d{2}\))|(?:(?:s|t|season|temporada|temp)\s*?\d{1,3}(?:\s*-\s*(?:s|t|season|temporada|temp)\s*\d{1,3})?(?:\s*(?:episodio|episode|capitulo|cap|ep|c|e)\s*\d{1,3})?))|$)', episode_name, re.IGNORECASE)
        title = re.sub(r'^[^a-zA-Z0-9]+|[^a-zA-Z0-9]+$', '', title_match.group(1)) if title_match else None
        logger.debug(f'title: {title}')

        season_episode_match = re.search(r'((?:S|t|season|temporada|temp)\s*?\d{1,3}(?:\s*-\s*(?:s|t|season|temporada|temp)\s*\d{1,3})?(?:\s*(?:episodio|episode|capitulo|cap|ep|c|e)\s*\d{1,3})?)', episode_name, re.IGNORECASE)
        season_episode = season_episode_match.group(1)
        logger.debug(f'season_episode: {season_episode}')


        epiosode_name_cleaned = f'{title} {season_episode}{file_extension}'



    elif 'hd-privatehd' in tracker:
        logger.debug('Inside privatehd condition')

        match = re.search(r'^(.*?)[.]([sS](\d{2}))([eE](\d{2}))?.*', episode_name)
        if match:
            title = match.group(1).replace('.', ' ').strip()
            logger.debug(f'title: {title}')

            season = match.group(3)
            logger.debug(f'season: {season}')

            episode = match.group(5)
            logger.debug(f'episode: {episode}')
            epiosode_name_cleaned = f'{title} S{season}E{episode}{file_extension}'

        else:
            logger.info(f'Could not parse series info: {episode_name}')

    return epiosode_name_cleaned

def clean_series_folder_name(folder_name, tracker, logger):
    logger.debug(f'clean_series_folder_name(folder_name="{folder_name}", tracker="{tracker}", logger="{logger}")')

    folder_name_cleaned = None

    if 'hd-olimpo' in tracker:
        logger.debug('Inside olimpo condition')

        title_match = re.search(r'^(.*?)(?:(?:(?:\((?:19|20)\d{2}\))|(?:(?:s|t|season|temporada|temp)\s*?\d{1,3}(?:\s*-\s*(?:s|t|season|temporada|temp)\s*\d{1,3})?(?:\s*(?:episodio|episode|capitulo|cap|ep|c|e)\s*\d{1,3})?))|$)', folder_name, re.IGNORECASE)

        title = re.sub(r'^[^a-zA-Z0-9]+|[^a-zA-Z0-9]+$', '', title_match.group(1)) if title_match else None
        logger.debug(f'title: {title}')

        year_match = re.search(r'(\(?(?:19|20)\d{2}\)?)', folder_name, re.IGNORECASE)

        year = re.sub(r"\(|\)", "", year_match.group(1)) if year_match else None

        logger.debug(f'year: {year}')

        folder_name_cleaned = f'{title} ({year})' if year else title

    elif 'hd-privatehd' in tracker:
        logger.debug('Inside privatehd condition')

        match = re.search(r'^([\w.\-]+)([sS](\d{2}))([eE](\d{2}))?.*', folder_name)
        if match:
            folder_name_cleaned = match.group(1).replace('.', ' ')
            logger.debug(f'folder_name_cleaned: {folder_name_cleaned}')

        else:
            logger.info(f'Could not parse series info: {folder_name}')

    series_telegram_message = get_series_telegram_message(folder_name, title, year, tracker, logger)

    return folder_name_cleaned, series_telegram_message

def clean_movies_folder_name(file_name, tracker, logger):
    logger.debug(f'clean_movies_folder_name(file_name="{file_name}", tracker="{tracker}", logger="{logger}")')

    folder_name_cleaned = None

    if 'hd-olimpo' in tracker:
        logger.debug('Inside olimpo condition')

        match = re.search(r'^([^\[\]]*) \((\d{4})\)', file_name)
        if match:
            title = match.group(1).strip()
            year = match.group(2)
            folder_name_cleaned = f'{title} ({year})' if year else title
        else:
            logger.info(f'Could not parse movie info: {file_name}')
    elif 'hd-privatehd' in tracker:
        logger.debug('Inside privatehd condition')

        match = re.search(r'^(.*?)(\d{4}).*', file_name)
        if match:
            title = match.group(1).replace('.', ' ').strip()
            year = match.group(2)
            folder_name_cleaned = f'{title} ({year})' if year else title
        else:
            logger.info(f'Could not parse movie info: {file_name}')

    return folder_name_cleaned

def escape_glob_pattern(pattern):
    escaped_pattern = re.sub(r'\[', r'[[', pattern)
    escaped_pattern = re.sub(r'\]', r']]', escaped_pattern)
    escaped_pattern = re.sub(r'\[\[', r'[[]', escaped_pattern)
    escaped_pattern = re.sub(r'\]\]', r'[]]', escaped_pattern)
    return escaped_pattern

def handle_series(original_file_name, tracker, source_path, hash_folder_path, logger):

    folder_name_cleaned, series_telegram_message = clean_series_folder_name(folder_name=original_file_name, tracker=tracker, logger=logger)
    logger.debug(f'folder_name_cleaned {folder_name_cleaned}')

    folder_to_scrap_path = os.path.join(hash_folder_path, folder_name_cleaned)
    logger.debug(f'folder_to_scrap_path: {folder_to_scrap_path}')


    os.makedirs(folder_to_scrap_path, exist_ok=True)

    if os.path.isdir(source_path):

        source_path_escaped = escape_glob_pattern(source_path)
        files_path = os.path.join(source_path_escaped, '**', '*.mkv')
        logger.debug(f'files_path: {files_path}')
        glob.glob('/downloads/series_fhd_webdl/Holding\ \(2022\)\ S01\ \[MiniSerie\]\[FILMN\ WEB\-DL\ 1080p\ AVC\ ES\-EN\ AAC\ 5\.1\-2\.0\ Subs\]\[HDO\]/**/*.mkv', recursive=True)

        mkv_files = glob.glob(files_path, recursive=True)
        logger.debug(f'mkv_files: {mkv_files}')
        for file in mkv_files:
            base_name = os.path.basename(file)
            episode_name = clean_series_episode_name(episode_name=base_name, tracker=tracker, logger=logger)
            episode_destination = os.path.join(folder_to_scrap_path, episode_name)
            shutil.copy(file, episode_destination)
            logger.debug(f'Copied {file} to {episode_destination}')

    else:
        episode_name = clean_series_episode_name(episode_name=original_file_name, tracker=tracker, logger=logger)
        episode_destination= os.path.join(folder_to_scrap_path, episode_name)
        shutil.copy(source_path, episode_destination)
        logger.debug(f'Copied {file} to {episode_destination}')

    return series_telegram_message

def handle_movies(original_file_name, tracker, source_path, hash_folder_path, logger):

    file_name, file_extension = os.path.splitext(original_file_name)

    folder_name_cleaned = clean_movies_folder_name(file_name=original_file_name, tracker=tracker, logger=logger)
    logger.debug(f'folder_name_cleaned {folder_name_cleaned}')

    folder_to_scrap_path = os.path.join(hash_folder_path, folder_name_cleaned)
    logger.debug(f'folder_to_scrap_path: {folder_to_scrap_path}')

    os.makedirs(folder_to_scrap_path, exist_ok=True)

    movie_destination = os.path.join(folder_to_scrap_path, f'{folder_name_cleaned}{file_extension}')

    shutil.copy(source_path, movie_destination)
    logger.debug(f'Copied {source_path} to {movie_destination}')


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
