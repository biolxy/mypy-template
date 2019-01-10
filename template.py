#!/usr/bin/env python
# -*- coding: utf-8 -*-
u"""
File Name   : aa.py .

Author      : biolxy
E-mail      : biolxy@aliyun.com
Created Time: 2018-09-17 12:10:33
version     : 1.0
Function    : The is a template.
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
    stepName = "fastp"
    equalSignNumber = 60
    start_time = time.time()
    start_time2 = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(start_time/1000))
    print(color_term("{}".format("=" * equalSignNumber)))
    print(color_term("[{} in start in time: {}]".format(stepName , start_time2)))
    print(color_term("{}".format("=" * equalSignNumber)))
    # start pipelien
    
    # end
    end_time = time.time()
    end_time2 = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(end_time/1000))
    ran_time = (end_time - start_time) / 60
    print(color_term("{}".format("=" * equalSignNumber)))
    print(color_term("[{} in end in time: {}, elapsed {:.1f} min]".format( stepName, end_time2, ran_time)))
    print(color_term("{}".format("=" * equalSignNumber)))


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
