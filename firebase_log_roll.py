import requests
import time
import json

# ------------ Do data need to roll
def roll_data_if_needed(secondsAllowed):
    # calculate last time
    last_roll_time = get_status()
    now = int(time.time())
    time_since_roll = now - last_roll_time
    # do I need to roll?
    if time_since_roll > secondsAllowed:
        roll_data()
    else:
        print 'do not roll'

# ------------ Get current status
def get_status():
    response = firebaseGet('status.json')
    json = response.json()
    return json.get('lastRollTime')


# ------------ Roll the data
def roll_data():
    # delete backup
    firebaseDelete('temperatures-backup.json')

    # update status time
    data = '{{"lastRollTime": {:d}}}'.format(int(time.time()))
    firebasePut('status.json', data)

    # get current values
    response = firebaseGet('temperatures.json')
    current_values = response.text

    # add to backup
    firebasePut('temperatures-backup.json', current_values)

    # delete current values
    firebaseDelete('temperatures.json')

# ------------ Firebase calls
def firebaseGet(path):
    return requests.get(getFirebaseUrl(path), params=getFirebaseQueryParams())

def firebasePut(path, data):
    requests.put(getFirebaseUrl(path), params=getFirebaseQueryParams(), data=data)

def firebaseDelete(path):
    return requests.delete(getFirebaseUrl(path), params=getFirebaseQueryParams())

def getFirebaseQueryParams():
    return {'auth': config.get('auth')}

def getFirebaseUrl(path):
    return '{}/{}/{}'.format(config.get('base_url'), config.get('pi_name'), path)

# ------------ Data setup

config = json.load(open("~/config.json"))

# ------------ Let's do this
roll_data_if_needed(60*60*24)
