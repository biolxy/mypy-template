#!/usr/bin/env python
# -*- coding: utf-8 -*-
u"""
File Name   : Standard.py .

Author      : biolxy
E-mail      : biolxy@aliyun.com
Created Time: 2018-07-24 13:53:32
version     : 1.0
Function    : This is a test.
"""
from util.base import color_term
from util.base import execute_cmd
from util.base import StreamToLogger
import os
import re
import time
import argparse

__VERSION__ = 'v1.0'



def main():
    u"""主要的函数流程."""
    start_time = time.time()
    for i in os.listdir(input_dir):
        if re.match("_muts.txt", i):
            file1 = os.path.join(input_dir, i)
    print(file1)
    print(color_term("main function execute time: {}s".format(
        round(time.time() - start_time, 2))
        ))


if __name__ == '__main__':
    try:
        parser = argparse.ArgumentParser(
            prog="Standard".format(__VERSION__),
            description="This is a RNAseq_pipeline."
        )
        # formatter_class=argparse.RawTextHelpFormatter,
        # https://docs.python.org/3/library/argparse.html
        # https://docs.python.org/2/howto/argparse.html
        # https://codeday.me/bug/20171209/105070.html
        # group = parser.add_mutually_exclusive_group()
        # group.add_argument()  # 该方法用来添加单选的参数，如 -l | -f 二选一
        parser.add_argument(
            '-i',
            '--inputdir',
            type=str,
            help="Input dir for fastq file.",
            metavar='')
        # 指定参数的形式，一般写两个，一个短参数，一个长参数
        parser.add_argument(
            '-o',
            '--outputdir',
            type=str,
            help="Specify output directory",
            metavar='')
        args = parser.parse_args()
        input_dir = os.path.abspath(args.inputdir)
        output_dir = os.path.abspath(args.outputdir)
        main()
    except KeyboardInterrupt:
        pass
    except IOError as e:
        raise
