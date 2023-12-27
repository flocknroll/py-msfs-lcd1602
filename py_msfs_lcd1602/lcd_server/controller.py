import zmq
import argparse
import logging
import json

from py_msfs_lcd1602.driver import LCD1602


parser = argparse.ArgumentParser("LCD1602 controller backend")
parser.add_argument("--bus-id", default=3)
parser.add_argument("--port", default=5555)

if __name__ == "__main__":
    params = parser.parse_args()

    context = zmq.Context()
    socket = context.socket(zmq.SUB)
    socket.connect(f"tcp://localhost:{params.port}")
    socket.setsockopt(zmq.SUBSCRIBE, b"")

    lcd = LCD1602(params.bus_id)
    lcd.init_lcd()
    lcd.rgb_set_modes()
    lcd.rgb_full_control()
    lcd.set_rgb(220, 220, 220)

    try:
        while True:
            #  Wait for next request from client
            data = json.loads(socket.recv_string())
            
            logging.info(f"Received message: {data}")

            # TODO: handle JSON message

            lcd.clear()
            lcd.write_ascii_string(data)
    finally:
        lcd.clear()
        lcd.rgb_off()
        lcd.close()