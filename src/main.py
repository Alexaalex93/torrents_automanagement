# -*- coding: utf-8 -*-
"""
Created on Wed Jul 28 11:29:17 2021

@author: alexf
"""

'''
###PASOS

###1 comprobar que tipo de torrent es(Esto viene dado por el tag puesto en el cliente) si es fullbd o fulluhd.
######1.1 Lanzar aviso en canal de logs
######1.2 Si es full comprobar si es iso o no
######1.3 Lanzar aviso en canal de logs
#########1.3.1 Si no es iso, convertir a iso y borrar la carpeta
#########1.3.2 Lanzar aviso en canal de logs


###2 Si no scrapea mover a otra carpeta y hacerlo manualmente (Hacerlo mediante telegram??)
######2.1 Lanzar aviso en canal de logs


###1 Subir torrents a drive subidas para tener una copia tal cual se necesita
######1.1 Lanzar aviso en canal de logs

###2 Subir torrents a drive temp para poder modificarlo a nuestro antojo
###2.2 Lanzar aviso en canal de logs


###4 Scrapear pelicula
######4.1 Lanzar aviso en canal de logs

###6 Una vez scrapeado comprobar en su team de destino si existe, si existe, sobreescribir, si no, mover
######6.1 Lanzar aviso en canal de logs

###7 Lanzar aviso en canal de novedades
'''

'''
###ESTRUCTURA

#Meter al main localizacion del rclone

main.py ---> orquestrador, une con diferentes modulos, subir torrents, lanzar mensajes, scrapping
    |
    |
    ---- upload_files.py ---> sube los archivos usando rclone al drive que indiquemos en el archivo de configuracion
    |
    |
    ---- send_messages.py ---> Reutilizar hehco en scripting
    |
    |
    ---- scrap.py ---> scrapea el archivo subido a temp drive
    |
    |
    ---- move_files.py ---> Usar rclone o api de google

    '''


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
    arm_tag = ''
    if configuration['arm']:
        arm_tag = '_arm'
    args.source_path = args.source_path.replace('\\', '/')
    upload_to_backup_drive(rclone_path=configuration['rclone_path'], source_path=args.source_path, remote_name=configuration['remote_backup'], remote_folder='Subidas', category=args.category)
    send_message.to_log_bot('INFO', 'Archivo subido a team backup')

    tmp_path, file_name = check_extension(source_path=args.source_path, category=args.category)

    tmp_path, folder_name, resolution, poster_path, plot, tagline = scrap_movies(arm=arm_tag, category=configuration['naming_conventions'][args.category], tmp_path=tmp_path, file_name=os.path.split(args.source_path)[1])
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