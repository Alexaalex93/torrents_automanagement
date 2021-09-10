# -*- coding: utf-8 -*-
"""
Created on Thu Jul 29 10:12:38 2021

@author: alexf
"""

import os

def upload_to_backup_drive(**kwargs):
    os.system(f'{kwargs["rclone_path"]} copy \"{kwargs["source_path"]}\" \"{kwargs["remote_name"]}:{kwargs["remote_folder"]}/{kwargs["category"]}\"')

def upload_to_drive(**kwargs):
    os.system(f'{kwargs["rclone_path"]} copy \"{kwargs["tmp_path"]}\" \"{kwargs["remote_name"]}:{kwargs["remote_folder"]}/{kwargs["folder_name"]}\"')