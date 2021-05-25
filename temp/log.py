#!/usr/bin/env python
# -*- coding: utf-8 -*-
u"""
File Name   : log.py .

Author      : biolxy
E-mail      : biolxy@aliyun.com
Created Time: 2020-06-23 13:12:43
version     : 1.0
Function    : The author is too lazy to write nothing
Usage       :
"""
import time
import os

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


def getLogFile(indir, logName):
    start_time = time.time()
    start_time2 = time.strftime('%y%m%d', time.localtime(start_time))
    filename = os.path.join(indir, logName + start_time2 + ".txt")
    return filename


def logPrint(logfile, info):
    start_time = time.time()
    start_time2 = time.strftime('[ %Y-%m-%d %H:%M:%S ]',
                                time.localtime(start_time))
    OUT = open(logfile, 'a+')
    print(color_term("{} {}".format(start_time2, info), 'green', bold=False))
    OUT.write("{} {}\n".format(start_time2, info))
    OUT.close()


if __name__ == "__main__":
    # loginfo -- info for which you want print
    # logPrint(logfile, loginfo)