import zmq
import argparse
from py_msfs_lcd1602.lcd1602 import LCD1602


context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://*:5555")

if __name__ == "__main__":
    lcd = LCD1602(3)
    lcd.init_lcd()

    try:
        while True:
            #  Wait for next request from client
            message = socket.recv()
            
            lcd.write_ascii_string(message)
    finally:
        lcd.clear()
        lcd.rgb_off()
        lcd.close()