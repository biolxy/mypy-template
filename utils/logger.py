#!/usr/bin/env python
# -*- coding: utf-8 -*-
u"""
File Name   : logger.py .

Author      : biolxy
E-mail      : biolxy@aliyun.com
Created Time: 2020-06-23 13:18:40
version     : 1.0
Function    : The author is too lazy to write nothing
Usage       :
"""
import os
from getpass import getuser
from socket import gethostbyname, gethostname
import time
import logging
from logging import handlers
from colorlog import ColoredFormatter



# import copy
# class ColoredConsoleHandler(logging.StreamHandler):
#     """
#     ref: https://kb.kutu66.com/others/post_188583
#     """
#     def emit(self, record):
#         # Need to make a actual copy of the record
#         # to prevent altering the message for other loggers
#         myrecord = copy.copy(record)
#         levelno = myrecord.levelno
#         if(levelno >= 50): # CRITICAL/FATAL
#             color = 'x1b[31m' # red
#         elif(levelno >= 40): # ERROR
#             color = 'x1b[31m' # red
#         elif(levelno >= 30): # WARNING
#             color = 'x1b[33m' # yellow
#         elif(levelno >= 20): # INFO
#             color = 'x1b[32m' # green
#         elif(levelno >= 10): # DEBUG
#             color = 'x1b[35m' # pink
#         else: # NOTSET and anything else
#             color = 'x1b[0m' # normal
#         myrecord.msg = color + str(myrecord.msg) + 'x1b[0m' # normal
#         logging.StreamHandler.emit(self, myrecord)


class ContextFilter(logging.Filter):
    """
    https://www.cnblogs.com/yyds/p/6897964.html
    使用Filters引入上下文信息
    """
    ip = 'IP'
    username = 'USER'
    def filter(self, record):
        record.ip = self.ip
        record.username = self.username
        return True


class Logger(object):
    level_relations = {
        'debug':logging.DEBUG,
        'info':logging.INFO,
        'warning':logging.WARNING,
        'error':logging.ERROR,
        'crit':logging.CRITICAL
    } #日志级别关系映射

    def __init__(self,filename,level='info',when='D',backCount=3,fmt='%(log_color)s[ %(asctime)s ] - %(ip)s - %(username)s - %(funcName)s - %(levelname)s: %(message)s'):
        # fmt='%(log_color)s[ %(asctime)s ] - %(ip)s - %(username)s - %(pathname)s[line:%(lineno)d] - %(levelname)s: %(message)s')
        self.logger = logging.getLogger(filename)
        format_str = logging.Formatter(fmt)                     #设置日志格式
        self.logger.setLevel(self.level_relations.get(level))   #设置日志级别
        sh = logging.StreamHandler()                            #往屏幕上输出

        ###
        # ref: https://pypi.org/project/colorlog/2.2.0/
        format_str = ColoredFormatter(
            fmt,
            datefmt=None,
            reset=True,
            log_colors={
                    'DEBUG':    'cyan',
                    'INFO':     'green',
                    'WARNING':  'yellow',
                    'ERROR':    'red',
                    'CRITICAL': 'red',
                }
        )
        sh.setFormatter(format_str)  #设置屏幕上显示的格式
        th = handlers.TimedRotatingFileHandler(filename=filename,when=when,backupCount=backCount,encoding='utf-8')#往文件里写入#指定间隔时间自动生成文件的处理器
        #实例化TimedRotatingFileHandler
        #interval是时间间隔，backupCount是备份文件的个数，如果超过这个个数，就会自动删除，when是间隔的时间单位，单位有以下几种：
        # S 秒
        # M 分
        # H 小时、
        # D 天、
        # W 每星期（interval==0时代表星期一）
        # midnight 每天凌晨
        filter = ContextFilter()
        self.logger.addFilter(filter)
        filter.username, filter.ip = get_username_ip()
        th.setFormatter(format_str)#设置文件里写入的格式
        self.logger.addHandler(sh) #把对象加到logger里
        self.logger.addHandler(th)


def getLogFile(indir, logName):
    start_time = time.time()
    start_time2 = time.strftime('%y%m%d', time.localtime(start_time))
    filename = os.path.join(indir, logName + "_" + start_time2 + ".log")
    return filename


def get_username_ip():
    # import os, pwd
    # return pwd.getpwuid(os.getuid())[0]
    # import getpass
    hostname = gethostname()
    ip = gethostbyname(hostname)
    username = getuser()
    return username, ip

if __name__ == '__main__':
    SCRIPT_FOLDER = os.path.abspath(os.path.dirname(__file__))
    logfile = getLogFile(SCRIPT_FOLDER, "Thisalogforpy")
    log = Logger(logfile,level='debug')
    log.logger.debug('debug')
    log.logger.info('info')
    log.logger.warning('警告')
    log.logger.error('报错')
    log.logger.critical('严重')
    Logger('error.log', level='error').logger.error('error')