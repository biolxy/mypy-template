#!/usr/bin/env python
# -*- coding: utf-8 -*-
u"""
File Name   : logger.py .

Author      : biolxy
E-mail      : biolxy@aliyun.com
Created Time: 2018-07-24 12:54:58
version     : 1.0
Function    : This script used to record the log of main script
"""
import os
import logging
import logging.handlers


def init_logger(log_file):
    u"""A script used to record the log of main script."""
    dir_path = os.path.dirname(log_file)
    try:
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)
    except Exception as error:
        pass

    handler = logging.handlers.RotatingFileHandler(
        log_file,
        maxBytes=20 * 1024 * 1024,
        backupCount=10
        )
    fmt = '%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s'
    formatter = logging.Formatter(fmt)
    handler.setFormatter(formatter)
    logger_instance = logging.getLogger('logs')
    logger_instance.addHandler(handler)
    logger_instance.setLevel(logging.DEBUG)
    return logger_instance
mylog = init_logger('./result.log')
mylog.info('')
