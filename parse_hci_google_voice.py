#!/usr/bin/python3
# -*- coding: utf-8 -*-
import os
import os.path
import sys
import time
import datetime
from struct import unpack_from, error
from enum import IntEnum
from lib_adpcm_codec import adpcm2pcm
from lib_parse_hci import HCI_FILE,get_raw_data

#usually use （8MHZ，16bit）or（16MHZ,16bit）
# Need double check, the frame total length:case1 ,full pkt;case2 last pkt
TOTAL_LENGTH = [32,26]
#Need double check,handle offset, from the begin of frame
DATA_HANDLE = 64

#Don't modify,handle offset, from the begin of frame
HANDLE_OFFSET = 10
#Don't modify, from the VOICE_DATA_OFFSET to end is voice data
VOICE_DATA_OFFSET = 12
#Don't modify , check ATT notify, 0x1b=27
OPCODE = 27
OPCODE_OFFSET = 9


def parse(buf):
    adpcm_buf = []
    for i in buf:
        if len(i) in TOTAL_LENGTH:
            if DATA_HANDLE == unpack_from('<H', i, offset=HANDLE_OFFSET)[0] and OPCODE == unpack_from('<B', i, offset=OPCODE_OFFSET)[0]:
                for byte in i[VOICE_DATA_OFFSET:]:
                    adpcm_buf.append(byte)
    print("Get {} bytes adpcm data".format(len(adpcm_buf)))
    try:
        s = open('pcm', 'wb')
        for b in adpcm_buf:
            sample = b
            high_bit = sample >> 4
            low_bit = (high_bit << 4) ^ sample
            s.write(adpcm2pcm(high_bit))
            s.write(adpcm2pcm(low_bit))
        s.close()
    except:
        print("decoder fail")
    print("Parse done")

if __name__ == '__main__':
    if not os.path.exists(HCI_FILE):
        print("HCI log not exists ! Exit after 3s")
        time.sleep(3)
        exit(0)
    parse(get_raw_data())
    time.sleep(2)