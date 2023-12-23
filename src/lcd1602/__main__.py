import lcd1602
import time

if __name__ == "__main__":
    try:
        lcd1602.init_lcd(3)
        lcd1602.rgb_full_control(3)
        lcd1602.set_rgb(3, 150, 220, 40)
        lcd1602.write(3, "test")
        lcd1602.set_cursor(3, 1, 5)
        lcd1602.write(3, "TEST")

        time.sleep(15)
    finally:
        lcd1602.clear(3)
        lcd1602.rgb_off(3)