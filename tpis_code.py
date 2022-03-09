#run other python script
import os
cmd = r"python test.py " + ADB_DEVICE
os.system(cmd)

#check input char，and stop script
import msvcrt
import time
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
        
#run adb cmd
def run_adb(command):
	adb_command_debug = True
	cmd = "adb "+ADB_DEVICE+command
	if adb_command_debug:
		print('[' + cmd + ']')
	return os.popen(cmd).read()
    
    
# pause console
raw_input('pull success, any key quit')
    
#other process adb
def run_adb(command, use_shell=True, print_result=False, timeout=60):
	adb_command_debug = False
	print_result = False
	adb_debug = False
	if adb_command_debug:
		print '[' + command + ']'
	output = ''
	process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=use_shell)
	kill_process = lambda p : p.kill()
	timer = threading.Timer(timeout, kill_process, [process])
	stdout = 'timeout'
	stderr = 'timeout'
	try:
		#timer.start()
		stdout, stderr = process.communicate()
	finally:
		#timer.cancel()
		pass
	for msg in [stdout, stderr]:
		if print_result or adb_debug:
				print msg
				print '--------'
		if stderr is not None:
			print stderr
	return process.returncode, stdout
    
    
#list sort
names.sort(key=lambda x:int(filter(str.isdigit, x) or -1))

#str check start
name.startswith('BT_HCI_')

#get current path
os.getcwd()

#merge file1 to file2
file1 = open('file1', 'rb')
file2 = open('file2', 'rb')
shutil.copyfileobj(file1, file2)
