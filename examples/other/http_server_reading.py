'''
Python3 needed for urllib3 and requests
'''

import time
from statistics import mean
from matplotlib.animation import FuncAnimation
import matplotlib.pyplot as plt
import requests

#plt.ion()  # Get Interactive Plots

# Change this address to your settings
link = "http://raspberrypi3:5000/data/E8:C7:D7:F2:4B:47"

fig = plt.figure(figsize=(10, 7))
fig.canvas.set_window_title('Sensor E8:C7:D7:F2:4B:47')
ax1T = fig.add_subplot(2, 2, 1)
ax2 = fig.add_subplot(2, 2, 2)
ax3 = fig.add_subplot(2, 2, 3)
ax4 = fig.add_subplot(2, 2, 4)
ax1H = ax1T.twinx()

plt.subplots_adjust(wspace=0.5, hspace=0.3)

ax1T.set_title('Temperatur und Luftfeuchte')
ax2.set_title('RSSI')
ax3.set_title('Beschleunigung / Neigung')
ax4.set_title('Luftdruck')

ax1T.set_ylabel('T in °C')
ax1H.set_ylabel('Luftfeuchte in %')
ax2.set_ylabel('RSSI in dBm')
ax3.set_ylabel('Beschleunigung in G')
ax4.set_xlabel('Druck in mBar')

ax2.set_xlabel('Zeit in s')
ax4.set_xlabel('Zeit in s')

timer = []
temp = []
accx = []
accy = []
accz = []
rssi = []
hum = []
pres = []
counter = 0

ax1T.set_xlim([0, 70])
ax1T.set_ylim([-10, 30])

ax1H.set_xlim([0, 70])
ax1H.set_ylim([0, 100])

ax2.set_xlim([0, 70])
ax2.set_ylim([0,-150])

ax3.set_xlim([0, 70])
ax3.set_ylim([-1.500, 1.500])

ax4.set_xlim([0, 70])
ax4.set_ylim([0, 1200])

line1T, = ax1T.plot(timer, temp, 'b-', label='Temp.')
line1H, = ax1H.plot(timer, temp, 'c-', label='rel. Hum.')
line2, = ax2.plot(timer, rssi, 'k-', label='RSSI')
line3x, = ax3.plot(timer, accx, 'k:', label='a(X)')
line3y, = ax3.plot(timer, accy, 'k--', label='a(Y)')
line3z, = ax3.plot(timer, accz, 'k-', label='a(Z)')
line4, = ax4.plot(timer, pres, 'k-', label='Pres.')

line1 = [line1T, line1H]
line1_labels = [l.get_label() for l in line1]
ax1T.legend(line1, line1_labels)
ax2.legend()
ax3.legend()
ax4.legend()

def update(frame):
    global counter

    data = requests.get(link).json()
    timer.append(counter)
    temp.append(data['temperature'])
    accx.append(data['acceleration_x'] / 1000)
    accy.append(data['acceleration_y'] / 1000)
    accz.append(data['acceleration_z'] / 1000)
    rssi.append(data['rssi'])
    hum.append(data['humidity'])
    pres.append(data['pressure'])

    if counter > 60:
        ax1T.set_xlim([timer[-1] - 60, timer[-1] + 10])
        ax1H.set_xlim([timer[-1] - 60, timer[-1] + 10])
        ax2.set_xlim([timer[-1] - 60, timer[-1] + 10])
        ax3.set_xlim([timer[-1] - 60, timer[-1] + 10])
        ax4.set_xlim([timer[-1] - 60, timer[-1] + 10])
        timer.pop(0)
        temp.pop(0)
        accx.pop(0)
        accy.pop(0)
        accz.pop(0)
        rssi.pop(0)
        hum.pop(0)
        pres.pop(0)

    line1T.set_data(timer, temp)
    line1H.set_data(timer, hum)
    line2.set_data(timer, rssi)
    line3x.set_data(timer, accx)
    line3y.set_data(timer, accy)
    line3z.set_data(timer, accz)
    line4.set_data(timer, pres)

    counter += 1

while True:
    try:
        ani = FuncAnimation(fig, update, interval=1000)
        plt.show()
        # Wait and start over again
    except KeyboardInterrupt:
        # When Ctrl+C is pressed
        # execution of the while loop is stopped
        print('Exit')
        break
