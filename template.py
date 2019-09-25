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
from utils.base import color_term, getFile
from utils.base import execute_cmd2, execute_cmd2
from utils.base import StreamToLogger
from utils.base import progressPrintStr
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
    stepName = "RNAseq"
    echo = progressPrintStr(stepName)
    echo.start()
    # start pipelien

    if re.search('fp', runoptions):
        mkoutdir("{outputDir}/1.fastq-out".format(outputDir=outputDir))
        returnNum = execute_cmd2(
            "python {path_py}/Fastp.py -i {rawdata} -o {outputDir}/1.fastq-out"
            .format(path_py=path_py, rawdata=inputDir, outputDir=outputDir))
        if returnNum != 0:
            print(color_term("error, program interruption", "red"))
            sys.exit()

    # end
    echo.stop()


if __name__ == '__main__':
    try:
        cfg = ConfigParser()
        path_py = os.path.abspath(os.path.dirname(__file__))
        configfile = os.path.join(path_py, "config.ini")
        cfg.read(configfile)  # python3
        parser = argparse.ArgumentParser(
            prog="RNAseq".format(__VERSION__),
            description=
            "This is a pipeline of sino-TA-RNA, developed by yeh and biolxy \
            in sinomics company, with all rights reserved.")
        parser.add_argument(
            '-i',
            '--inputdir',
            type=str,
            help=
            "input dir for raw fastq dir, 'normal' or 'tumor' should be present in fastq file name,\
            and suffix should in {}.".format(fastqsuffixList),
            metavar='')
        parser.add_argument('-o',
                            '--outputdir',
                            type=str,
                            help="specify output directory",
                            metavar='')
        parser.add_argument(
            '-r',
            '--runoptions',
            type=str,
            help="Specifies the program to run",
            default='fpstarmkresmcganovelsplitmutecthlafusionsomaticaffinity')

        gene_annotation = cfg.get('GRCh37', 'gene_annotation')
        fasta_file = cfg.get('GRCh37', 'fasta_file')
        args = parser.parse_args()
        inputDir = os.path.abspath(args.inputdir)
        outputDir = os.path.abspath(args.outputdir)
        runoptions = args.runoptions
        main()
    except KeyboardInterrupt:
        pass
    except IOError as e:
        raise
