import zmq
import argparse
import logging
import json

from py_msfs_lcd1602.driver import LCD1602


parser = argparse.ArgumentParser("LCD1602 controller backend")
parser.add_argument("--bus-id", default=3)
parser.add_argument("--port", default=5555)

def run():
    logging.basicConfig(level=logging.INFO)

    params = parser.parse_args()

    context = zmq.Context()
    socket = context.socket(zmq.SUB)
    socket.connect(f"tcp://localhost:{params.port}")
    socket.setsockopt(zmq.SUBSCRIBE, b"")

    lcd = LCD1602(params.bus_id)
    lcd.init_lcd(cursor=False, blink=False)
    lcd.rgb_set_modes()
    lcd.rgb_full_control()
    lcd.set_rgb(220, 220, 220)

    try:
        while True:
            #  Wait for next request from client
            raw = socket.recv_string()
            msg = json.loads(raw)
            
            logging.info(f"Received message: {msg}")

            if msg["command"] == "update_data":
                for d in msg["data"]:
                    name = d["name"]
                    value = d["value"]

                    if name == "INDICATED ALTITUDE":
                        lcd.set_cursor_pos(0, 0)
                        lcd.write_ascii_string(f"{value}ft")
                    elif name == "AIRSPEED INDICATED":
                        lcd.set_cursor_pos(1, 0)
                        lcd.write_ascii_string(f"{value}kts")
                    elif name == "AIRSPEED MACH":
                        pass
                    elif name == "VERTICAL SPEED":
                        lcd.set_cursor_pos(0, 8)
                        lcd.write_ascii_string(f"{value}ft/s")
                    else:
                        logging.warn(f"Unknown data: {name}")
            elif msg["command"] == "clear":
                lcd.clear()
            else:
                logging.warn(f"Unknown command: {msg['command']}")
    finally:
        lcd.clear()
        lcd.rgb_off()
        lcd.close()

if __name__ == "__main__":
    run()