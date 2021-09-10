# -*- coding: utf-8 -*-
"""
Created on Wed Jul 28 11:29:17 2021

@author: alexf
"""

from convert_to_iso import check_extension
from manage_files import upload_to_drive, upload_to_backup_drive
from scrapper import scrap_movies
from send_message import SendMessage

import argparse
import json
import os
import shutil

def main(args):
    if 'Series' in args.source_path or 'Seeding' in args.source_path:
        return
    send_message = SendMessage()
    send_message.to_log_bot('INFO', f'Torrent descargado {args.source_path}')
    with open('../configuration/configuration.json') as configuration_file:
        configuration = configuration_file.read().replace('\\', '/')
        configuration = json.loads(configuration)

    args.source_path = args.source_path.replace('\\', '/')
    upload_to_backup_drive(rclone_path=configuration['rclone_path'], source_path=args.source_path, remote_name=configuration['remote_backup'], remote_folder='Subidas', category=args.category)
    send_message.to_log_bot('INFO', 'Archivo subido a team backup')

    tmp_path, file_name = check_extension(source_path=args.source_path, category=args.category)

    tmp_path, folder_name, resolution, poster_path, plot, tagline = scrap_movies(category=configuration['naming_conventions'][args.category], tmp_path=tmp_path, file_name=os.path.split(args.source_path)[1])
    send_message.to_log_bot('INFO', 'Archivo scrapeado')

    upload_to_drive(rclone_path=configuration['rclone_path'], tmp_path=tmp_path, remote_name=configuration['equivalences_tags_remote'][args.category], remote_folder=configuration['remote_folders'][args.category], folder_name=folder_name)
    send_message.to_log_bot('INFO', 'Archivo subido a team definitivo')

    send_message.to_telegram_channel(tmp_path=tmp_path, folder_name=folder_name, resolution=resolution, poster_path=poster_path, plot=plot, tagline=tagline)
    shutil.rmtree(tmp_path)
    send_message.to_log_bot('INFO', 'Housekeeping, archivo borrado de carpeta temporal')



if __name__ == "__main__":
    parser = argparse.ArgumentParser(description = "Movies automanagement script")
    parser.add_argument("-p", "--source_path", help = "Path of the download", required=True)
    parser.add_argument("-c", "--category", help = "Torrent category", required=True)

    args = parser.parse_args()
    main(args)