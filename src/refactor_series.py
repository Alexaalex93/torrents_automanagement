# -*- coding: utf-8 -*-
"""
Created on Fri Sep 17 12:45:00 2021

@author: AlexPC
"""

import os
import re
import shutil 

def refactor_series(**kwargs):
    
    if os.path.isdir(f'{kwargs["tmp_path"]}/{kwargs["file_name"]}'):
        folder_name = re.sub('(?i)s\d{1,2}.*\[.*\]', '', kwargs["file_name"]).strip()
        os.rename(f'{kwargs["tmp_path"]}/{kwargs["file_name"]}', f'{kwargs["tmp_path"]}/{folder_name}')
        return folder_name
    else:
        print(kwargs["file_name"])
        file = os.path.splitext(kwargs["file_name"])[0]
        print(file)
        folder_name =  re.sub('(?i)s\d{1,2}e\d{1,2}.*\[.*\]', '', file).strip()
        print(folder_name)
        os.mkdir(f'{kwargs["tmp_path"]}/{folder_name}')
        shutil.move(f'{kwargs["tmp_path"]}/{kwargs["file_name"]}',  f'{kwargs["tmp_path"]}/{folder_name}')
        return folder_name

