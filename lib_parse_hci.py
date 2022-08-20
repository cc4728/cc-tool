#!/usr/bin/python3
# -*- coding: utf-8 -*-
from struct import unpack_from, error
from enum import IntEnum

#vendor config
HCI_FILE = "voice_demo_btsnoop_hci.cfa"

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

def parse_name(buf,offset,len):
    pass

def parse_address(buf,offset):
    OFFSET, SIZE_OCTETS = offset, 6
