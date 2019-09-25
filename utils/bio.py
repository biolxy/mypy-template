#!/usr/bin/env python
# -*- coding: utf-8 -*-
u"""
File Name   : bio.py .

Author      : biolxy
E-mail      : biolxy@aliyun.com
Created Time: 2018-07-24 13:34:17
version     : 1.0
Function    : 用来提供一些基础功能，例如linux客户端彩色输出，记录日志，安全shell命令等
"""
from Bio import SeqIO


def create_bam_index(pathbam):
    pathbambai = pathbam + ".bai"
    if not os.path.exists(pathbambai):
        try:
            cmd = "sambamba index {}".format(pathbam)
            execute_cmd
        except Exception as e:
            raise Exception(color_term(e, 'red'))


def getFastaSeq(inlist, infastq, outfastaName):
    def writeFasta(inSeq, outfastaName):
        SeqIO.write(inSeq, outfastaName, "fasta")

    sequences = []
    for record in SeqIO.parse(infastq, "fasta"):
        ids = record.id
        ids = ids.split(".")[0]
        if ids in inlist:
            sequences.append(record)
    writeFasta(sequences, outfastaName)
