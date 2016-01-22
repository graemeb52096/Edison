#!/usr/bin/python
import socket
import fcntl
import struct
import mraa
import sys
import time
import datetime

import pyupm_i2clcd as lcd

def get_ip_address(ifname):

    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    return socket.inet_ntoa(fcntl.ioctl(
        s.fileno(),
        0x8915,  # SIOCGIFADDR
        struct.pack('256s', ifname[:15])
    )[20:24])

# Initialize Jhd1313m1 at 0x3E (LCD_ADDRESS) and 0x62 (RGB_ADDRESS)
myLcd = lcd.Jhd1313m1(0, 0x3E, 0x62)

# Clear
myLcd.clear()

# Green
myLcd.setColor(200, 200, 200)

# Zero the cursor
myLcd.setCursor(0,0)

# Print it.
x = 1000
for i in range(0, x):
    now = datetime.datetime.now()
    myLcd.write(now)
    time.sleep(1)
    myLcd.clear