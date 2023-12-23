import lcd1602
import time
import argparse
from smbus2 import SMBus

parser = argparse.ArgumentParser("LCD1602 test program")
parser.add_argument("--bus-id", default=3)

if __name__ == "__main__":
    params = parser.parse_args()
    try:
        bus = SMBus(params.bus_id)

        lcd1602.init_lcd(bus)
        lcd1602.rgb_full_control(bus)
        lcd1602.set_rgb(bus, 150, 220, 40)

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
        addr = lcd1602.define_char(bus, 1, data)

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
        addr = lcd1602.define_char(bus, 0, data)
        lcd1602.set_cursor_pos(bus, 0, 0)
        lcd1602.write_int(bus, 0)
        lcd1602.write_int(bus, 1)

        time.sleep(15)
    finally:
        lcd1602.clear(bus)
        lcd1602.rgb_off(bus)
        bus.close()