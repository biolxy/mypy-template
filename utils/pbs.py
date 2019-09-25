#!/usr/bin/env python
# -*- coding: utf-8 -*-
u"""
File Name   : pbs.py .

Author      : biolxy
E-mail      : biolxy@aliyun.com
Created Time: 2019-07-24 17:42:52
version     : 1.0
Function    : The author is too lazy to write nothing
Usage       :
"""
import subprocess
import shlex
import sys
import os
import pysnooper
import time
from base import MagicDict, progressBar, color_term
# import json


def qsub_command(incommand, NamePrefix, Namesuffix, outFolder, cpuCore,
                 batch='batch'):
    # command = "qsub -N {NamePrefix}_{Namesuffix} -o \
    #     {outFolder}/{NamePrefix}_{Namesuffix}.log -l nodes=1:ppn={cpuCore} \
    #     -q {batch} <<< \"{command}\"".format(NamePrefix=NamePrefix,
    #                                        outFolder=outFolder,
    #                                        command=incommand,
    #                                        Namesuffix=Namesuffix,
    #                                        batch=batch,
    #                                        cpuCore=cpuCore)
    jobName = NamePrefix + "_" + Namesuffix
    cmdscript = os.path.join(outFolder, jobName + ".sh")
    with open(cmdscript, 'w') as ff:
        ff.write("#!/bin/sh\n")
        ff.write("#PBS -N {}\n".format(jobName))
        ff.write("#PBS -l nodes=1:ppn={}\n".format(cpuCore))
        # ff.write("#PBS -q {}\n".format(batch))
        ff.write("#PBS -o {}/{}.log\n".format(outFolder, jobName))
        ff.write("#PBS -j oe\n")
        ff.write(incommand)
        ff.write("\n")
        ff.write('wait\n')
    command = "qsub -V {cmdscript}".format(jobName=jobName,
                                       outFolder=outFolder,
                                       command=incommand,
                                       batch=batch,
                                       cmdscript=cmdscript,
                                       cpuCore=cpuCore)
    command = " ".join(command.split())
    return command


def submit_cmd(cmd):
    p = subprocess.Popen(shlex.split(cmd),
                         stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE)
    p.wait()
    stdo = p.stdout.read()
    stdo = stdo.strip()
    stde = p.stderr.read()
    exit_status = int(p.returncode)
    print(exit_status, stdo, stde)
    if exit_status == 0:
        print(color_term("submit successed, {}".format(stdo), "green", False))
    else:
        print(color_term("failed, {}".format(stde),"red"))
    return exit_status, stdo, stde


def submit_cmd2(cmd):
    jobid = os.popen(cmd)
    return jobid


def submit_cmdList(cmdList):
    """ 
    此处python2 3 不兼容，type(b) 在2中是 str, 3中是 bytes
    """
    jobid_list = []
    if len(cmdList) != 0:
        firstCmd = cmdList[0]
        a,b,c = submit_cmd(firstCmd)
        jobid_list.append(b)
        for cmd in cmdList[1:]:
            cmd = shlex.split(cmd)
            cmd1, cmd2 = cmd[:-1], cmd[-1]
            cmd = "  ".join(cmd1) + " -W depend=afterok:" + b + " " + cmd2
            print("submit cmd: {}".format(cmd))
            a,b,c = submit_cmd(cmd)
            time.sleep(1)
            jobid_list.append(b)
    else:
        print("error, cmdList is empty!")
    return jobid_list


def get_dependStr(inafterList):
    depend = ""
    if inafterList == []:
        depend = ""
    else:
        depend = " -W depend=afterok"
        for i in inafterList:
            depend += ":" + i
    return depend

# def submit_cmdList2(cmdList, afterList = []):
#     jobid_list = []
#     afterList2 = afterList
#     depend = get_dependStr(afterList)

#     if len(cmdList) != 0:
#         for cmd in cmdList:
#             if afterList == []:
#                 firstCmd = cmdList[0]
#                 a,b,c = submit_cmd(firstCmd)
#                 print("submit cmd: {}".format(cmd))
#                 afterList2.append(b)
#                 jobid_list.append(b)
#             else:
#                 cmd = shlex.split(cmd)
#                 cmd1, cmd2 = cmd[:-1], cmd[-1]
#                 depend = " -W depend=afterok:"
#                 for i in afterList2:
#                     depend += ":" + i
#                 depend = depend.rstrip(":")
#                 cmd = "  ".join(cmd1) + depend + " " + cmd2
#                 a,b,c = submit_cmd(cmd)
#                 print("submit cmd: {}".format(cmd))
#                 afterList2.append(b)
#                 time.sleep(1)
#                 jobid_list.append(b)
#     else:
#         print("error, cmdList is empty!")
#     return jobid_list


