# SPDX-FileCopyrightText: 2021 Kattni Rembor for Adafruit Industries
#
# SPDX-License-Identifier: MIT

"""NeoKey Trinkey Capacitive Touch and HID Keyboard example"""
import time
import board
import neopixel
import usb_hid
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keyboard_layout_us import KeyboardLayoutUS
from adafruit_hid.keycode import Keycode  # pylint: disable=unused-import
from digitalio import DigitalInOut, Pull
import touchio
import random

print("NeoKey Trinkey HID")

# create the pixel and turn it off
pixel = neopixel.NeoPixel(board.NEOPIXEL, 1, brightness=0.1)
pixel.fill(0x0)
brightVal = 0.1

time.sleep(1)  # Sleep for a bit to avoid a race condition on some systems
keyboard = Keyboard(usb_hid.devices)
keyboard_layout = KeyboardLayoutUS(keyboard)  # We're in the US :)

# create the switch, add a pullup, start it with not being pressed
button = DigitalInOut(board.SWITCH)
button.switch_to_input(pull=Pull.DOWN)
button_state = False

# create the captouch element and start it with not touched
touch = touchio.TouchIn(board.TOUCH)
touch_state = False

# our helper function will press the keys themselves
def make_keystrokes(keys, delay):
    if isinstance(keys, str):  # If it's a string...
        keyboard_layout.write(keys)  # ...Print the string
    elif isinstance(keys, int):  # If its a single key
        keyboard.press(keys)  # "Press"...
        keyboard.release_all()  # ..."Release"!
    elif isinstance(keys, (list, tuple)):  # If its multiple keys
        keyboard.press(*keys)  # "Press"...
        keyboard.release_all()  # ..."Release"!
    time.sleep(delay)
    
def setColor():
    hexadecimal = ""+''.join(random.choice('ABCDEF0123456789') for i in range(6))
    newhex = int(hexadecimal, 16)
    # print(newhex)
    pixel.fill((newhex))
    pixel.show()
    return newhex
    
while True:
    if button.value and not button_state:
        set = setColor()
        print(set)
        print("Button pressed.")
        button_state = True

    if not button.value and button_state:
        print("Button released.")
        print("when released the brightness was")
        print(brightVal)
        button_state = False

    if touch.value and not touch_state:
        print("Touched!")
        
        touch_state = True
    if not touch.value and touch_state:
        print("Untouched!")
        print(brightVal)
        currentBright = brightVal
        
        if currentBright >= 0.99:
            currentBright = 0.1
            brightVal = 0.1
            pixel.brightness = 0.1
        elif currentBright < 0.99:
            inc = currentBright + 0.1
            pixel.brightness = inc
            brightVal = inc
        touch_state = False
