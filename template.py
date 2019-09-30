#!/usr/bin/env python
# -*- coding: utf-8 -*-
u"""
File Name   : template.py .

Author      : biolxy
E-mail      : biolxy@aliyun.com
Created Time: 2019-09-29 21:32:16
version     : 1.0
Function    : The author is too lazy to write nothing
Usage       :
"""
import os, sys
import re
import time
import argparse
from configparser import ConfigParser

__VERSION__ = 'v1.0'


def mkoutdir(indir):
    if not os.path.isdir(indir):
        os.mkdir(indir)


def main():
    # start pipelien

    if re.search('fp', runoptions):
        mkoutdir("{outputDir}/1.fastq-out".format(outputDir=outputDir))
        returnNum = execute_cmd2(
            "python {path_py}/Fastp.py -i {rawdata} -o {outputDir}/1.fastq-out"
            .format(path_py=SCRIPT_FOLDER, rawdata=inputDir, outputDir=outputDir))
        if returnNum != 0:
            print(color_term("error, program interruption", "red"))
            sys.exit()

    # end
    echo.stop()


if __name__ == '__main__':
    try:
        SCRIPT_FOLDER = os.path.abspath(os.path.dirname(__file__))
        parser = argparse.ArgumentParser(
            prog="RNAseq".format(__VERSION__),
            description=
            "This is a pipeline of sino-TA-RNA, developed by yeh and biolxy \
            in sinomics company, with all rights reserved.")
        parser.add_argument(
            '-i',
            '--inputfile',
            type=str,
            help="input file",
            required=True,
            metavar='')
        parser.add_argument('-o',
                            '--outputdir',
                            type=str,
                            help="specify output directory",
                            required=True,
                            metavar='')
        parser.add_argument('-r',
                            '--runoptions',
                            type=str,
                            help="Specifies the program to run",
                            default='fpstarmkresm',
                            metavar='')
        # cfg = ConfigParser()
        # configfile = os.path.join(path_py, "config.ini")
        # cfg.read(configfile)  # python3
        # gene_annotation = cfg.get('GRCh37', 'gene_annotation')
        args = parser.parse_args()
        inputDir = os.path.abspath(args.inputdir)
        outputDir = os.path.abspath(args.outputdir)
        runoptions = args.runoptions
        main()
    except KeyboardInterrupt:
        pass
    except IOError as e:
        raise
