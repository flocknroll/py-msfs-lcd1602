import lcd1602


if __name__ == "__main__":
    lcd1602.init_lcd(3)
    lcd1602.write(3, "test")
    lcd1602.set_cursor(3, 1, 5)
    lcd1602.write(3, "TEST")