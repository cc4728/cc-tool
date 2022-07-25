#!/usr/bin/python

import os
import os.path
import sys
import platform
import struct
import time
import random
import subprocess
import msvcrt
import shutil
import threading
import datetime
from get_8518_bt_log_once import pull_log_files,parse_stack_conf,get_other_logs,run_adb
#import ConfigParser

"""
This device ID only used in this special project
Here must be end with a space
adb_device=" "
"""
ADB_DEVICE= "-s 0123456789ABCDEF "
LOG_LOCAL_PATH = ""
LOG_DUT_DEFAULT_PATH = "/data/misc/bluetooth/logs/"

def getInput( timeout = 5):
	start_time = time.time()
	input = ''
	while True:
		if msvcrt.kbhit():
			input = msvcrt.getche()
		if len(input) != 0 or (time.time() - start_time) > timeout:
			break
	if len(input) > 0:
		return (input)
	else:
		return ('\0')

if __name__ == '__main__':
	print ("wait adb devices ...")
	os.system("adb wait-for-device")
	print ("adb devices connected")

	LOG_LOCAL_PATH = os.path.join(os.getcwd(), "yocto_bt_log_" + time.strftime("%Y%m%d_%H%M%S", time.localtime(time.time())))

	#print ("2.perform cmd before pull")
	cmd = r"python cmd_before_pull.py " + ADB_DEVICE
	os.system(cmd)

	#print ("3.reset platform timestamps")
	run_adb("shell date -s \"" + time.strftime("%Y/%m/%d", time.localtime(time.time())) + "\"")
	run_adb("shell date -s \"" + time.strftime("%H:%M:%S", time.localtime(time.time())) + "\"")

	if os.path.exists(LOG_LOCAL_PATH) == False:
		print ("Create " + LOG_LOCAL_PATH)
		os.makedirs(LOG_LOCAL_PATH)
		os.makedirs(os.path.join(LOG_LOCAL_PATH, "bluetooth"))

	#print ("5.get bt_stack.conf")
	if os.path.exists(LOG_LOCAL_PATH + "/bt_stack.conf") == False:
		run_adb(" pull /data/misc/bluedroid/bt_stack.conf " + LOG_LOCAL_PATH)
		run_adb(" pull /data/misc/bluedroid/bt_config.conf " + LOG_LOCAL_PATH)
		run_adb(" pull /data/misc/bluedroid/bt_did.conf " + LOG_LOCAL_PATH)

	hci_log_path,stack_log_path,picus_log_path =parse_stack_conf(LOG_LOCAL_PATH)

	while 1:
		run_adb("shell sync")
		pull_log_files(os.path.join(LOG_LOCAL_PATH, "bluetooth"),hci_log_path,stack_log_path,picus_log_path)
		print ("[S]top, [C]ontinue, To continue after 20s @" + time.strftime("%H:%M:%S",time.localtime(time.time())))
		input_char = getInput(20)
		print(input_char)
		# print "input_char" + input_char
		if "s" in input_char or "S" in input_char:
			break

	print ("Get All Log")
	#cmd = r"python get_8518_bt_log_once.py " + LOG_LOCAL_PATH + " " + ADB_DEVICE
	#os.system(cmd)
	get_other_logs(LOG_LOCAL_PATH)

	#start merge hci
	hci_log_local_path = LOG_LOCAL_PATH + "\\bluetooth\\logs\\bthci\\"
	#print (hci_log_local_path)
	if os.path.exists(hci_log_local_path):
		tmp_list = os.listdir(hci_log_local_path)
		for doc in tmp_list:
			doc = hci_log_local_path+doc+"\\"
			print (doc,os.path.isdir(doc))
			if os.path.isdir(doc):
				print (doc)
				cmd = r"python merge_hci.py " + doc
				os.system(cmd)
	else:
		print("not found hci log doc")
	print ("merge hci log finish")
	raw_input('pull success, any key quit')
