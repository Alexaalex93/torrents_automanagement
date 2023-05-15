# -*- coding: utf-8 -*-
"""
Created on Wed May 10 22:29:59 2023

@author: alexf
"""

import inspect
import logging


class FunctionNameLoggerAdapter(logging.LoggerAdapter):
    def process(self, msg, kwargs):
        return '%s - %s: %s' % (self.extra['unique_id'], inspect.stack()[2][3], msg), kwargs
