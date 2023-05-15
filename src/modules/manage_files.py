# -*- coding: utf-8 -*-
"""
Created on Thu Jul 29 10:12:38 2021

@author: alexf
"""

import os

def upload_to_drive(folder_to_upload_path, destination_folder_name, rclone_path, remote_name, logger):


    logger.info( f'Rclone execution command: {rclone_path} copy \"{folder_to_upload_path}\" --ignore-existing \"{remote_name}:/{destination_folder_name}\"')

    os.system(f'{rclone_path} copy \"{folder_to_upload_path}\" --ignore-existing \"{remote_name}:/{destination_folder_name}\"')
