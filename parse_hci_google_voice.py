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

#vendor config  usually use （8MHZ，16bit）or（16MHZ,16bit） 
HCI_FILE = "btsnoop_hci.cfa" 

# Need double check, the frame total length:case1 ,full pkt
TOTAL_LENGTH_1 = 32
# Need double check,the frame total length:case2 ,last pkt
TOTAL_LENGTH_2 = 26
#Need double check,handle offset, from the begin of frame
DATA_HANDLE = 64

#Don't modify,handle offset, from the begin of frame
HANDLE_OFFSET = 10
#Don't modify, from the VOICE_DATA_OFFSET to end is voice data
VOICE_DATA_OFFSET = 12
#Don't modify , check ATT notify, 0x1b=27
OPCODE = 27
OPCODE_OFFSET = 9


#const define
class PacketType(IntEnum):
    COMMAND = 0x01
    ASYNCHRONOUS_DATA = 0x02
    SYNCHRONOUS_DATA = 0x03
    EVENT = 0x04
    ISO_DATA = 0x05

OFFSET_DATA_LENGTH = {"COMMAND": 3,
              "EVENT": 2,
              "ASYNCHRONOUS_DATA": 3,
              "ISO_DATA": 3,
              "SYNCHRONOUS_DATA": 3
}

DATA_LENGTH_OCTET = {"COMMAND": 1,
              "ASYNCHRONOUS_DATA": 2,
              "SYNCHRONOUS_DATA": 2,
              "EVENT": 1,
              "ISO_DATA": 2
              }

def _parse_pkt_type(buf, pkt_offset):
    return unpack_from('<B', buf, offset=pkt_offset)[0]

def _parse_pkt_length(buf, pkt_type, pkt_offset):
    data_length = 0
    if pkt_type> 0 and pkt_type < 6:
        type = PacketType(pkt_type).name
        #print("type:", type)
        offset_data_length = OFFSET_DATA_LENGTH[type]
        #print("offset_data_length:",offset_data_length)
        offset = pkt_offset + offset_data_length
        if DATA_LENGTH_OCTET[type] == 1:
            data_length = unpack_from('<B', buf, offset=offset)[0]
        elif DATA_LENGTH_OCTET[type] == 2:
            data_length = unpack_from('<H', buf, offset=offset)[0]
        #print("data_length:",data_length)
        pkt_length = DATA_LENGTH_OCTET[type] + offset_data_length + data_length
        #print("pkt_length",pkt_length)
    else:
        raise NotImplementedError(pkt_type)
    return pkt_length

def get_raw_data():
    PACKET_HEADER_SIZE_OCTETS = 24
    pkts = []
    pkt_offset = 0
    with open(HCI_FILE, 'rb') as f:
        #header parse
        header = f.read(16)
        if not "btsnoop" in header[:7].decode('utf-8', 'ignore'):
            print("Skip_no_header: ", HCI_FILE)
            return
        buf = f.read()
        while (pkt_offset < len(buf) and len(buf) > PACKET_HEADER_SIZE_OCTETS):
            try:
                pkt_offset += PACKET_HEADER_SIZE_OCTETS
                pkt_type = _parse_pkt_type(buf, pkt_offset)
                if not pkt_type :
                    break
                pkt_length = _parse_pkt_length(buf, pkt_type, pkt_offset)
            except error:
                incomplete_pkt_data = buf[pkt_offset:]
                break
            pkt_data = buf[pkt_offset:pkt_offset + pkt_length]
            #print(pkt_data)
            if (len(pkt_data) < pkt_length):
                incomplete_pkt_data = pkt_data
                break
            pkts.append(pkt_data)
            pkt_offset += pkt_length
    print("Get {} item hci frame".format(len(pkts)))
    return pkts

def parse(buf):
    adpcm_buf = []
    for i in buf:
        if len(i) == TOTAL_LENGTH_1 or len(i) == TOTAL_LENGTH_2:
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