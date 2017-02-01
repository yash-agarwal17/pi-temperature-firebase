# Raspberry Pi Temperature Monitor

This project consists of 2 python scripts that can be run on a raspberry pi that measure the temperature of the pi and report the data to [Firebase](https://firebase.google.com/).

## Scripts

The first script, `temp_monitor.py` just measures the internal temperature using `vcgencmd`, logs it to a file, and posts it to firebase.

The second script, `firebase_log_roll.py` is used so you don't keep too much data in firebase by removing old data. By default, it will delete that data once a day, so at most you'll have about two days of data, and at a minimum you'll have one.

## Graph

In addition to recording the temperature, I also have a simple HTML page that uses D3 to graph the temperature. It pulls data directly from Firebase to plot a simple line chart.

![Example chart](images/example-chart.png)

## Dependencies

### pip

This isn't strictly required, but it is the easiest way to get the `requests` python package. More information on `pip` can be found here: [website](https://pip.pypa.io/en/stable/)

To install `pip` on the raspberry pi:

1. `wget https://bootstrap.pypa.io/get-pip.py`
2. `sudo python get-pip.py`

### requests library
The `requests` python package is used to make the REST API calls to Firebase. More information can be found here: [website](http://docs.python-requests.org/en/master/)

Assuming you have `pip` installed, all you need to do is:

1. `sudo pip install requests`
