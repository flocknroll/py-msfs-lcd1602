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

    # Alt char
    ALT_CHAR = lcd.define_char(0,
        [ 0b00111,
          0b00010,
          0b00010,
          0b00100,
          0b01010,
          0b10001,
          0b11111,
          0b10001 ])
    
    # VS char
    VS_CHAR = lcd.define_char(1,
        [ 0b00011,
          0b00010,
          0b00110,
          0b10001,
          0b10001,
          0b10001,
          0b01010,
          0b00100 ])
    
    # Knot char
    KT_CHAR = lcd.define_char(2,
        [ 0b00111,
          0b00010,
          0b00010,
          0b10001,
          0b10010,
          0b11100,
          0b10010,
          0b10001 ])
    
    # Mach char
    MC_CHAR = lcd.define_char(3,
        [ 0b00011,
          0b00100,
          0b00011,
          0b10001,
          0b11011,
          0b10101,
          0b10001,
          0b10001 ])

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
                        lcd.write_int(ALT_CHAR)
                        lcd.write_ascii_string(f"{int(value)}".ljust(7)[0:7])
                    elif name == "AIRSPEED INDICATED":
                        lcd.set_cursor_pos(1, 0)
                        lcd.write_int(KT_CHAR)
                        lcd.write_ascii_string(f"{int(value)}".ljust(7)[0:7])
                    elif name == "AIRSPEED MACH":
                        lcd.set_cursor_pos(1, 8)
                        lcd.write_int(MC_CHAR)
                        lcd.write_ascii_string(f"{value}".ljust(7)[0:7])
                    elif name == "CALCULATED_VS":
                        lcd.set_cursor_pos(0, 8)
                        lcd.write_int(VS_CHAR)
                        lcd.write_ascii_string(f"{int(value)}".ljust(7)[0:7])
                    else:
                        logging.debug(f"Ignored data: {name}")
            elif msg["command"] == "clear":
                lcd.clear()
            elif msg["command"] == "set_rgb":
                lcd.set_rgb(msg["r"], msg["g"], msg["b"])
            else:
                logging.warn(f"Unknown command: {msg['command']}")
    finally:
        lcd.clear()
        lcd.rgb_off()
        lcd.close()

if __name__ == "__main__":
    run()