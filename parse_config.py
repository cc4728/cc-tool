import os.path
import re

CONFIG_FILE = "project_config.conf"
VALUE_FORMATE = '\"(.+)\"'  #"VALUE"

def get_logcat_file():
    project = ""
    logcat_file = ""
    if not os.path.exists(CONFIG_FILE):
        return project,logcat_file
    with open(CONFIG_FILE, 'rb') as f:
        line = f.readline().decode('utf-8', 'ignore')
        while line:
            l = line.split(" ")
            if "Project:" in l[0] and "YES" in l[2]:
                project = l[0]
            if project:
                if "LOGCAT_FILE" in l[0]:
                    logcat_file = l[2].strip('\r\n')
                    break
            line = f.readline().decode('utf-8', 'ignore')
    print("Found:",project," ",logcat_file)
    return project, logcat_file

def get_scan_start_tag():
    project = ""
    scan_start_tag = ""
    if not os.path.exists(CONFIG_FILE):
        return project,scan_start_tag
    with open(CONFIG_FILE, 'rb') as f:
        line = f.readline().decode('utf-8', 'ignore')
        while line:
            l = line.split(" ")
            if "Project:" in l[0] and "YES" in l[2]:
                project = l[0]
            if project:
                if "SCAN_START_TAG" in l[0]:
                    tmp = re.compile(VALUE_FORMATE).search(line)
                    if tmp:
                        scan_start_tag = tmp[0][1:-1] #remove ""
                    break
            line = f.readline().decode('utf-8', 'ignore')
    print("Found:",project," ",scan_start_tag)
    return project, scan_start_tag

def get_scan_end_tag():
    project = ""
    scan_end_tag = ""
    if not os.path.exists(CONFIG_FILE):
        return project,scan_end_tag
    with open(CONFIG_FILE, 'rb') as f:
        line = f.readline().decode('utf-8', 'ignore')
        while line:
            l = line.split(" ")
            if "Project:" in l[0] and "YES" in l[2]:
                project = l[0]
            if project:
                if "SCAN_END_TAG" in l[0]:
                    tmp = re.compile(VALUE_FORMATE).search(line)
                    if tmp:
                        scan_end_tag = tmp[0][1:-1] #remove ""
                    break
            line = f.readline().decode('utf-8', 'ignore')
    print("Found:",project," ",scan_end_tag)
    return project, scan_end_tag

def get_scan_result_tag():
    project = ""
    scan_result_tag = ""
    if not os.path.exists(CONFIG_FILE):
        return project,scan_result_tag
    with open(CONFIG_FILE, 'rb') as f:
        line = f.readline().decode('utf-8', 'ignore')
        while line:
            l = line.split(" ")
            if "Project:" in l[0] and "YES" in l[2]:
                project = l[0]
            if project:
                if "SCAN_RESULT_TAG" in l[0]:
                    tmp = re.compile(VALUE_FORMATE).search(line)
                    if tmp:
                        scan_result_tag = tmp[0][1:-1] #remove ""
                    break
            line = f.readline().decode('utf-8', 'ignore')
    print("Found:",project," ",scan_result_tag)
    return project, scan_result_tag

def get_hci_file():
    project = ""
    hci_file = ""
    if not os.path.exists(CONFIG_FILE):
        return project,hci_file
    with open(CONFIG_FILE, 'rb') as f:
        line = f.readline().decode('utf-8', 'ignore')
        while line:
            l = line.split(" ")
            if "Project:" in l[0] and "YES" in l[2]:
                project = l[0]
            if project:
                if "HCI_FILE" in l[0]:
                    hci_file = l[2].strip('\r\n')
                    break
            line = f.readline().decode('utf-8', 'ignore')
    print("Found:",project," ",hci_file)
    return project, hci_file

