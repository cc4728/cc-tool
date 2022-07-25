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
#import ConfigParser

ADB_DEVICE= "-s 0123456789ABCDEF "
LOG_LOCAL_PATH = ""
LOG_DUT_DEFAULT_PATH = "/data/misc/bluetooth/logs/"

#print sys.argv
def run_adb(command):
	adb_command_debug = True
	cmd = "adb "+ADB_DEVICE+command
	if adb_command_debug:
		print('[' + cmd + ']')
	return os.popen(cmd).read()

def pull_log_files(dst_log_path, hci_log_path,stack_log_path=None,picus_log_path=None):
	if not dst_log_path or not hci_log_path:
		return

	hci_log_path = os.path.dirname(hci_log_path)
	stack_log_path = os.path.dirname(stack_log_path)
	print("Get hci log:",hci_log_path)
	print("Get stack log:", stack_log_path)
	print("Get picus log:", picus_log_path)

	run_adb("pull "+hci_log_path+ " "+dst_log_path)

	if (stack_log_path != hci_log_path and hci_log_path not in stack_log_path):
		print ("pull stack in other folder",stack_log_path,hci_log_path)
		run_adb("pull " + stack_log_path + " " + dst_log_path)

	if (picus_log_path != stack_log_path and picus_log_path != hci_log_path):
		if stack_log_path not in picus_log_path and hci_log_path not in picus_log_path:
			print ("pull picus in other folder")
			run_adb("pull " + picus_log_path + " " + dst_log_path)

def parse_stack_conf(local_log_path):
	#save local config
	file_path = local_log_path + "/bt_stack.conf"

	picus_log_path = LOG_DUT_DEFAULT_PATH
	stack_log_path = LOG_DUT_DEFAULT_PATH
	hci_log_path = LOG_DUT_DEFAULT_PATH

	if os.path.exists(file_path) == True:
		cf = open(file_path, 'r+')
		for line in cf.readlines():
			if "BtSnoopFileName=" in line and len(line)>16:
				#print(line)
				hci_log_path = line[16:-1]
			if "BtStackFileName=" in line and len(line) > 16:
				#print (line)
				stack_log_path = line[16:-1]
			if "BtPicusParam=" in line and len(line) > 13:
				#print(line)
				try:
					#don't know this part used for ? 2022.3.9 jing
					picus_param = line[line.find("=") + 1:]
					picus_param_list = picus_param.split()
					picus_param_path_idx = picus_param_list.index("-p")
					if picus_param_path_idx != -1:
						picus_log_path = picus_param_list[picus_param_path_idx + 1]
				except:
					pass
		cf.close()
	print ("Log Path:",picus_log_path,stack_log_path,hci_log_path)
	return picus_log_path ,stack_log_path ,hci_log_path

def get_other_logs(relative_folder):
	run_adb(" shell sync")
	# os.system("adb "+adb_device+" pull /data/syslog.log ./"+relative_folder+"/syslog.log")
	# os.system("adb "+adb_device+" pull /data/syslog.log.0  ./"+relative_folder+"/syslog.log.0")
	# os.system("adb "+adb_device+" pull /data/syslog.log.1 ./"+relative_folder+"/syslog.log.1")

	run_adb(" pull /proc/last_kmsg " + relative_folder + "/last_kmsg.log")
	run_adb(" shell cat /proc/meminfo > " + relative_folder + "/meminfo.txt")
	run_adb(" pull /lib/firmware/wifi_mt7920.cfg " + relative_folder + "/wifi.cfg")
	run_adb(" pull /lib/firmware/bt_mt7961_1a_2.cfg " + relative_folder + "/bt.cfg")
	run_adb(" shell uptime > " + relative_folder + "/version_uptime.txt")
	run_adb(" shell echo version: >> " + relative_folder + "/version_uptime.txt")
	run_adb(" shell cat /temp/version/version.ini >> " + relative_folder + "/version_uptime.txt")
	run_adb(" shell echo fw_version: >> " + relative_folder + "/version_uptime.txt")
	run_adb(" shell head -n 1 /lib/firmware/BT_RAM_CODE_MT7961_1a_2_hdr.bin >> " + relative_folder + "/version_uptime.txt")
	run_adb(" shell iwpriv wlan0 driver \"ver\" >> " + relative_folder + "/version_uptime.txt")

	run_adb(" shell dmesg > " + relative_folder + "/dmesg")
	run_adb(" shell top -b -n 1 > " + relative_folder + "/top.txt")
	run_adb(" shell ifconfig > " + relative_folder + "/wlan_satus.txt")
	run_adb(" shell wpa_cli -iwlan0 -p/tmp/wpa_supplicant status >> " + relative_folder + "/wlan_satus.txt")
	run_adb(" pull /proc/kallsyms " + relative_folder + "/kallsyms")
	run_adb(" shell rm -rf /data/coredump/*")
	# os.system("adb "+adb_device+" shell rm -rf /data/misc/stp_dump/*")
	run_adb(" shell rm -rf " + picus_log_path + "fw_dump*")
	run_adb(" shell rm -rf /data/syslog.log*")
	run_adb(" shell sync")

if __name__ == '__main__':

	if len(sys.argv) > 1:
		LOG_LOCAL_PATH = sys.argv[1]
		print("Use input path:",LOG_LOCAL_PATH)
	else:
		LOG_LOCAL_PATH = os.path.join(os.getcwd(),
									  "yocto_bt_log_" + time.strftime("%Y%m%d_%H%M%S", time.localtime(time.time())))
		print("New path:", LOG_LOCAL_PATH)

	if len(sys.argv) > 2:
		adb_device = sys.argv[2] + " "

	if len(sys.argv) > 3:
		adb_device = adb_device + sys.argv[3] + " "

	print ("wait adb devices ...")
	os.system("adb wait-for-device")
	print ("adb devices connected")

	if os.path.exists(LOG_LOCAL_PATH) == False:
		print ("Create " + LOG_LOCAL_PATH)
		os.makedirs(LOG_LOCAL_PATH)
		os.makedirs(os.path.join(LOG_LOCAL_PATH, "bluetooth"))

	#print ("5.get bt_stack.conf")
	if os.path.exists(LOG_LOCAL_PATH + "/bt_stack.conf") == False:
		run_adb(" pull /data/misc/bluedroid/bt_stack.conf " + LOG_LOCAL_PATH)
		run_adb(" pull /data/misc/bluedroid/bt_config.conf " + LOG_LOCAL_PATH)
		run_adb(" pull /data/misc/bluedroid/bt_did.conf " + LOG_LOCAL_PATH)

	#print ("6.parse bt_stack.conf")
	picus_log_path ,stack_log_path ,hci_log_path = parse_stack_conf(LOG_LOCAL_PATH)
	run_adb("shell sync")
	pull_log_files(os.path.join(LOG_LOCAL_PATH, "bluetooth"), hci_log_path, stack_log_path, picus_log_path)
	get_other_logs(LOG_LOCAL_PATH)
	print('get success, quit after 1s')
	time.sleep(1)
