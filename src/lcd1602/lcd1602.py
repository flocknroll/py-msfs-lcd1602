from smbus2 import SMBus
from time import sleep

# I2C addresses
LCD_ADDRESS = 0x3e
RGB_ADDRESS = 0x60

## Masks
# Register selection
LCD_INSTR_REG = 1 << 7  # No R/S bit (instruction) but control bit set for command data
LCD_DATA_REG  = 1 << 6  # R/S bit set (data) but no control bit set -> data stream

RGB_MODE1_REG      = 0x00
RGB_MODE2_REG      = 0x01
RGB_BLUE_PWM_REG   = 0x02
RGB_GREEN_PWM_REG  = 0x03
RGB_RED_PWM_REG    = 0x04
RGB_GROUP_PWM_REG  = 0x06   # if DMBLNK = 0
RGB_GROUP_BLINK_DUTY_CYCLE_REG = 0x06   # if DMBLNK = 1
RGB_GROUP_BLINK_PERIOD_REG     = 0x07   # if DMBLNK = 1
RGB_LED_OUTPUT_REG = 0x08

# Function set
FUNCTION_SET_CMD = 1 << 5   # 0x20
FS_1_LINE_MODE   = 0
FS_2_LINES_MODE  = 1 << 3
FS_8BIT_MODE     = 1 << 4
FS_4BIT_MODE     = 0
FS_SMALL_FONT    = 0
FS_BIG_FONT      = 1 << 2

# Display control
DISPLAY_CONTROL_CMD = 1 << 3    # 0x08
DC_DISPLAY_ON       = 1 << 2
DC_DISPLAY_OFF      = 0
DC_CURSOR_ON        = 1 << 1
DC_CURSOR_OFF       = 0
DC_BLINK_ON         = 1
DC_BLINK_OFF        = 0

# Display clear
DISPLAY_CLEAR_CMD = 1

# Entry mode set
ENTRY_MODE_SET_CMD   = 1 << 2 # 0x04
EM_MOVE_RIGHT        = 1 << 1
EM_MOVE_LEFT         = 0
EM_SHIFT_DISPLAY_ON  = 1
EM_SHIFT_DISPLAY_OFF = 0

# Set DDRAM address
DDRAM_ADR_SET_CMD = 1 << 7  # 0x80
DDRAM_SECOND_ROW  = 0x40

# Set CGRAM address
CGRAM_ADR_SET_CMD = 1 << 6  # 0x40

# Return home
RETURN_HOME_CMD = 1 << 1  # 0x02

DEFAULT_WAIT = 0.0004

