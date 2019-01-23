#!/usr/bin/env python
# -*- coding: utf-8 -*-
u"""
File Name   : template.py .

Author      : biolxy
E-mail      : biolxy@aliyun.com
Created Time: 2018-09-17 12:10:33
version     : 1.0
Function    : The is a template.
"""
from util.base import color_term
from util.base import execute_cmd
from util.base import StreamToLogger, 
import os
import re
import time
import argparse
from configparser import ConfigParser
# https://python3-cookbook.readthedocs.io/zh_CN/latest/c13/p10_read_configuration_files.html

__VERSION__ = 'v1.0'


def main():
    stepName = "fastp"

    # start pipelien

    # end
    end_time = time.time()
    end_time2 = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(end_time))
    ran_time = (end_time - start_time) / 60
    print(color_term("{}".format("=" * equalSignNumber)))
    print(color_term("[{} in end in time: {}, elapsed {:.1f} min]".format(
        stepName, end_time2, ran_time)))
    print(color_term("{}".format("=" * equalSignNumber)))


if __name__ == '__main__':
    try:
        parser = argparse.ArgumentParser(
            prog="template".format(__VERSION__),
            description="This is a pipeline of XX."
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
        cfg = ConfigParser()
        path_py = os.path.abspath(os.path.dirname(__file__))
        configfile = os.path.join(path_py, "config.ini")
        cfg.read(configfile)   # python3
        gene_annotation = cfg.get('GRCh37', 'gene_annotation')
        fasta_file = cfg.get('GRCh37', 'fasta_file')
        args = parser.parse_args()
        input_dir = os.path.abspath(args.inputdir)
        output_dir = os.path.abspath(args.outputdir)
        main()
    except KeyboardInterrupt:
        pass
    except IOError as e:
        raise
