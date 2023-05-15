# -*- coding: utf-8 -*-
"""
Created on Sun May  7 18:28:34 2023

@author: alexf
"""

import time
import hashlib
import os


def create_unique_id(original_file_name):

    timestamp = int(time.time())
    original_file_name = original_file_name.replace(' ', '_')
    unique_id = f"{original_file_name}_{timestamp}"

    return unique_id



def create_hash_folder(tmp_path, file):
    hash_folder = hashlib.md5(file.encode('utf-8')).hexdigest()
    hash_folder_path = os.path.join(tmp_path, hash_folder)

    return hash_folder_path, hash_folder
