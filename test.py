#!/usr/bin/python
import socket
import fcntl
import struct
import mraa
import sys
import time
import datetime
import pywapi

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

# Set city to Toronto ID#
city = 'CAXX0504'

# Print it.
x = 1000

# when is it too cold?
too_cold = -10

for i in range(0, x):

    now = datetime.datetime.now()

    weather = pywapi.get_weather_from_weather_com(city, units = 'metric')
    current_temp = weather['current_conditions']['temperature']

    year = now.year
    month = now.month
    day = now.day
    hour = now.hour
    minute = now.minute

    if minute < 10:
        myString = '%s:0%s %s/%s/%s' % (hour, minute, month, year)
    else:
        myString = '%s:%s %s/%s/%s' % (hour, minute, day, month, year)
    myLcd.clear()
    myLcd.setCursor(0,0)
    myLcd.write(myString)

    print int(current_temp) < too_cold
    if int(current_temp) < too_cold:
        myLcd.setCursor(1,0)
        myString = 'Its freezing. %s' % str(current_temp)
    else:
        myLcd.setCursor(1,15)
        myString = '%s out.' % str(current_temp)
    myLcd.write(myString)
    time.sleep(2)
