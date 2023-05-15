# -*- coding: utf-8 -*-
"""
Created on Sun May  7 18:40:37 2023

@author: alexf
"""

def log_message(logger, unique_id, message, level='info'):

    log_extra = {'unique_id': unique_id}

    if level == 'debug':
        logger.debug(message, extra=log_extra)
    elif level == 'info':
        logger.info(message, extra=log_extra)
    elif level == 'warning':
        logger.warning(message, extra=log_extra)
    elif level == 'error':
        logger.error(message, extra=log_extra)
    elif level == 'critical':
        logger.critical(message, extra=log_extra)
    else:
        raise ValueError(f'Nivel de log desconocido: {level}')
