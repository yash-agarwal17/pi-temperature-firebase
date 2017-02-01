import requests
import time

# ------------ Get current status
def get_status(pi_name):
    url = 'https://pi-temperature-c369d.firebaseio.com/temperature/{0}/status.json'.format(pi_name)
    query_params = {'auth': 'ItdM8YVCzL5YBbiEM2sSax92JhficBxvFPPKBzXz'}
    response = requests.get(url, params=query_params)
    json = response.json()
    return json.get('lastRollTime')

# ------------ Do data need to roll
def roll_data_if_needed(pi_name, secondsAllowed):
    last_roll_time = get_status(pi_name)
    now = int(time.time())
    time_since_roll = now - last_roll_time
    if time_since_roll > secondsAllowed:
        roll_data(pi_name)
    else:
        print time_since_roll
        print secondsAllowed
        print 'do not roll'

def roll_data(pi_name):
    query_params = {'auth': 'ItdM8YVCzL5YBbiEM2sSax92JhficBxvFPPKBzXz'}

    # delete backup
    url = 'https://pi-temperature-c369d.firebaseio.com/temperature/{0}/temperatures-backup.json'.format(pi_name)
    requests.delete(url, params=query_params)

    # update status time
    url = 'https://pi-temperature-c369d.firebaseio.com/temperature/{0}/status.json'.format(pi_name)
    data = '{{"lastRollTime": {:d}}}'.format(int(time.time()))
    response = requests.put(url, params=query_params, data=data)

    # get current values
    url = 'https://pi-temperature-c369d.firebaseio.com/temperature/{0}/temperatures.json'.format(pi_name)
    response = requests.get(url, params=query_params)
    current_values = response.text
    print current_values

    # add to backup
    url = 'https://pi-temperature-c369d.firebaseio.com/temperature/{0}/temperatures-backup.json'.format(pi_name)
    requests.put(url, params=query_params, data=current_values)

    # delete current values
    url = 'https://pi-temperature-c369d.firebaseio.com/temperature/{0}/temperatures.json'.format(pi_name)
    requests.delete(url, params=query_params)


# ------------ Let's do this
roll_data_if_needed('home-test', 10)
