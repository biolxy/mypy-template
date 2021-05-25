#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   configParserUper.py
@Author  :   biolxy 
@E-mail  :   biolxy@aliyun.com
@Time    :   2021/03/17 17:27:57
@Version :   1.0
@Desc    :   None
@Usage   :   None
'''
from configparser import ConfigParser

class ConfigParserUper(ConfigParser):
    """
    继承ConfigParser，修改其optionxform, 使其支持大小写
    """
    def optionxform(self, optionstr):
        return optionstr