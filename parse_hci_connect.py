#!/usr/bin/python3
# -*- coding: utf-8 -*-
import os.path
import time
import hci

#hci config
HCI_Filter = ["HCI_LE_Add_Device_To_Filter_Accept_List","HCI_LE_Extended_Create_Connection",
              "HCI_LE_Connection_Update","HCI_Disconnection_Complete"
]

#save report
REPORT_FILE = "connect_hci_filter.txt"
HCI_FILE = "btsnoop_hci.cfa"

def parse(file):
    cnt = 0
    conn_frame = []
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
                    conn_frame.append(line)
                    print(line)
                    break
    if conn_frame:
        print("Get {} conn_frame".format(len(conn_frame)))
        with open(REPORT_FILE, 'w') as f:
            for frame in conn_frame:
                frame += "\n"
                f.write(frame)
    print("Parse done")


if __name__ == '__main__':
    if not os.path.exists(HCI_FILE):
        print("HCI log not exists ! Exit after 3s")
        time.sleep(3)
        exit(0)
    parse(HCI_FILE)
    time.sleep(2)