def submit_cmdList3(cmdList, afterList = [], resubmitN=3):
    jobid_list = []
    afterList2 = afterList
    if len(cmdList) != 0:
        for cmd in cmdList:
            cmd = shlex.split(cmd)
            cmd1, cmd2 = cmd[:-1], cmd[-1]
            depend = get_dependStr(afterList2)
            cmd = "  ".join(cmd1) + depend + " " + cmd2
            print("submit cmd: {}".format(cmd))
            a,b,c = submit_cmd(cmd)
            while resubmitN >= 0 and a != 0:
                print(color_term("Resubmit cmd: {}".format(cmd), "yellow"))
                a,b,c = submit_cmd(cmd)
                resubmitN -= 1
            afterList2.append(b)
            time.sleep(1)
            jobid_list.append(b)
    else:
        print("error, cmdList is empty!")
    return jobid_list

# @pysnooper.snoop()
def get_task_status(taskid):
    aa = qstatfParse()
    info = os.popen("qstat -f")
    aa.getinfo(info.read())
    dict1 = aa.dict
    status = "None"
    if taskid in dict1:
        status = dict1[taskid]['job_state']
    return status


def get_taskList_status(taskidList):
    list1 = []
    for taskid in taskidList:
        list1.append(get_task_status(taskid))
    return list1


class qstatfParse(object):
    def __init__(self):
        self.msg = ""
        self.list = []
        self.dict = MagicDict()

    def getinfo(self, info):
        list1 = []
        self.info = info
        joblist = info.split("\n\n")
        joblist.pop(-1)
        for jobinfo in joblist:
            jobinfolist = jobinfo.split("\n    ")
            str1 = jobinfolist[21].replace("\n\t", "")
            jobinfolist_sub = str1.split(",")
            jobinfolist.pop(21)
            jobinfolist.extend(jobinfolist_sub)
            jobinfolist = [x.replace(" = ", "=") for x in jobinfolist]
            list1.append(jobinfolist)
        self.list = list1
        self.dict = self.infodict()

    # @pysnooper.snoop()
    def infodict(self):
        dict1 = MagicDict()
        for i in self.list:
            tmplist = i
            key = tmplist[0].split(": ")[-1]
            for value in tmplist[1:]:
                valueN = value.split("=")[0]
                valueV = value.split("=")[-1]
                dict1[key][valueN] = valueV
        return dict1






# def dict2str(indict):
#     str1 = json.dumps(indict, sort_keys=True, indent=4, separators=(',', ':'))
#     return str1

if __name__ == '__main__':
    cwd = '/home/Account/lixy/tmp/test'
    # qsub -N test -o /home/Account/lixy/tmp/test/log -l nodes=1:ppn=1 -q batch <<< 'bash /home/Account/lixy/tmp/test/aa.sh '
    command = "bash /home/Account/lixy/tmp/test/aa.sh"
    qsub_cmd = qsub_command(command, "test", "script",
                            "/home/Account/lixy/tmp/test",
                            1,
                            batch='batch')

    print(qsub_cmd)
    cmdList = []
    for i in range(5):
        cmdList.append(qsub_cmd)


    print(cmdList)
    tasklist = submit_cmdList3(cmdList)
    print(tasklist)
    print("start")
    listS = list(set(get_taskList_status(tasklist)))
    while listS != ["None"]:
        listS = list(set(get_taskList_status(tasklist)))
        print("=== {} ===".format(listS))
        progressBar(10, 2)

    print("end")
    sys.exit()
    # with open("/home/Account/lixy/RNAseq_pipeline/pbs/qstatf.txt", 'r') as ff:
    #     b = ff.read()
    # hhh =   qstatfParse()
    # hhh.getinfo(b)
    # print(dict2str(hhh.dict))

    statu, stdo, stde = submit_cmd(qsub_cmd)
    stdo = stdo.rstrip("\n")  # (0, '59349.mu01', '')
    print(statu, stdo, stde)
    if statu == 0:
        print("submit is OK")
    if stde:
        print(stde)

    info = submit_cmd("qstat -f")
    aa = qstatfParse()
    aa.getinfo(info[1])
    dict1 = aa.dict
    if stdo in dict1:
        print(dict1[stdo])
    else:
        # print(dict2str(dict1))
        print(dict1)
