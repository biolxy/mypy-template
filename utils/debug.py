#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   debug.py
@Author  :   biolxy 
@E-mail  :   biolxy@aliyun.com
@Time    :   2021/04/28 13:01:45
@Version :   1.0
@Desc    :   None
@Usage   :   None
@Ref     :   http://blog.oneapm.com/apm-tech/700.html
'''
import time
from functools import wraps
import cProfile
from line_profiler import LineProfiler  # @profile


def timethis(func):
    """
    简单
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        r = func(*args, **kwargs)
        end = time.perf_counter()
        print('{}.{} : {}'.format(func.__module__, func.__name__, end - start))
        return r
    return wrapper


def do_cprofile(func):
    """
    中等
    """ 
    def profiled_func(*args, **kwargs):
        profile = cProfile.Profile()        
        try:
            profile.enable()
            result = func(*args, **kwargs)
            profile.disable()            
            return result        
        finally:
            profile.print_stats()    
        return profiled_func

      
def do_profile(func):
    """
    复杂
    """ 
    def profiled_func(*args, **kwargs):
        try:
            profiler = LineProfiler()
            profiler.add_function(func)
            profiler.enable_by_count()
            return func(*args, **kwargs)
        finally:
            profiler.print_stats()
    return profiled_func