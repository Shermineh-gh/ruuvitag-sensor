'''
Python3 needed for urllib3 and requests
'''

import time
import requests
#import os
#import math

link = "http://raspberrypi3:5000/data/E8:C7:D7:F2:4B:47"  # Change this address to your settings

while True:
    r = requests.get(link)
    print(r.json())

    try:
        # Wait and start over again
        time.sleep(0.5)
    except KeyboardInterrupt:
        # When Ctrl+C is pressed
        # execution of the while loop is stopped
        print('Exit')
        break
