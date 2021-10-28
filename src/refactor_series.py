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
        folder_name = re.sub('(?i)((?!(\(\d+\)))\(miniserie(.+?)?\)|\[(.+?)]|s\d+(e\d+)?)', '', kwargs["file_name"]).strip()
        os.rename(f'{kwargs["tmp_path"]}/{kwargs["file_name"]}', f'{kwargs["tmp_path"]}/{folder_name}')
        return folder_name
    else:

        file = os.path.splitext(kwargs["file_name"])[0]
        folder_name = re.sub('(?i)((?!(\(\d+\)))\(miniserie(.+?)?\)|\[(.+?)]|s\d+(e\d+)?)', '', file).strip()
        os.mkdir(f'{kwargs["tmp_path"]}/{folder_name}')
        shutil.move(f'{kwargs["tmp_path"]}/{kwargs["file_name"]}',  f'{kwargs["tmp_path"]}/{folder_name}')
        return folder_name