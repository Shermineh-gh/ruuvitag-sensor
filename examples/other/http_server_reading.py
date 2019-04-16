'''
Python3 needed for requests
'''

from matplotlib.animation import FuncAnimation
import matplotlib.pyplot as plt
import requests

# Change this address to your settings
macaddr = 'E8:C7:D7:F2:4B:47'
hostname = 'raspberrypi3'
port = '5000'

# http-link generation
link = 'http://' + hostname + ':' + port + '/data/' + macaddr

# initialization of all axes
fig = plt.figure(figsize=(10, 7))
fig.canvas.set_window_title('Sensor E8:C7:D7:F2:4B:47')
ax1T = fig.add_subplot(2, 2, 1) # Temperatur
ax2R = fig.add_subplot(2, 2, 2) # RSSI
ax3 = fig.add_subplot(2, 2, 3)  # Beschleunigung
ax4 = fig.add_subplot(2, 2, 4)  # Luftdruck

ax1H = ax1T.twinx() # Luftfeuchte als secondary y-axis in ax1
ax2B = ax2R.twinx() # Battery-Wert als secondary y-axis in ax2

plt.subplots_adjust(wspace=0.5, hspace=0.4)

ax1T.set_title('Temperatur und Luftfeuchte')
ax2R.set_title('RSSI und Batteriespannung')
ax3.set_title('Beschleunigung / Neigung')
ax4.set_title('Luftdruck')

ax1T.set_ylabel('T in °C')
ax1H.set_ylabel('Luftfeuchte in %')
ax2R.set_ylabel('RSSI in dBm')
ax2B.set_ylabel('Batteriespannung in V')
ax3.set_ylabel('Beschleunigung in G')
ax4.set_ylabel('Druck in mBar')

ax1T.set_xlabel('Zeit in min')
ax2R.set_xlabel('Zeit in min')
ax3.set_xlabel('Zeit in min')
ax4.set_xlabel('Zeit in min')

timer = []
temp = []
accx = []
accy = []
accz = []
rssi = []
hum = []
pres = []
batt = []
counter = 0

ax1T.set_xlim([0, 2.1])
ax1T.set_ylim([-10, 30])

ax1H.set_xlim([0, 2.1])
ax1H.set_ylim([0, 100])

ax2R.set_xlim([0, 2.1])
ax2R.set_ylim([0, -150])

ax2B.set_xlim([0, 2.1])
ax2B.set_ylim([0, 4])

ax3.set_xlim([0, 2.1])
ax3.set_ylim([-1.500, 1.500])

ax4.set_xlim([0, 2.1])
ax4.set_ylim([600, 1200])

line1T, = ax1T.plot(timer, temp, 'b-', label='Temp.')
line1H, = ax1H.plot(timer, temp, 'c-', label='rel. LF.')
line2R, = ax2R.plot(timer, rssi, 'k-', label='RSSI')
line2B, = ax2B.plot(timer, batt, 'r-', label='Batterie')
line3x, = ax3.plot(timer, accx, 'k:', label='a(x)')
line3y, = ax3.plot(timer, accy, 'k--', label='a(y)')
line3z, = ax3.plot(timer, accz, 'k-', label='a(z)')
line4, = ax4.plot(timer, pres, 'k-', label='Druck')

# Erstellen der jeweiligen Diagramm-Legenden
line1 = [line1T, line1H]
ax1_labels = [l.get_label() for l in [line1T, line1H]]
ax1T.legend(line1, ax1_labels)

line2 = [line2R, line2B]
ax2_labels = [l.get_label() for l in [line2R, line2B]]
ax2R.legend(line2, ax2_labels)

ax3.legend()
ax4.legend()

def update(frame):
    global counter

    # Request Data from given link
    # -> Linux-System (Raspberry-Pi)
    # -> is linked with this http-webserver

    data = requests.get(link).json()

    # data request happens every 1000 ms (counter)
    # -> look at interval in "FuncAnimation"
    # -> timer in minutes
    timer.append(counter / 60)

    # get all new data into plotted arrays
    temp.append(data['temperature'])
    accx.append(data['acceleration_x'] / 1000)
    accy.append(data['acceleration_y'] / 1000)
    accz.append(data['acceleration_z'] / 1000)
    rssi.append(data['rssi'])
    hum.append(data['humidity'])
    pres.append(data['pressure'])
    batt.append(data['battery'] / 1000)

    if counter > 120:
        # set time-scales every time to 120s + 10s
        ax1T.set_xlim([timer[-1] - 2, timer[-1] + 0.1])
        ax1H.set_xlim([timer[-1] - 2, timer[-1] + 0.1])
        ax2R.set_xlim([timer[-1] - 2, timer[-1] + 0.1])
        ax3.set_xlim([timer[-1] - 2, timer[-1] + 0.1])
        ax4.set_xlim([timer[-1] - 2, timer[-1] + 0.1])

        # pop last item of all arrays
        # if time lasting > 120 s
        timer.pop(0)
        temp.pop(0)
        accx.pop(0)
        accy.pop(0)
        accz.pop(0)
        rssi.pop(0)
        hum.pop(0)
        pres.pop(0)
        batt.pop(0)

    # update all plots with new arrays
    line1T.set_data(timer, temp)
    line1H.set_data(timer, hum)
    line2R.set_data(timer, rssi)
    line2B.set_data(timer, batt)
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
