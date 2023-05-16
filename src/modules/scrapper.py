# -*- coding: utf-8 -*-
"""
Created on Sat Jul 31 15:18:36 2021

@author: alexf
"""

import os
import glob
import shutil
import re
import requests
from docker import DockerClient

def get_docker_volume_path(container_name, target_path):

    client = DockerClient(base_url='unix://var/run/docker.sock')
    volumes = client.containers.get(container_name).attrs['Mounts']

    for volume in volumes:
        if volume['Destination'] == target_path:
            return volume['Source']

    raise Exception(f'No se pudo encontrar el volumen mapeado a {target_path}.')

def get_container_name():
    # Leemos el contenido de /proc/self/cgroup
    with open('/proc/self/cgroup', 'r') as cgroup_file:
        cgroup_content = cgroup_file.read()

    # Usamos una expresión regular para extraer el ID del contenedor
    container_id = re.search(r'/docker/([\da-f]{64})', cgroup_content)
    if container_id is None:
        raise Exception('No se pudo obtener el ID del contenedor Docker.')
    container_id = container_id.group(1)

    # Hacemos una solicitud a la API de Docker para obtener el nombre del contenedor
    try:
        response = requests.get(f'http://localhost:2375/containers/{container_id}/json')
        response.raise_for_status()
    except requests.exceptions.RequestException as err:
        raise Exception(f'Error al hacer la solicitud a la API de Docker: {err}')

    # Devolvemos el nombre del contenedor
    container_info = response.json()
    return container_info['Name'][1:]  # [1:] se utiliza para eliminar la barra inicial

def scrap(hash_folder_path, hash_folder, posters_folder_path, tmm_configuration_path, category, logger):

    if 'series' in category:
        tmm_command = 'tvshow'
    else:
        tmm_command = 'movie'

    file_type = category.split('_')[-1].lower()

    container_name = get_container_name()

    download_path  = get_docker_volume_path(container_name, '/downloads')

    last_two_folders = os.path.join(*hash_folder_path.split(os.sep)[-2:])

    realworld_download_path = os.path.join(download_path,  last_two_folders)

    logger.debug(f'Docker command: docker run --rm -e CONTENT_TYPE="{tmm_command}" -v {realworld_download_path}:/{file_type} -v {tmm_configuration_path}:/tinyMediaManager/data alexaalex93/tinymediamanager_cli_ubuntu')

    os.system(f'docker run --rm -e CONTENT_TYPE="{tmm_command}" -v {hash_folder_path}:/{file_type} -v {tmm_configuration_path}:/tinyMediaManager/data alexaalex93/tinymediamanager_cli_ubuntu')

    if glob.glob(f'{hash_folder_path}/*/*poster*'):
        path = glob.glob(f'{hash_folder_path}/*/*poster*')[0]
        extension = os.path.splitext(path)[1]
        shutil.copy(path, f'{posters_folder_path}/{hash_folder}{extension}')

        return  f'{posters_folder_path}/{hash_folder}{extension}'

    return None
