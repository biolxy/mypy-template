#!/usr/bin/env python
# -*- coding: utf-8 -*-
u"""
File Name   : writeJson.py .

Author      : biolxy
E-mail      : biolxy@aliyun.com
Created Time: 2020-04-03 18:01:35
version     : 1.0
Function    : The author is too lazy to write nothing
Usage       :
"""
from __future__ import unicode_literals
import codecs
import json
import numpy as np


class NpEncoder(json.JSONEncoder):
    """
    FIX BUG in json.dumps:
    TypeError: Object of type 'int64' is not JSON serializable
    """
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        elif isinstance(obj, np.floating):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        else:
            return super(NpEncoder, self).default(obj)


def writeJson(inputdict, outputfile):
    # https://blog.csdn.net/u014431852/article/details/53058951
    fp = codecs.open(outputfile, 'w', 'utf-8')
    fp.write(json.dumps(inputdict, sort_keys=True, indent=4, ensure_ascii=False, cls=NpEncoder))
    fp.close()


if __name__ == "__main__":
    pass