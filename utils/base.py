#!/usr/bin/env python
# -*- coding: utf-8 -*-
u"""
File Name   : biolxyUtil.py .

Author      : biolxy
E-mail      : biolxy@aliyun.com
Created Time: 2018-07-24 13:34:17
version     : 1.0
Function    : 用来提供一些基础功能，例如linux客户端彩色输出，记录日志，安全shell命令等
"""
import shlex
import logging
import subprocess
from collections import Counter
import time
import sys
import os
import re


class MagicDict(dict):
    u"""
    Mdict = MagicDict()
    Mdict[a][b] = c

    Mdict = MagicDict(dict1)  # 转化一个dict为MagicDict
    """
    def __getitem__(self, item):
        try:
            return dict.__getitem__(self, item)
        except KeyError:
            value = self[item] = type(self)()
            return value


class Timer(object):
    # u"""计时器.
    # 仅仅适用python3
    # 参见：
    # https://python3-cookbook.readthedocs.io/zh_CN/latest/c13/p13_making_stopwatch_timer.html
    # python3 的话可以让 func=time.perf_counter ，能获得更高的时间精度
    # """
    def __init__(self, func=time.time):
        self.elapsed = 0.0
        self._func = func
        self._start = None

    def start(self):
        if self._start is not None:
            raise RuntimeError('Already started')
        self._start = self._func()

    def stop(self):
        if self._start is None:
            raise RuntimeError('Not started')
        end = self._func()
        self.elapsed += end - self._start
        self._start = None

    def reset(self):
        self.elapsed = 0.0

    @property
    def running(self):
        return self._start is not None

    def __enter__(self):
        self.start()
        return self

    def __exit__(self, *args):
        self.stop()


class progressPrintStr(object):
    def __init__(self,
                 inputStr,
                 func=time.time,
                 func2=time.localtime,
                 func3=time.strftime):
        self.elapsed = 0.0
        self._func = func
        self._func2 = func2
        self._func3 = func3
        self._start = None
        self.inputStr = inputStr

    def start(self):
        if self._start is not None:
            raise RuntimeError('Already started')
        self._start = self._func()
        self._startstr1 = self._func3('%Y-%m-%d %H:%M:%S',
                                      self._func2(self._start))
        self._startstr2 = "   [ {} is begin at time: {} ]   ".format(
            self.inputStr, self._startstr1)
        self._startline = len(self._startstr2) * "="
        print(color_term(self._startline, "green", True))
        print(color_term(self._startstr2, "green", True))
        print(color_term(self._startline, "green", True))

    def stop(self):
        if self._start is None:
            raise RuntimeError('Not started')
        self._end = self._func()
        self.elapsed += self._end - self._start
        self.elapsedMinutes = int(self.elapsed / 60)
        self.elapsedSeconds = self.elapsed % 60
        self._start = None
        self._endstr1 = self._func3('%Y-%m-%d %H:%M:%S',
                                    self._func2(self._end))
        self._endstr2 = "   [ {} is end at time: {}, {} min {:.2f} s has elapsed ]   ".format(
            self.inputStr, self._endstr1, self.elapsedMinutes,
            self.elapsedSeconds)
        self._endline = len(self._endstr2) * "="
        print(color_term(self._endline, "green", True))
        print(color_term(self._endstr2, "green", True))
        print(color_term(self._endline, "green", True))

    def reset(self):
        self.elapsed = 0.0

    @property
    def running(self):
        return self._start is not None

    def __enter__(self):
        self.start()
        return self

    def __exit__(self, *args):
        self.stop()


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


def execute_cmd(cmd):
    start_time = time.time()
    start_time2 = time.strftime('[ %Y-%m-%d %H:%M:%S ]',
                                time.localtime(start_time))
    print(color_term("{} run command:\n{}".format(
        start_time2, cmd),
                     'cyan',
                     bold=False))
    p = subprocess.Popen(shlex.split(cmd),
                         stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE)

    while True:
        output = p.stdout.readline()
        if output == '' and p.poll() is not None:
            break
        if output:
            print(color_term(output.strip(), 'white', False))

    error = p.stderr.read()
    if error:
        raise Exception(error)


