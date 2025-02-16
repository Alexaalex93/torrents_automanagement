#!/bin python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 28 11:29:17 2021

@author: Alexaalex93
"""

from modules.rename_and_move import rename_and_move
from modules.manage_files import upload_to_drive
from modules.scrapper import scrap

import argparse
import json
import shutil
import os
import re
import sys
import glob
import traceback

import logging
import functools

from utils.send_message import SendMessage
from utils.telegram_log_handler import TelegramLogHandler
from utils.utils import create_hash_folder, create_unique_id

# Define a function decorator to log function calls
def log_function_call(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        logger = logging.getLogger()
        if logger.level == logging.DEBUG:
            kwargs_str = ', '.join(f'{k}={v!r}' for k, v in kwargs.items())
            logger.debug(f"Input variables to {func.__name__}() ---> {func.__name__}({kwargs_str})")
        result = func(*args, **kwargs)
        return result
    return wrapper

# Setup logging with both file logging and telegram logging
@log_function_call
def setup_logging(bot_configuration_path, templates_path, main_directory, unique_id):

    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    formatter = logging.Formatter(f'%(asctime)s - %(levelname)s - %(message)s - Unique ID: {unique_id}')
    logs_path = os.path.join(main_directory, 'logs')

    if not os.path.exists(logs_path):
        os.makedirs(logs_path)

    file_handler = logging.FileHandler(os.path.join(main_directory, 'logs', 'logs.log'))
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    telegram_handler = TelegramLogHandler(bot_configuration_path, templates_path, unique_id)
    telegram_handler.setLevel(logging.INFO)

    telegram_handler.setFormatter(formatter)
    logger.addHandler(telegram_handler)

# Load configurations from the configuration files
@log_function_call
def load_configuration(main_directory):

    configuration_path = os.path.join(main_directory, '..', 'configuration', 'app_configuration.json')
    bot_configuration_path = os.path.join(main_directory, '..', 'configuration', 'bot_configuration.json')
    templates_path = os.path.join(main_directory, '..', 'templates')

    with open(configuration_path) as configuration_file:

        configuration = json.load(configuration_file)

    return configuration, bot_configuration_path, templates_path

# Prepare a temporary folder for processing
@log_function_call
def prepare_temporary_folder(source_path, category, original_file_name, logger):

    source_path = os.path.normpath(source_path)
    category = category.lower()

    logger.info('Creating temporary folder')
    tmp_path = os.path.dirname(os.path.dirname(source_path))

    logger.debug(f'tmp_path: {tmp_path}')

    posters_folder_path = os.path.join(tmp_path, 'posters')

    logger.debug(f'tmp_path_posters: {posters_folder_path}')

    scrap_subdir = 'scrap_series' if 'series' in category else 'scrap_movies'

    scrap_folder = os.path.join(tmp_path, scrap_subdir)

    logger.debug(f'tmp_path after creating subdirs: {scrap_folder}')

    if not os.path.isdir(scrap_folder):
        os.mkdir(scrap_folder)

    if not os.path.isdir(posters_folder_path):
        os.mkdir(posters_folder_path)

    hash_folder_path, hash_folder = create_hash_folder(scrap_folder, original_file_name)

    if os.path.isdir(hash_folder_path):
        shutil.rmtree(hash_folder_path)

    os.mkdir(hash_folder_path)
    logger.debug(f'Folder {hash_folder} created')

    logger.debug(f'After create_hash_folder hash_folder_path: {hash_folder_path}, hash_folder: {hash_folder}')

    return hash_folder_path, hash_folder, posters_folder_path

# Process the downloaded file, rename, move and scrap it
@log_function_call
def process_downloaded_file(args, configuration, hash_folder_path, posters_folder_path, hash_folder, logger):

    original_file_name = os.path.split(args.source_path)[1]

    logger.info('Downloaded')

    try:

        logger.info('Moving file to temporary folder')

        series_telegram_message = rename_and_move(original_file_name=original_file_name, hash_folder_path=hash_folder_path, downloads_mount_point=configuration['downloads_mount_point'], source_path=args.source_path, category=args.category, tracker=args.tracker, logger=logger)

        logger.info('File moved to temporary folder')

    except Exception as e:
        logger.error(f'Error moving the file to temporary folder: {e}')
        tb = traceback.format_exc()
        logger.error(tb)
        sys.exit(1)
    try:
        logger.info('Starting scraping')

        poster_path = scrap(posters_folder_path=posters_folder_path, hash_folder=hash_folder, category=args.category, hash_folder_path=hash_folder_path, downloads_mount_point=configuration['downloads_mount_point'], tmm_configuration_path=configuration['tmm_configuration_path'], logger=logger)

        logger.debug(f'Result after scrap poster_path: {poster_path}')
        logger.info('File scraped')

    except Exception as e:
        logger.error(f'Error while scraping: {e}')
        tb = traceback.format_exc()
        logger.error(tb)

    return poster_path, series_telegram_message

# Create the title for the file
@log_function_call
def create_title(hash_folder_path, category, logger):

    folder_to_upload_path = glob.glob(os.path.join(hash_folder_path, '*'))[0]
    logger.debug(f'Glob result of os.path.join(hash_folder_path, *) {folder_to_upload_path}')
    folder_name = os.path.split(folder_to_upload_path)[-1]
    title = re.sub(r'\s?\{tmdb-\d+\}', '', folder_name)

    resolution = '1080p' if category.split('_')[1] == 'fhd' else '2160p'

    return title, resolution, folder_to_upload_path

# Upload the file to Google Drive
@log_function_call
def upload_file_to_drive(folder_to_upload_path, category, logger):

    destination_folder_name = os.path.split(folder_to_upload_path)[-1]

    try:
        logger.info('Starting upload to Google Drive')
        upload_to_drive(folder_to_upload_path=folder_to_upload_path, destination_folder_name=destination_folder_name, remote_name=category, logger=logger)
        logger.info('Upload finished')

    except Exception as e:
        logger.error(f'Error while uploading the file: {e}')
        tb = traceback.format_exc()
        logger.error(tb)
        sys.exit(1)

# Move to local folder
@log_function_call
def move_to_local_folder(folder_to_upload_path, category, logger):

    destination_folder_name = os.path.split(folder_to_upload_path)[-1]
    if 'series' in category:
        category = 'series'
    else:
        category = 'peliculas'

    try:
        logger.info('Starting to move')

        final_path = os.path.join('/multimedia', 'local', category, destination_folder_name)

        for raiz, carpetas, archivos in os.walk(folder_to_upload_path, topdown=True):
            # Determinar el path relativo de la raíz actual al path de origen para mantener la estructura
            rel_path = os.path.relpath(raiz, folder_to_upload_path)
            destino_raiz = os.path.join(final_path, rel_path)

            # Crear carpetas en el destino si no existen
            os.makedirs(destino_raiz, exist_ok=True)

            # Mover cada archivo al destino, sobrescribiendo si ya existe
            for archivo in archivos:
                origen_archivo = os.path.join(raiz, archivo)
                destino_archivo = os.path.join(destino_raiz, archivo)

                # Sobrescribir el archivo si ya existe
                if os.path.isfile(destino_archivo):
                    os.remove(destino_archivo)
                    logger.info(f"Archivo anterior eliminado: {destino_archivo}")

                # Copiamos el archivo manteniendo metadatos
                shutil.copy2(origen_archivo, destino_archivo)
                
                logger.info(f"Archivo copiado: {origen_archivo} -> {destino_archivo}")

                # Eliminamos el archivo original después de copiarlo
                os.remove(origen_archivo)
                
                logger.info(f"Archivo original eliminado: {origen_archivo}")

        logger.info('Move finished')

    except Exception as e:
        logger.error(f'Error while uploading the file: {e}')
        tb = traceback.format_exc()
        logger.error(tb)
        sys.exit(1)


# Perform cleaning operations
@log_function_call
def perform_housekeeping(hash_folder_path, logger):

    try:
        logger.info('Starting housekeeping')

        shutil.rmtree(hash_folder_path)

        logger.info('Housekeeping, file deleted from temporary folder')

    except Exception as e:
        logger.error(f'Error in housekeeping, could not delete the temporary folder: {e}')
        tb = traceback.format_exc()
        logger.error(tb)
        sys.exit(1)

# The main function orchestrates the entire flow
@log_function_call
def main(args):

    main_file_path = os.path.abspath(__file__)
    main_directory = os.path.dirname(main_file_path)

    configuration, bot_configuration_path, templates_path = load_configuration(main_directory)

    original_file_name = os.path.split(args.source_path)[1]

    unique_id = create_unique_id(original_file_name)
    setup_logging(bot_configuration_path, templates_path, main_directory, unique_id)

    logger = logging.getLogger()
    logger.debug('####################################################################################################')
    logger.debug('####################################################################################################')
    logger.debug('####################################################################################################')
    logger.debug(f'Executed command: python {os.path.join(main_directory,"main.py")} --source_path \"{args.source_path}\" --category \"{args.category}\" --tracker \"{args.tracker}\"')
    logger.debug('####################################################################################################')
    logger.debug('####################################################################################################')
    logger.debug('####################################################################################################')

    send_message = SendMessage(bot_configuration_path, templates_path)
    source_path = args.source_path.encode('utf-8').decode('utf-8')

    try:

        logger.debug('Starting the process')


        if args.category or args.category !='upload':
            hash_folder_path, hash_folder, posters_folder_path = prepare_temporary_folder(source_path=source_path, category=args.category, original_file_name=original_file_name, logger=logger)

            logger.debug(f'Output variables from prepare_temporary_folder() ---> hash_folder_path: {hash_folder_path}, posters_folder_path: {posters_folder_path}, hash_folder: {hash_folder}')

            poster_path, series_telegram_message = process_downloaded_file(args=args, configuration=configuration, hash_folder_path=hash_folder_path, posters_folder_path=posters_folder_path, hash_folder=hash_folder, logger=logger)

            logger.debug(f'Output variables from process_downloaded_file() ---> poster_path: {poster_path}. series_telegram_message: {series_telegram_message}')

            title, resolution, folder_to_upload_path = create_title(hash_folder_path=hash_folder_path, category=args.category, logger=logger)

            title = series_telegram_message if ('series' in args.category and series_telegram_message is not None) else title

            logger.debug(f'Output variables from create_title() ---> title: {title}, resolution: {resolution}, folder_to_upload_path: {folder_to_upload_path}')
        else:
            args.category = 'upload'
            folder_to_upload_path = source_path
        if args.upload_to_google_drive == 'True':
            upload_file_to_drive(folder_to_upload_path=folder_to_upload_path, category=args.category, logger=logger)
        else:
            move_to_local_folder(folder_to_upload_path=folder_to_upload_path, category=args.category, logger=logger)

        if args.category != 'upload':
            send_message.send(template_name='channel_message_template', title=title, resolution=resolution, photo=poster_path)
            perform_housekeeping(hash_folder_path=hash_folder_path, logger=logger)

    except Exception as e:

       logger.critical( f'General error in the script: {e}')
       tb = traceback.format_exc()
       logger.error(tb)
       sys.exit(1)


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description = "Movies automanagement script")
    parser.add_argument("-p", "--source_path", help = "Path of the download", required=True)
    parser.add_argument("-c", "--category", help = "Torrent category", required=True)
    parser.add_argument("-t", "--tracker", help = "Torrent tracker", required=True)
    parser.add_argument("-u", "--upload_to_google_drive", type=str, choices=["True", "False"], default="False")

    args = parser.parse_args()
    main(args)
