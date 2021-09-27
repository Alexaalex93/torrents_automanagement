#!/bin python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 28 11:29:17 2021

@author: alexf
"""

from convert_and_move import check_extension
from manage_files import upload_to_drive, upload_to_backup_drive
from scrapper import scrap_movies, scrap_series
from send_message import SendMessage
from refactor_series import refactor_series

import argparse
import json
import shutil
import os
import threading
import re

def get_season_episode_number(file):
    season_episode = re.search(r'\s(?i)s\d{1,2}(e\d{1,2})?\s', file)[0].strip()
    if 'e' in season_episode.lower():
        season = re.search(r'(?i)s\d{1,2}', season_episode)[0].lower().replace('s', '\n\nTemporada ')
        episode = re.search(r'(?i)e\d{1,2}', season_episode)[0].lower().replace('e', ' Episodio ')
        season_episode = season + episode
    else:
        season_episode = season_episode.lower().replace('s', '\n\nTemporada Completa ')
        
    return season_episode

def main(args):

    with open('/scripts/torrents_automanagement/configuration/configuration.json') as configuration_file:
    #with open('/mnt/c/src/torrents_automanagement/configuration/configuration.json') as configuration_file:

        configuration = configuration_file.read().replace('\\', '/')
        configuration = json.loads(configuration)
        
    send_message = SendMessage(configuration['script_path'])
    
    file = os.path.split(args.source_path)[1]
    send_message.to_log_bot('INFO', f'Descargado: {file}')
    
    args.source_path = args.source_path.replace('\\', '/')
    args.category = args.category.lower()
    
    #upload_to_backup_drive(configuration['rclone_path'], args.source_path, configuration['remote_backup'], 'Subidas', args.category, file)
    t = threading.Thread(target=upload_to_backup_drive, args=(configuration['rclone_path'], configuration['script_path'], args.source_path, configuration['remote_backup'], 'Subidas', args.category, file,))
    t.start()
    
    if 'seeding' in args.category.lower():
        return
    
    series = False
    if 'series' in args.category.lower():
        series = True
        season_episode = get_season_episode_number(file)
          
    tmp_path, file_name = check_extension(source_path=args.source_path, script_path=configuration['script_path'], category=args.category, file=file, series=series)
    
    send_message.to_log_bot('INFO', f'Inicio scrapping [{file}]')
    
    if series:
        file_name = refactor_series(tmp_path=tmp_path, file_name=file_name, file=file)
        tmp_path, folder_name, resolution, poster_path, plot, imdb_rating, imdb_id = scrap_series(script_path=configuration['script_path'], tmp_path=tmp_path, file_name=file_name, file=file)    
    else:
        tmp_path, folder_name, resolution, poster_path, plot, tagline, imdb_rating, imdb_id = scrap_movies(script_path=configuration['script_path'], category=configuration['naming_conventions'][args.category], tmp_path=tmp_path, file_name=file_name, file=file)
        
    send_message.to_log_bot('INFO', f'Archivo scrapeado [{file}]')
    
    upload_to_drive(rclone_path=configuration['rclone_path'], script_path = configuration['script_path'], tmp_path=tmp_path, remote_name=configuration['equivalences_tags_remote'][args.category], remote_folder=configuration['remote_folders'][args.category], folder_name=folder_name, file=file)
    
    if series:
        send_message.to_telegram_channel(tmp_path=tmp_path, folder_name=f'{folder_name} {season_episode}', resolution=resolution, poster_path=poster_path, plot=plot, imdb_rating=imdb_rating, imdb_id=imdb_id)

    else:
        send_message.to_telegram_channel(tmp_path=tmp_path, folder_name=folder_name, resolution=resolution, poster_path=poster_path, plot=plot, imdb_rating=imdb_rating, imdb_id=imdb_id)
    
    send_message.to_log_bot('INFO', f'Inicio housekeeping [{file}]')
    shutil.rmtree('/'.join(tmp_path.replace('?', '').split('/')[:-1]))
    send_message.to_log_bot('INFO', f'Housekeeping, archivo borrado de carpeta temporal [{file}]')



if __name__ == "__main__":
    parser = argparse.ArgumentParser(description = "Movies automanagement script")
    parser.add_argument("-p", "--source_path", help = "Path of the download", required=True)
    parser.add_argument("-c", "--category", help = "Torrent category", required=True)

    args = parser.parse_args()
    main(args)
