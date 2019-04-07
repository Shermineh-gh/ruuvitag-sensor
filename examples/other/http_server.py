'''
Simple http server, that returns data in json.
Executes get data for sensors in the background.

Endpoints:
    http://0.0.0.0:5000/data
    http://0.0.0.0:5000/data/<mac>

Requires:
    Flask - pip install flask
'''

import json
from multiprocessing import Manager
from concurrent.futures import ProcessPoolExecutor
from flask import Flask, abort
from ruuvitag_sensor.ruuvi import RuuviTagSensor

app = Flask(__name__)

m = Manager()
q = m.Queue()

allData = {}

tags = {
    'E8:C7:D7:F2:48:47': 'S1',
    'C6:E0:4D:19:D0:47': 'S2',
    'D5:98:A7:DB:02:77': 'S3'
}

timeout_in_sec = 5


def run_get_data_background(macs, queue):
    """
    Background process from RuuviTag Sensors
    """
    while True:
        datas = RuuviTagSensor.get_data_for_sensors(macs, timeout_in_sec)
        queue.put(datas)


def update_data():
    """
    Update data sent by background process to global allData
    """
    global allData
    while not q.empty():
        allData = q.get()
    for key, value in tags.items():
        if key in allData:
            allData[key]['name'] = value


@app.route('/data')
def get_all_data():
    update_data()
    return json.dumps(allData)


@app.route('/data/<mac>')
def get_data(mac):
    update_data()
    if mac not in allData:
        abort(404)
    return json.dumps(allData[mac])


if __name__ == '__main__':
    # Start background process
    executor = ProcessPoolExecutor(1)
    executor.submit(run_get_data_background, list(tags.keys()), q)

    # Strt Flask application
    app.run(host='0.0.0.0', port=5000, debug=True)
