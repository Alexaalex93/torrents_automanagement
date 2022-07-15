#!/bin python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 28 11:29:17 2021

@author: alexf
"""

from rename_and_move import rename_and_move
from manage_files import upload_to_drive, upload_to_backup_drive
from scrapper import scrap
from send_message import SendMessage

import argparse
import json
import shutil
import os
import threading
import re
import hashlib
import glob


def create_hash_folder(tmp_path, file):
    hash_folder = hashlib.md5(file.encode('utf-8')).hexdigest()
    if  os.path.isdir(f'{tmp_path}/{hash_folder}'):
        shutil.rmtree(f'{tmp_path}/{hash_folder}')
    os.mkdir(f'{tmp_path}/{hash_folder}')
    return f'{tmp_path}/{hash_folder}', hash_folder

def main(args):

    with open('/scripts/torrents_automanagement/configuration/configuration.json') as configuration_file:
    #with open('/mnt/c/src/torrents_automanagement_pc/configuration/configuration.json') as configuration_file:

        configuration = configuration_file.read().replace('\\', '/')
        configuration = json.loads(configuration)

    send_message = SendMessage(configuration['script_path'])

    original_file_name = os.path.split(args.source_path)[1]
    send_message.to_log_bot('INFO', f'Descargado: {original_file_name}')

    args.source_path = args.source_path.replace('\\', '/')
    args.category = args.category.lower()


    if 'seeding' in args.category.lower():
        return

    #Creating tmp_path
    scrap_folder = '/scrap_series' if 'series' in args.category else '/scrap_movies'
    tmp_path = '/'.join(args.source_path.split('/')[:-2]) + scrap_folder

    if not os.path.isdir(tmp_path):
        os.mkdir(tmp_path)

    tmp_path, hash_folder = create_hash_folder(tmp_path, original_file_name)

    rename_and_move_output = rename_and_move(tracker=args.tracker, source_path=args.source_path, script_path=configuration['script_path'], tmp_path=tmp_path, original_file_name=original_file_name, category= args.category)

    send_message.to_log_bot('INFO', f'Inicio scrapping [{original_file_name}]')

    resolution, poster_path, plot, imdb_rating, imdb_id = scrap(script_path=configuration['script_path'], category=args.category, source_tag=configuration['naming_conventions'][args.category], tmp_path=tmp_path, hash_folder=hash_folder, original_file_name=original_file_name, global_path=configuration['global_path'], docker_tmm_image=configuration['docker_tmm_image'])

    send_message.to_log_bot('INFO', f'Archivo scrapeado [{original_file_name}]')

    current_path = glob.glob(f'{tmp_path}/*')[0]
    folder_name = os.path.split(current_path)[-1]

    upload_to_drive(rclone_path=configuration['rclone_path'], script_path=configuration['script_path'], tmp_path=current_path, remote_name=configuration['equivalences_tags_remote'][args.category], remote_folder=configuration['remote_folders'][args.category], folder_name=rename_and_move_output["folder_name"], original_file_name=original_file_name)
    folder_name = re.sub('\s?\{tmdb-\d+\}', '', folder_name)

    if 'series' in args.category:
        series_caption = ''

        if rename_and_move_output['season_episode']['episode']:
            series_caption = f' Temporada {rename_and_move_output["season_episode"]["seasons"][0]} Episodio {rename_and_move_output["season_episode"]["episode"]}'
        elif rename_and_move_output['season_episode']['seasons']:
            series_caption = f' Temporada {rename_and_move_output["season_episode"]["seasons"][0]} Completa' if len(rename_and_move_output["season_episode"]["seasons"]) == 1 else f' Desde la temporada {rename_and_move_output["season_episode"]["seasons"][0]} a la {rename_and_move_output["season_episode"]["seasons"][-1]} completas'

        folder_name = folder_name + series_caption

    send_message.to_telegram_channel(folder_name=folder_name, resolution=resolution, poster_path=poster_path, plot=plot, imdb_rating=imdb_rating, imdb_id=imdb_id)

    send_message.to_log_bot('INFO', f'Inicio housekeeping [{original_file_name}]')
    shutil.rmtree(tmp_path)
    send_message.to_log_bot('INFO', f'Housekeeping, archivo borrado de carpeta temporal [{original_file_name}]')



if __name__ == "__main__":
    parser = argparse.ArgumentParser(description = "Movies automanagement script")
    parser.add_argument("-p", "--source_path", help = "Path of the download", required=True)
    parser.add_argument("-c", "--category", help = "Torrent category", required=True)
    parser.add_argument("-t", "--tracker", help = "Torrent tracker", required=True)

    args = parser.parse_args()
    main(args)