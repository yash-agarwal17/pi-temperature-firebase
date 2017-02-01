from subprocess import check_output
from re import findall
from time import sleep, strftime, time

import logging
import logging.handlers
import requests
import json

# --------------------
#
# Requirements:
# 1. wget https://bootstrap.pypa.io/get-pip.py
# 2. sudo python get-pip.py
# 3. sudo pip install requests
#
# --------------------

# ------------ Read the temperature

def get_temp():
    temp = check_output(["vcgencmd","measure_temp"]).decode("UTF-8")
    temp = float(findall("\d+\.\d+",temp)[0])
    return(temp)

# ------------ Logging

def write_log(temp, tempF):
    cpu_logger.info("{0}\t{1:.1f}\t{2:.2f}".format(strftime("%Y-%m-%d %H:%M:%S"), temp, tempF))

# ------------ Write to firebase

def write_firebase(temp, tempF):
    now = int(time())
    queryParams = {'auth': config.get('auth')}
    data = '{{"time":"{0}", "temperature":{1:.1f}, "temperatureF":{2:.2f}}}'.format(strftime("%Y-%m-%d %H:%M:%S"), temp, tempF)

    # write to temperatures (ongoing)
    response = requests.put(getFirebaseUrl('temperatures/{:d}.json'.format(now)), data=data, params=queryParams)
    # write to current
    response = requests.put(getFirebaseUrl('current.json'), data=data, params=queryParams)

def getFirebaseUrl(path):
    return '{}/{}/{}'.format(config.get('base_url'), config.get('pi_name'), path)

# ------------ Log Setup

file_name = 'cpu_temp_log.tsv'
cpu_logger = logging.getLogger('CPU')
cpu_logger.setLevel(logging.INFO)
handler = logging.handlers.RotatingFileHandler(file_name, maxBytes=200*1024, backupCount=5)
cpu_logger.addHandler(handler)

# ------------ Data setup

config = json.load(open("config.json"))

# ------------ Do the Work

temp = get_temp()
tempF = (temp * 9 / 5) + 32

write_log(temp, tempF)
write_firebase(temp, tempF)
