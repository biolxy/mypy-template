#!/usr/bin/env python
# -*- coding: utf-8 -*-
u"""
File Name   : writePatientInfo.py .

Author      : biolxy
E-mail      : biolxy@aliyun.com
Created Time: 2020-02-28 19:20:46
version     : 1.0
Function    : The author is too lazy to write nothing
Usage       :
"""
# ref: https://github.com/elapouya/python-docx-template
#      https://docxtpl.readthedocs.io/en/latest/
#      https://blog.csdn.net/qcyfred/article/details/79925099
# ref: https://python-docx.readthedocs.io/en/latest/index.html#
# ref: https://blog.csdn.net/meteor_cheng/article/details/88582426

# from docx import Document
# from docx.shared import Inches
from docxtpl import DocxTemplate
from docxtpl import InlineImage
from docx.shared import Mm
from docxtpl import RichText
import copy


def writePatientInfo(Templatewordfile, output_word, patientDict):
    doc = DocxTemplate(Templatewordfile)
    # word 模板中的替换字符串为 {{ name }}
    # patientDict = { 'name' : u'张三' }
    # print(patientDict)
    doc.render(patientDict)
    doc.save(output_word)


class reportWord(object):
    def __init__(self, Templatewordfile, output_word, patientDict):
        self.Templatewordfile = Templatewordfile
        self.output_word = output_word
        self.patientDict = patientDict
        self.dict2 = copy.deepcopy(patientDict)
        self.doc = DocxTemplate(self.Templatewordfile)
        self.__insert_image()

    # def changepatientDict(self, changedDict):
    #     self.patientDict = changedDict

    def writePatientInfo(self):
        # self.doc.render(self.dict2)
        self.doc.render(self.dict2, autoescape=True)

    def __insert_image(self):
        if 'HRD_rank_plot' in self.patientDict:
            HRD_rank_plot = self.patientDict['HRD_rank_plot']
            self.dict2['HRD_rank_plot'] = InlineImage(self.doc, HRD_rank_plot, width=Mm(100))

        if 'figurePath' in self.patientDict['TMB']:
            figurePath = self.patientDict['TMB']['figurePath']
            self.dict2['TMB']['figurePath'] = InlineImage(self.doc, figurePath, width=Mm(100))
        # self.doc.render(self.patientDict, autoescape=True)
        self.__rich()
        self.doc.render(self.dict2, autoescape=True)

    def saveWord(self):
        self.doc.save(self.output_word)

    def __rich(self):
        inlist = ['Clinical_trial', 'FDA', 'mutation_res']
        self.dict2 = rRich(self.dict2)
        self.dict2.make_rich("medication_associated_l", inlist)
        inlist2 = ['targeted_drug_indications', 'common_name', 'trade_name']
        self.dict2.make_rich("Indication_table", inlist2)
        # pprint(self.dict2)


class rRich(dict):
    # def __init__(self):
    #     self.inlist = ['Clinical_trial', 'FDA', 'mutation_res']
    def make_rich(self, k, inlist):
        """
        recursion: replace value = y if value == x
        """

        if k in self:
            value = self[k]
            if isinstance(value, list):
                for item in value:
                    for item2 in item:
                        # print(item2)
                        if item2 in inlist:
                            item[item2] = RichText(item[item2])
                            # print(item[item2])
                    """
                    {
                            "gene_anno": "/",
                            "gene_drug": "/",
                            "gene_interpretations": "/",
                            "gene_relation": "/",
                            "gene_title": "HIST1H3G;NM_003534.2:exon1:c.266C>T(p.A89V);错义突变"
                    }
                    """   

    # def make_rich(self, inlist):
    #     """
    #     recursion: replace value = y if value == x
    #     """

    #     if "medication_associated_l" in self:
    #         value = self["medication_associated_l"]
    #         if isinstance(value, list):
    #             for item in value:
    #                 for item2 in item:
    #                     # print(item2)
    #                     if item2 in inlist:
    #                         item[item2] = RichText(item[item2])
    #                         # print(item[item2])
    #                 """
    #                 {
    #                         "gene_anno": "/",
    #                         "gene_drug": "/",
    #                         "gene_interpretations": "/",
    #                         "gene_relation": "/",
    #                         "gene_title": "HIST1H3G;NM_003534.2:exon1:c.266C>T(p.A89V);错义突变"
    #                 }
    #                 """
