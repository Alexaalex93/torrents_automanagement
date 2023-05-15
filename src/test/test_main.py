# -*- coding: utf-8 -*-
"""
Created on Sun May  7 13:59:07 2023

@author: alexf
"""

import pytest
from modules.rename_and_move import rename_and_move
from modules.scrapper import scrap
from modules.manage_files import upload_to_drive

# Casos de prueba para la función rename_and_move
rename_and_move_test_cases = [
    {
        "input": {
            "tracker": "hd-olimpo",
            "source_path": "/path/to/source1",
            "script_path": "/path/to/script1",
            "tmp_path": "/path/to/tmp1",
            "original_file_name": "example_file_name1",
            "category": "movies_fhd",
        },
        "expected_output": "expected_result1"
    },
    # Agregar más casos de prueba aquí
]

# Casos de prueba para la función scrap
scrap_test_cases = [
    {
        "input": {
            "tmp_path_posters": "/path/to/tmp_path_posters",
            "hash_folder": "hash_folder1",
            "category": "movies_fhd",
            "tmp_path": "/path/to/tmp1",
            "configuration_tmm_path": "/path/to/configuration_tmm_path",
        },
        "expected_output": "expected_result1"
    },
    # Agregar más casos de prueba aquí
]

# Casos de prueba para la función upload_to_drive
upload_to_drive_test_cases = [
    {
        "input": {
            "rclone_path": "/path/to/rclone_path",
            "script_path": "/path/to/script_path",
            "tmp_path": "/path/to/tmp1",
            "remote_name": "movies_fhd",
            "folder_name": "folder_name1",
            "original_file_name": "example_file_name1",
        },
        "expected_output": "expected_result1"
    },
    # Agregar más casos de prueba aquí
]

# Pruebas unitarias para rename_and_move
@pytest.mark.parametrize("test_case", rename_and_move_test_cases)
def test_rename_and_move(test_case):
    result = rename_and_move(**test_case["input"])
    assert result == test_case["expected_output"]

# Pruebas unitarias para scrap
@pytest.mark.parametrize("test_case", scrap_test_cases)
def test_scrap(test_case):
    result = scrap(**test_case["input"])
    assert result == test_case["expected_output"]

# Pruebas unitarias para upload_to_drive
@pytest.mark.parametrize("test_case", upload_to_drive_test_cases)
def test_upload_to_drive(test_case):
    result = upload_to_drive(**test_case["input"])
    assert result == test_case["expected_output"]
