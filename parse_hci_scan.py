#!/usr/bin/python3
# -*- coding: utf-8 -*-
import os.path
import time
import hci
import parse_config


#hci config
HCI_Filter = ["HCI_Inquiry","HCI_LE_Set_Scan_Enable","HCI_Inquiry_Cancel","HCI_Inquiry_Complete",
              "HCI_LE_Advertising_Report","APCF","HCI_LE_Set_Scan_Parameters",
              "HCI_Extended_Inquiry_Result","HCI_LE_Extended_Advertising_Report"]
#save report
HCI_REPORT_FILE = "scan_hci_filter.txt"
HCI_FILE = ""

def parse(file):
    cnt = 0
    scan_frame = []
    buf = []
    with open(file, 'rb') as f:
        #header parse
        c = f.read(16)
        if not "btsnoop" in c[:7].decode():
            print("not hci")
            return
        #frame parse
        buf = f.read()

    pkts, _ = hci.from_binary(buf)

    for frame in pkts:
        cnt += 1
        if frame.packet_type == 1 or frame.packet_type == 4:
            line = "".join('{} {}').format(str(cnt).ljust(6), frame)
            for key in HCI_Filter:
                if key in line:
                    scan_frame.append(line)
                    #print(line)
                    break
    if scan_frame:
        print("Get {} scan_frame".format(len(scan_frame)))
        with open(HCI_REPORT_FILE, 'w') as f:
            for frame in scan_frame:
                frame += "\n"
                f.write(frame)
    print("Parse hci scan done")


if __name__ == '__main__':
    if os.path.exists(HCI_REPORT_FILE):
        os.remove(HCI_REPORT_FILE)
        print("Remove old scan hci file")

    _,HCI_FILE = parse_config.get_hci_file()

    if not os.path.exists(HCI_FILE):
        print("HCI log not exists ! Exit after 3s")
        time.sleep(3)
        exit(0)
    parse(HCI_FILE)
