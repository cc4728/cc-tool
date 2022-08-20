#!/usr/bin/python3
# -*- coding: utf-8 -*-
import os
import os.path
import sys
import time
import re
import parse_config



#logcat config
TXT_REPORT_FILE = "scan_logcat_filter.txt"
LOGCAT_FILE = ""
START_TAG = ""
END_TAG = ""
RESULT_TAG = ""
BT_ADDR_FORMATE = ""  # xx:xx:xx:xx:xx:xx
LOGCAT_DATE_FORMATE = "" #02-06 22:27:39.405
DEVICE_NAME = ""

RES_LIST = []

def init_parameter():
    global LOGCAT_FILE,START_TAG,END_TAG,RESULT_TAG,DEVICE_NAME,\
            LOGCAT_DATE_FORMATE,BT_ADDR_FORMATE

    _,LOGCAT_FILE =parse_config.get_logcat_file()
    _,START_TAG = parse_config.get_scan_start_tag()
    _,END_TAG = parse_config.get_scan_end_tag()
    _,RESULT_TAG = parse_config.get_scan_result_tag()
    _,DEVICE_NAME = parse_config.get_scan_device_name()
    _,LOGCAT_DATE_FORMATE = parse_config.get_logcat_date_formate()
    _,BT_ADDR_FORMATE = parse_config.get_bt_addr_formate()


# read file by line , ingore read error
def parse(file):
    global RES_LIST
    global LOGCAT_FILE,START_TAG,END_TAG,RESULT_TAG,DEVICE_NAME,\
            LOGCAT_DATE_FORMATE,BT_ADDR_FORMATE
    data = ""
    with open(file, 'rb') as f:
        line = f.readline().decode('utf-8', 'ignore')
        while line:
            tmp = re.compile(LOGCAT_DATE_FORMATE).search(line)
            if tmp:
                data = tmp[0]
            if START_TAG in line:
                line = "".join('{}Start Discover').format(data.ljust(22))
                RES_LIST.append(line)
            elif END_TAG in line :
                line = "".join('{}Stop Discover\n').format(data.ljust(22))
                RES_LIST.append(line)
            elif RESULT_TAG in line:
                t_name =  re.compile(DEVICE_NAME).search(line)
                if t_name:
                    name = t_name[0][7:-1]
                    line = "".join('{}Found dev-name:{}').format(data.ljust(22),name)
                    RES_LIST.append(line)
                t_addr =  re.compile(BT_ADDR_FORMATE).search(line)
                if t_addr :
                    addr = t_addr[0]
                    line = "".join('{}Found dev-address:{}').format(data.ljust(22),addr)
                    RES_LIST.append(line)
            else:
                pass
            line = f.readline().decode('utf-8', 'ignore')
    print("Get {} line in logcat".format(len(RES_LIST)))
    print("Parse logcat scan done")
    return RES_LIST

if __name__ == '__main__':

    if os.path.exists(TXT_REPORT_FILE):
        os.remove(TXT_REPORT_FILE)
        print("Remove old scan txt file")
    init_parameter()
    if not os.path.exists(LOGCAT_FILE):
        print("Logcat not exists ! Exit after 3s")
        time.sleep(3)
        exit(0)
    if parse(LOGCAT_FILE):
         with open(TXT_REPORT_FILE, 'w') as f:
            for i in RES_LIST:
                line = i+'\n'
                f.write(line)