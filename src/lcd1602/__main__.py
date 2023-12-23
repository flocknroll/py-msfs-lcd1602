import lcd1602
import time
import argparse

parser = argparse.ArgumentParser("LCD1602 test program")
parser.add_argument("--bus-id", default=3)

if __name__ == "__main__":
    params = parser.parse_args()
    bus = params.bus_id

    try:
        lcd1602.init_lcd(bus)
        lcd1602.rgb_full_control(3)
        lcd1602.set_rgb(bus, 150, 220, 40)
        lcd1602.write(bus, "test")
        lcd1602.set_cursor_pos(bus, 1, 0)

        lcd1602.write(bus, "123")
        time.sleep(1)
        lcd1602.write(bus, "456")
        time.sleep(1)
        lcd1602.write(bus, "789")

        time.sleep(15)
    finally:
        lcd1602.clear(bus)
        lcd1602.rgb_off(bus)