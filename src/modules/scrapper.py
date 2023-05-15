# -*- coding: utf-8 -*-
"""
Created on Sat Jul 31 15:18:36 2021

@author: alexf
"""

import os
import glob
import shutil


def scrap(hash_folder_path, hash_folder, posters_folder_path, tmm_configuration_path, category, logger):


    if 'series' in category:
        tmm_command = 'tvshow'
    else:
        tmm_command = 'movie'

    file_type = category.split('_')[-1].lower()

    logger.debug(f'Docker command: docker run --rm -e CONTENT_TYPE="{tmm_command}" -v {hash_folder_path}:/{file_type} -v {tmm_configuration_path}:/tinyMediaManager/data alexaalex93/tinymediamanager_cli_ubuntu')

    os.system(f'docker run --rm -e CONTENT_TYPE="{tmm_command}" -v {hash_folder_path}:/{file_type} -v {tmm_configuration_path}:/tinyMediaManager/data alexaalex93/tinymediamanager_cli_ubuntu')

    if glob.glob(f'{hash_folder_path}/*/*poster*'):
        path = glob.glob(f'{hash_folder_path}/*/*poster*')[0]
        extension = os.path.splitext(path)[1]
        shutil.copy(path, f'{posters_folder_path}/{hash_folder}{extension}')

        return  f'{posters_folder_path}/{hash_folder}{extension}'

    return None
