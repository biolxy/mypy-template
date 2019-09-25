#!/usr/bin/env python
# -*- coding: utf-8 -*-
u"""
File Name   : Slog.py .

Author      : biolxy
E-mail      : biolxy@aliyun.com
Created Time: 2019-08-19 09:45:56
version     : 1.0
Function    : The author is too lazy to write nothing
Usage       :
"""
import os
import re
import sys
import time
import logging
from .base import color_term


class StreamToLogger(object):
    u"""
    Fake file-like stream object that reinputDirects writes to a logger instance.

    记录log日志，适配py3
    Refer: [ReinputDirect stdout and stderr to a logger in Python]
           (https://www.electricmonk.nl/log/2011/08/14/reinputDirect-stdout-and-stderr-to-a-logger-in-python/)
           [How to reinputDirect stdout and stderr to logger in Python]
           (https://stackoverflow.com/questions/19425736/how-to-reinputDirect-stdout-and-stderr-to-logger-in-python)
    """
    def __init__(self, logger, log_level=logging.INFO):
        self.logger = logger
        self.log_level = log_level
        self.linebuf = ''

    def write(self, buf):
        for line in buf.rstrip().splitlines():
            self.logger.log(self.log_level, line.rstrip())


class FileHandlerFormatter(logging.Formatter):
    """
    格式化log文件中的彩色输出为普通输出
    """
    def format(self, record):
        msg = super(FileHandlerFormatter, self).format(record)
        return re.sub('\\033\[[0-8;]+m', '', msg)


class SetupLogger(object):
    def __init__(
            self,
            log_name,
            path_log=None,
            level=logging.INFO,
            on_file=True,
            on_stream=True,
            log_mode='a',
            format_fh='%(asctime)s | %(filename)s - line:%(lineno)-4d | %(levelname)s | %(message)s',
            format_sh='[%(levelname)s] %(message)s',
            format_date='[%Y-%m-%d %H:%M:%S]'):
        self.log_name = log_name
        self.path_log = path_log
        self.level = level
        self.on_file = on_file
        self.on_stream = on_stream
        self.log_mode = log_mode
        self.format_fh = format_fh
        self.format_sh = format_sh
        self.format_date = format_date
        self.logger = logging.getLogger(log_name)
        self.logger.setLevel(level)
        self.add_filehandler()
        self.add_streamhandler()

    def add_filehandler(self):
        if self.on_file:
            if self.path_log:  # handle log directory
                dir_name = os.path.dirname(self.path_log)
                if not os.path.exists(dir_name):
                    print color_term(
                        "[WARNING] directory of log doesn't exist, create it!",
                        'yellow')
                    os.makedirs(dir_name)

            file_handler = logging.FileHandler(self.path_log,
                                               mode=self.log_mode)
            file_handler.setFormatter(
                FileHandlerFormatter(self.format_fh, self.format_date))
            self.logger.addHandler(file_handler)

    def add_streamhandler(self):
        if self.on_stream:
            stream_handler = logging.StreamHandler()
            stream_handler.setFormatter(logging.Formatter(self.format_sh))
            self.logger.addHandler(stream_handler)


def main():
    reN = execute_cmd2(
        "bashaa /home/Account/lixy/RNAseq_pipeline/biolxyUtil/aa.sh")
    print("command retuen num is {}:".format(reN))


if __name__ == '__main__':
    dir_output = '/home/Account/lixy/RNAseq_pipeline/biolxyUtil'
    SetupLogger('log',
                os.path.join(dir_output, 'aa.log'),
                log_mode='w',
                format_sh='%(message)s',
                format_fh='[%(levelname)s] %(asctime)s %(message)s')
    logger = logging.getLogger('log')

    sys.stdout = StreamToLogger(logger, logging.INFO)
    sys.stderr = StreamToLogger(logger, logging.ERROR)
    print("============> 1")
    main()
    print("============> 2")