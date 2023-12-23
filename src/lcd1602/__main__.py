import argparse
from lcd1602 import LCD1602
from time import sleep
from datetime import datetime

parser = argparse.ArgumentParser("LCD1602 test program")
parser.add_argument("--bus-id", default=3)

if __name__ == "__main__":
    params = parser.parse_args()
    try:
        lcd = LCD1602(params.bus_id)

        lcd.init_lcd()
        lcd.rgb_full_control()
        lcd.set_rgb(150, 220, 40)

        data = [
            0b11111,
            0b10001,
            0b10101,
            0b10001,
            0b10001,
            0b10101,
            0b10001,
            0b11111,
        ]
        addr = lcd.define_char(1, data)

        data = [
            0b00011,
            0b00101,
            0b01001,
            0b10001,
            0b10001,
            0b10001,
            0b10001,
            0b01111,
        ]
        addr = lcd.define_char(0, data)
        lcd.set_cursor_pos(0, 0)
        lcd.write_int(0)
        lcd.write_int(1)
        lcd.set_display_control(True, False, False)
        while True:
            lcd.return_home()
            lcd.write_ascii_string(datetime.now().strftime("%H:%M:%S:%f"))
            sleep(0.5)
        
    finally:
        lcd.clear()
        lcd.rgb_off()
        lcd.close()