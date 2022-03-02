#!/usr/bin/python3
# -*- coding: utf-8 -*-
import os
import os.path
import sys
import time
import re

# regular expression config

#logcat config
LOGCAT_FILE = ["logcat.log","logcat.txt","logcat","KernelBuffer.txt"]
CRASH_TAG = "beginning of crash"
DRIVER_TAG = "btmtk"

#ring buffer
Ptr = 0
Buffer_Size = 20
Buffer = []

#save report
REPORT_FILE = "crash_analysis_report.txt"

def get_all_file(filepath, list, key=None):
    if not os.path.exists(filepath):
        print("file not exist")
        return
    if os.path.isfile(filepath):
        if not key:
            list.append(filepath)
        else:
            if '\\' in filepath:
                names = filepath.split('\\')
                if key in names[-1:]:
                    list.append(filepath)
            else:
                if key in filepath:
                    list.append(filepath)
        return

    files = os.listdir(filepath)
    for fi in files:
        fi_d = os.path.join(filepath, fi)
        if os.path.isdir(fi_d):
            get_all_file(fi_d, list,key)
        else:
            file = os.path.join(filepath, fi_d)
            if not key :
                list.append(file)
            else:
                names = file.split('\\')
                if key in names[-1:]:
                    list.append(file)


def add2ring(line):
    global Buffer
    global Ptr
    global Buffer_Size
    if Ptr > 2*Buffer_Size-1:
        Ptr = 0
        Buffer.clear()
    #print("Ring_prt:", Ring_prt)
    Buffer.append(line)
    Ptr += 1

#only get data before index
def get2ring(num):
    global Buffer
    global Ptr
    global Buffer_Size
    if num > Buffer_Size:
        return None
    return Buffer[(Ptr - num):Ptr]

# read file by line , ingore read error
def process_logcat(file):
    list = []
    After_num = 0
    with open(file, 'rb') as f:
        line = f.readline().decode('utf-8', 'ignore')
        while line:
            line = line.strip('\n')
            add2ring(line)
            if After_num:
                list.append(line)
                After_num -= 1
            elif CRASH_TAG in line:
                list += get2ring(5)
                After_num = 10
            elif DRIVER_TAG in line :
               list.append(line)
            else:
                pass
            line = f.readline().decode('utf-8', 'ignore')
    if list:
        line = "Finish_Process: " + file + '\n'
        list.append(line)

    for i in list:
        print(i)
    return list

if __name__ == '__main__':
    logcat_list = []
    logcat_list_res = []
    print("Start crash_analysis.py")
    if len (sys.argv) > 1 and sys.argv[1]:
        print ("Now open =>", sys.argv[1])
        path = sys.argv[1]
        for key in LOGCAT_FILE:
            get_all_file(path, logcat_list, key)
    else:
        print("Please input file path, and retry")

#    print(logcat_list)
    for file in logcat_list:
        logcat_list_res += process_logcat(file)

    if logcat_list_res:
         with open(REPORT_FILE, 'w') as f:
            for i in logcat_list_res:
                line = i+'\n'
                f.write(line)

    del logcat_list_res
    del logcat_list
    print("Fininsh crash_analysis.py")
    print("auto close 3s later......")
    time.sleep(3)
