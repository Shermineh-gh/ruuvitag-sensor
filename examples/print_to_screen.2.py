'''
Printing Data to Shell Window
Press Ctrl+C to escape running sequence
'''
from time import sleep
from ruuvitag_sensor.testing import MyRuuvi

sensor = MyRuuvi('E8:C7:D7:F2:4B:47')
while True:
    try:
        sensor.update()
        sensor.print_to_shell()
        sleep(1)
    except:
        # On KeyError or KeyInterrupt exit loop
        print('\nExit')
        break
