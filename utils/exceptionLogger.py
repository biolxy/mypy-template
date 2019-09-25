#!/usr/bin/env python
# -*- coding: utf-8 -*-
u"""
File Name   : exception_logger.py .

Author      : biolxy
E-mail      : biolxy@aliyun.com
Created Time: 2019-08-16 15:45:47
version     : 1.0
Function    : The author is too lazy to write nothing
Usage       :
"""
import functools
import logging
import os
import sys
import shlex
import subprocess
import time


def color_term(string, color='blue', bold=True):
    u"""Linux客户端彩色输出，适配py2，py3."""
    colors = {
        'grey': '\033[0;30m',
        'red': '\033[0;31m',
        'green': '\033[0;32m',
        'yellow': '\033[0;33m',
        'blue': '\033[0;34m',
        'megenta': '\033[0;35m',
        'cyan': '\033[0;36m',
        'white': '\033[0;37m',
        'bold': '\033[1m',
        'end': '\033[0m'
    }
    color_format = colors[color].replace('[0', '[1') if bold else colors[color]
    return color_format + str(string) + colors['end']
    # print(color_term("{}".format(var), 'red'))


def create_logger(log_name, log_file, log_level=logging.INFO):
    """
    Creates a logging object and returns it
    """
    logger = logging.getLogger(log_name)
    logger.setLevel(log_level)

    # create the logging file handler
    fh = logging.FileHandler(log_file)

    fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    formatter = logging.Formatter(fmt)
    fh.setFormatter(formatter)

    # add handler to logger object
    logger.addHandler(fh)
    return logger


def exception(logger):
    """
    A decorator that wraps the passed in function and logs
    exceptions should one occur

    @param logger: The logging object
    """

    # https://segmentfault.com/a/1190000005728587
    def decorator(func):
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except:
                # log the exception
                err = "There was an exception in  "
                err += func.__name__
                logger.exception(err)

            # re-raise the exception
            raise

        return wrapper

    return decorator


# """
# example:
# # 先创建一个logger
# logger = create_logger('xiao2',
#                        '/home/Account/lixy/RNAseq_pipeline/biolxyUtil/log')

# # 装饰函数
# @exception(logger)
# def zero_divide():
#     1 / 0

# @exception(logger)
# def echo():
#     os.system("for i in $(seq 1 9);do echo $i;done")
# """

#  https://www.e-learn.cn/en/node/2355753
# https://www.cnblogs.com/txw1958/archive/2011/10/21/2220636.html


def echo():
    os.system("for i in $(seq 1 10);do echo $i ;done")


def err():
    os.system("xxx")


def execute_cmd(cmd):
    print(color_term("Run command:\n{}".format(cmd), color='cyan', bold=False))
    p = subprocess.Popen(shlex.split(cmd),
                         stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE,
                         shell=True)
    while p.poll() is None:
        line = p.stdout.readline()
        line = line.strip()
        if line:
            print('Subprogram output: [{}]'.format(line))
    if p.returncode == 0:
        print(color_term('Run command success', color='blue'))
    else:
        print(color_term('Run command failed', color='red'))

if __name__ == '__main__':
    zero_divide()
    echo()

    dir_output = "/home/Account/lixy/RNAseq_pipeline/biolxyUtil"

    log_file = os.path.join(dir_output, 't1.log')
    logger = create_logger('测试1', log_file, log_level=logging.INFO)
