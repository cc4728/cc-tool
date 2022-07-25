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

#print sys.argv

adb_device="-s 0123456789ABCDEF "  ###here must be end with a space
if len(sys.argv) > 1:
	adb_device = sys.argv[1]+" "

if len(sys.argv) > 2:
	adb_device = adb_device+sys.argv[2]+" "

cmd=r"adb "+adb_device+" shell \"echo -n 'file sound/soc/mediatek/mt8518/mt8518-audio-spi.c +p' > /sys/kernel/debug/dynamic_debug/control\""
print(cmd)
os.system(cmd)