def get_bt_addr_formate():
    project = ""
    bt_addr_formate = ""
    if not os.path.exists(CONFIG_FILE):
        return project,bt_addr_formate
    with open(CONFIG_FILE, 'rb') as f:
        line = f.readline().decode('utf-8', 'ignore')
        while line:
            l = line.split(" ")
            if "Project:" in l[0] and "YES" in l[2]:
                project = l[0]
            if project:
                if "BT_ADDR_FORMATE" in l[0]:
                    tmp = re.compile(VALUE_FORMATE).search(line)
                    if tmp:
                        bt_addr_formate = tmp[0][1:-1] #remove ""
                    break
            line = f.readline().decode('utf-8', 'ignore')
    print("Found:",project," ",bt_addr_formate)
    return project, bt_addr_formate

def get_logcat_date_formate():
    project = ""
    logcat_date_formate = ""
    if not os.path.exists(CONFIG_FILE):
        return project,logcat_date_formate
    with open(CONFIG_FILE, 'rb') as f:
        line = f.readline().decode('utf-8', 'ignore')
        while line:
            l = line.split(" ")
            if "Project:" in l[0] and "YES" in l[2]:
                project = l[0]
            if project:
                if "LOGCAT_DATE_FORMATE" in l[0]:
                    tmp = re.compile(VALUE_FORMATE).search(line)
                    if tmp:
                        logcat_date_formate = tmp[0][1:-1] #remove ""
                    break
            line = f.readline().decode('utf-8', 'ignore')
    print("Found:",project," ",logcat_date_formate)
    return project, logcat_date_formate

def get_scan_device_name():
    project = ""
    scan_device_name = ""
    if not os.path.exists(CONFIG_FILE):
        return project,scan_device_name
    with open(CONFIG_FILE, 'rb') as f:
        line = f.readline().decode('utf-8', 'ignore')
        while line:
            l = line.split(" ")
            #print(l)
            if "Project:" in l[0] and "YES" in l[2]:
                project = l[0]
            if project:
                if "SCAN_DEVICE_NAME" in l[0]:
                    tmp = re.compile(VALUE_FORMATE).search(line)
                    if tmp:
                        scan_device_name = tmp[0][1:-1] #remove ""
                    break
            line = f.readline().decode('utf-8', 'ignore')
    print("Found:",project," ",scan_device_name)
    return project, scan_device_name


def get_scan_special_name():
    project = ""
    scan_special_name = ""
    if not os.path.exists(CONFIG_FILE):
        return project,scan_special_name
    with open(CONFIG_FILE, 'rb') as f:
        line = f.readline().decode('utf-8', 'ignore')
        while line:
            l = line.split(" ")
            #print(l)
            if "Project:" in l[0] and "YES" in l[2]:
                project = l[0]
            if project:
                if "SCAN_SPECIAL_NAME" in l[0]:
                    tmp = re.compile(VALUE_FORMATE).search(line)
                    if tmp:
                        scan_special_name = tmp[0][1:-1] #remove ""
                    break
            line = f.readline().decode('utf-8', 'ignore')
    print("Found:",project," ",scan_special_name)
    return project, scan_special_name

def get_scan_special_addr():
    project = ""
    scan_special_addr = ""
    if not os.path.exists(CONFIG_FILE):
        return project,scan_special_addr
    with open(CONFIG_FILE, 'rb') as f:
        line = f.readline().decode('utf-8', 'ignore')
        while line:
            l = line.split(" ")
            #print(l)
            if "Project:" in l[0] and "YES" in l[2]:
                project = l[0]
            if project:
                if "SCAN_SPECIAL_ADDR" in l[0]:
                    tmp = re.compile(VALUE_FORMATE).search(line)
                    if tmp:
                        scan_special_addr = tmp[0][1:-1] #remove ""
                    break
            line = f.readline().decode('utf-8', 'ignore')
    print("Found:",project," ",scan_special_addr)
    return project, scan_special_addr


if __name__ == '__main__':
    get_scan_device_name()
    get_hci_file()
    get_bt_addr_formate()
    get_scan_result_tag()
    get_scan_start_tag()
    get_scan_end_tag()
    get_logcat_date_formate()
    get_logcat_file()