def execute_cmd2(cmd):
    returnNum = 1
    start_time = time.time()
    start_time2 = time.strftime('[%Y-%m-%d %H:%M:%S ]',
                                time.localtime(start_time))
    print(color_term("{} run command:\n{}".format(
        start_time2, cmd),
                     'cyan',
                     bold=False))
    returnStstus = True
    try:
        returnNum = os.system(cmd)
    except Exception as e:
        returnStstus = False
        raise Exception(color_term(e, 'red'))
    if returnNum != 1:
        returnNum = returnNum >> 8
    return returnNum


def execute_cmd3(cmd, printStstus=True):
    u"""Change sys.system(),提供安全的shell输入端口，为以后web键入命令提供基础,适配py2, py3.

    execute_cmd 中可以直接嵌套 linux命令，同样可以嵌套类似 python script.py inputfile 等命令
    通常用法为 execute_cmd("mkinputDir {}".format())
    该函数调用 color_term 函数
    """
    # https://python3-cookbook.readthedocs.io/zh_CN/latest/c13/p06_executing_external_command_and_get_its_output.html
    start_time = time.time()
    start_time2 = time.strftime('[ %Y-%m-%d %H:%M:%S ]',
                                time.localtime(start_time))
    print(color_term("{} Command will be execute in a subshell:\n{}".format(
        start_time2, cmd),
                     'cyan',
                     bold=False))
    returnNum = 1
    try:
        p = subprocess.Popen(shlex.split(cmd),
                             stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE)
        # To interpret as text, decode
        while True:
            output = p.stdout.readline()
            if output == '' and p.poll() is not None:
                break
            if output:
                if printStstus:
                    print(color_term(output.strip(), 'white', False))
        p.wait()
        returnNum = int(p.returncode)
        if returnNum != 0:
            print(color_term("This command returnNum is {}".format(returnNum),
                             'red'))
        return returnNum
    except BaseException as e:
        raise BaseException(color_term(e, 'red'))
    finally:
        return returnNum


def diff_multiple_list(list_list):
    u"""
    对多个数组求交集，并集
    """
    listall = []
    for listi in list_list:
        listall += listi
    # Intersection
    list_A = []
    dictlist = Counter(listall)
    numof_list = len(list_list)
    for i in dictlist:
        if dictlist[i] == numof_list:
            list_A.append(i)
    # Union
    list_B = list(set(listall))
    return list_A, list_B


def get_real_path(pathfile):
    if os.path.islink(pathfile):
        pathfile = os.readlink(pathfile)
    pathfile = os.path.abspath(pathfile)
    return pathfile


def getFile(inputDir, inputStr):
    list1 = []
    if os.path.isdir(inputDir):
        for relpath, dirs, files in os.walk(inputDir):
            for item in files:
                if re.search(inputStr, item):
                    full_path = os.path.join(inputDir, relpath, item)
                    str1 = os.path.normpath(os.path.abspath(full_path))
                    print(str1)
                    list1.append(str1)
    else:
        print("{} is not a dir".format(inputDir))
    return list1


def progressBar(number, time1):
    """ 和 StreamToLogger 不能共用 """
    time1 = float(time1)
    number = int(number)
    sys.stdout.write("wait ==>>>")
    for i in range(number):
        # 进度条类型
        sys.stdout.write("\b\b\b=>>>")
        sys.stdout.flush()
        time.sleep(time1)
    sys.stdout.write("\n")
    sys.stdout.flush()


def progressBar2(number, time1):
    time1 = float(time1)
    number = int(number) + 1
    for i in range(number):
        sys.stdout.write('   \r')
        sys.stdout.flush()
        sys.stdout.write('{}%\r'.format(i))
        sys.stdout.flush()
        time.sleep(time1)


def getColumnNamesNum(infile):
    """
    input infile, get a dict (key is cloumnName , value is the cloumn number )
    """
    linelist = []
    dict1 = {}
    with open(infile) as ff:
        for line in ff:
            line = line.rstrip()
            linelist = line.split("\t")
            break
    for x, columnName in enumerate(linelist):
        dict1[columnName] = x
    return dict1


def mkdirf(indir):
    if not os.path.isdir(indir):
        os.mkdir(indir)
    return None


def getrepoHead(indir):
    # from git import repo
    # repo = git.Repo.init(path='.')
    # /home/Account/lixy/RNAseq_pipeline/.git/refs/heads
    headsfile = os.path.join(indir, '.git', 'refs', 'heads', 'master')
    with open(headsfile, 'r') as ff:
        heads = ff.read()
        heads = heads.strip()
    return heads