class LCD1602:
    def __init__(self, bus_id: int):
        self.bus = SMBus(bus_id)

    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_value, traceback):
        self.close()

    def close(self):
        self.bus.close()

    def clear(self):
        self.bus.write_byte_data(LCD_ADDRESS, LCD_INSTR_REG, DISPLAY_CLEAR_CMD)
        self.cursor_pos = 0
        sleep(0.0015)

    def return_home(self):
        self.bus.write_byte_data(LCD_ADDRESS, LCD_INSTR_REG, RETURN_HOME_CMD)
        self.cursor_pos = 0
        sleep(0.0015)

    def set_function(self, two_lines: bool=True, eight_bit_mode: bool=False, big_font: bool=False):
        cmd = FUNCTION_SET_CMD
        cmd |= FS_2_LINES_MODE if two_lines else FS_1_LINE_MODE
        cmd |= FS_8BIT_MODE if eight_bit_mode else FS_4BIT_MODE
        cmd |= FS_BIG_FONT if big_font else FS_SMALL_FONT

        self.bus.write_byte_data(LCD_ADDRESS, LCD_INSTR_REG, cmd)
        sleep(DEFAULT_WAIT)

    def set_display_control(self, on: bool=True, cursor: bool=True, blink: bool=True):
        cmd = DISPLAY_CONTROL_CMD
        cmd |= DC_DISPLAY_ON if on else DC_DISPLAY_OFF
        cmd |= DC_CURSOR_ON if cursor else DC_CURSOR_OFF
        cmd |= DC_BLINK_ON if blink else DC_BLINK_OFF

        self.bus.write_byte_data(LCD_ADDRESS, LCD_INSTR_REG, cmd)
        sleep(DEFAULT_WAIT)

    def set_entry_mode(self, shift_display: bool=False, left_dir: bool=False):
        cmd = ENTRY_MODE_SET_CMD
        cmd |= EM_SHIFT_DISPLAY_ON if shift_display else EM_SHIFT_DISPLAY_OFF
        cmd |= EM_MOVE_LEFT if left_dir else EM_MOVE_RIGHT

        self.bus.write_byte_data(LCD_ADDRESS, LCD_INSTR_REG, cmd)
        sleep(DEFAULT_WAIT)

    def set_cursor_pos(self, row: int, col: int):
        addr = row * DDRAM_SECOND_ROW + col

        self.bus.write_byte_data(LCD_ADDRESS, LCD_INSTR_REG, DDRAM_ADR_SET_CMD | addr)
        sleep(DEFAULT_WAIT)

    def define_char(self, index: int, data: list) -> int:
        if index > 7:
            raise Exception("Only 8 CGRAM slots")
        addr = index << 3
        
        self.bus.write_byte_data(LCD_ADDRESS, LCD_INSTR_REG, CGRAM_ADR_SET_CMD | addr)
        sleep(DEFAULT_WAIT)
        for i in range(8):
            self.bus.write_byte_data(LCD_ADDRESS, LCD_DATA_REG, data[i])
            sleep(DEFAULT_WAIT)

        return index

    def init_lcd(self, two_lines: bool=True, eight_bit_mode: bool=False, big_font: bool=False, on: bool=True, cursor: bool=True, blink: bool=True, shift_display: bool=False, left_dir: bool=False):
        self.set_function(two_lines, eight_bit_mode, big_font)
        self.set_display_control(on, cursor, blink)
        self.clear()
        self.set_entry_mode(shift_display, left_dir)

    def write_ascii_string(self, text: str):
        self.bus.write_i2c_block_data(LCD_ADDRESS, LCD_DATA_REG, [c for c in text.encode("ascii")])
        sleep(DEFAULT_WAIT)

    def write_int_array(self, data: list):
        self.bus.write_i2c_block_data(LCD_ADDRESS, LCD_DATA_REG, data)
        sleep(DEFAULT_WAIT)

    def write_int(self, value: int):
        self.bus.write_byte_data(LCD_ADDRESS, LCD_DATA_REG, value)
        sleep(DEFAULT_WAIT)



    def rgb_full_on(self):
        self.bus.write_byte_data(RGB_ADDRESS, RGB_LED_OUTPUT_REG, 0x55)  # Full ON

    def rgb_full_control(self):
        self.bus.write_byte_data(RGB_ADDRESS, RGB_LED_OUTPUT_REG, 0xFF)  # Full control

        # TODO: set mode 1 & 2

        # No blinking
        self.bus.write_byte_data(RGB_ADDRESS, RGB_GROUP_BLINK_DUTY_CYCLE_REG, 255)
        self.bus.write_byte_data(RGB_ADDRESS, RGB_GROUP_BLINK_PERIOD_REG, 0)

    def set_rgb(self, r: int, g: int, b: int):
        self.bus.write_byte_data(RGB_ADDRESS, RGB_RED_PWM_REG, r)
        self.bus.write_byte_data(RGB_ADDRESS, RGB_GREEN_PWM_REG, g)
        self.bus.write_byte_data(RGB_ADDRESS, RGB_BLUE_PWM_REG, b)

    def rgb_off(self):
        self.bus.write_byte_data(RGB_ADDRESS, RGB_LED_OUTPUT_REG, 0)  # Full OFF