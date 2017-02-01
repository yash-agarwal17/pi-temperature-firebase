from subprocess import check_output
from re import findall
from time import sleep, strftime, time

import logging
import logging.handlers
import requests

# --------------------
#
# Requirements:
# 1. wget https://bootstrap.pypa.io/get-pip.py
# 2. sudo python get-pip.py
# 3. sudo pip install requests
#
# --------------------

# ------------ Methods

def get_temp():
    temp = check_output(["vcgencmd","measure_temp"]).decode("UTF-8")
    temp = float(findall("\d+\.\d+",temp)[0])
    return(temp)

def write_log(temp):
    tempF = (temp * 9 / 5) + 32
    cpu_logger.info("{0}\t{1:.1f}\t{2:.2f}".format(strftime("%Y-%m-%d %H:%M:%S"), temp, tempF))

def write_firebase(temp, pi_name):
    now = int(time())
    queryParams = {'auth': 'ItdM8YVCzL5YBbiEM2sSax92JhficBxvFPPKBzXz'}
    data = '{{"time":"{0}", "temperature":{1:.1f}}}'.format(strftime("%Y-%m-%d %H:%M:%S"), temp)

    url = 'https://pi-temperature-c369d.firebaseio.com/temperature/{}/temperatures/{:d}.json'.format(pi_name, now)
    response = requests.put(url, data=data, params=queryParams)

    url = 'https://pi-temperature-c369d.firebaseio.com/temperature/{}/current.json'.format(pi_name)
    response = requests.put(url, data=data, params=queryParams)

# ------------ Data setup

pi_name = 'work-retropi'

# ------------ Log Setup

file_name = 'cpu_temp_log.tsv'
cpu_logger = logging.getLogger('CPU')
cpu_logger.setLevel(logging.INFO)
handler = logging.handlers.RotatingFileHandler(file_name, maxBytes=200*1024, backupCount=5)
cpu_logger.addHandler(handler)

# ------------ Do the Work

temp = get_temp()
write_log(temp)
write_firebase(temp, pi_name)
