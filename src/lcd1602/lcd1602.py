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
ENTRY_MODE_SET_CMD = 1 << 2 # 0x04
EM_MOVE_RIGHT      = 1 << 1
EM_MOVE_LEFT       = 0
EM_SHIFT_DISPLAY   = 1

# Set DDRAM address
DDRAM_ADR_SET_CMD = 1 << 7  # 0x80
DDRAM_SECOND_ROW  = 0x40


def clear(bus_id: int):
    bus = SMBus(bus_id)

    bus.write_byte_data(LCD_ADDRESS, LCD_INSTR_REG, DISPLAY_CLEAR_CMD)
    sleep(0.0015)


def init_lcd(bus_id: int):
    bus = SMBus(bus_id)

    bus.write_byte_data(LCD_ADDRESS, LCD_INSTR_REG, FUNCTION_SET_CMD | FS_2_LINES_MODE | FS_4BIT_MODE | FS_SMALL_FONT)
    sleep(0.0004)

    bus.write_byte_data(LCD_ADDRESS, LCD_INSTR_REG, DISPLAY_CONTROL_CMD | DC_DISPLAY_ON | DC_CURSOR_ON | DC_BLINK_ON)
    sleep(0.0004)

    clear(bus_id)

    bus.write_byte_data(LCD_ADDRESS, LCD_INSTR_REG, ENTRY_MODE_SET_CMD | EM_MOVE_RIGHT)
    sleep(0.0004)


def set_cursor(bus_id: int, row: int, col: int):
    bus = SMBus(bus_id)

    addr = row * DDRAM_SECOND_ROW + col 

    bus.write_byte_data(LCD_ADDRESS, LCD_INSTR_REG, DDRAM_ADR_SET_CMD | addr)
    sleep(0.0004)


def write(bus_id: int, text: str):
    bus = SMBus(bus_id)
    bus.write_i2c_block_data(LCD_ADDRESS, LCD_DATA_REG, [c for c in text.encode("ascii")])


def rgb_full_on(bus_id: int):
    bus = SMBus(bus_id)
    bus.write_byte_data(RGB_ADDRESS, RGB_LED_OUTPUT_REG, 0x55)  # Full ON

def rgb_full_control(bus_id: int):
    bus = SMBus(bus_id)
    bus.write_byte_data(RGB_ADDRESS, RGB_LED_OUTPUT_REG, 0xFF)  # Full control

    # TODO: set mode 1 & 2

    # No blinking
    bus.write_byte_data(RGB_ADDRESS, RGB_GROUP_BLINK_DUTY_CYCLE_REG, 255)
    bus.write_byte_data(RGB_ADDRESS, RGB_GROUP_BLINK_PERIOD_REG, 0)

def set_rgb(bus_id: int, r: int, g: int, b: int):
    bus = SMBus(bus_id)

    bus.write_byte_data(RGB_ADDRESS, RGB_RED_PWM_REG, r)
    bus.write_byte_data(RGB_ADDRESS, RGB_GREEN_PWM_REG, g)
    bus.write_byte_data(RGB_ADDRESS, RGB_BLUE_PWM_REG, b)

def rgb_off(bus_id: int):
    bus = SMBus(bus_id)
    bus.write_byte_data(RGB_ADDRESS, RGB_LED_OUTPUT_REG, 0)  # Full OFF