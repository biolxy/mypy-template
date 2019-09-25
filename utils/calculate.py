#!/usr/bin/env python
# -*- coding: utf-8 -*-
u"""
File Name   : calculate.py .

Author      : biolxy
E-mail      : biolxy@aliyun.com
Created Time: 2019-08-23 18:49:59
version     : 1.0
Function    : The author is too lazy to write nothing
Usage       :
"""
import sys
import os
import numpy as np
from scipy import stats


def pearsonr_ci(x, y, alpha=0.05):
    with np.errstate(divide='ignore'):
        r, p = stats.pearsonr(x, y)
        r_z = np.arctanh(r)
        se = 1 / np.sqrt(x.size - 3)
        z = stats.norm.ppf(1 - alpha / 2)
        lo_z, hi_z = r_z - z * se, r_z + z * se
        lo, hi = np.tanh((lo_z, hi_z))
    return r, p, lo, hi

