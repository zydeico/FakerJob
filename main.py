import argparse
import time
from datetime import datetime
from pynput.mouse import Controller as MouseController
from pynput.keyboard import Key, Controller as KeyboardController

mouse = MouseController()
keyboard = KeyboardController()

move_mouse = False
press_shift_key = False
pixels_to_move = 1
mouse_direction_delta = 0

moveMouseEveySeconds = 20
mouseDirection = 0


def define_custom_seconds():
    global moveMouseEveySeconds, pixels_to_move, press_shift_key, move_mouse, mouse_direction_delta
    parser = argparse.ArgumentParser(description="Move mouse pointer every X seconds to X pixels")

    parser.add_argument("-s", "--seconds", type=int,
                        help="Define in seconds how long to wait after a user is considered idle. Default 300.")

    parser.add_argument("-p", "--pixels", type=int,
                        help="Define how pixels has been moved the mouse pointer")

    parser.add_argument("-c", "--circular", action="store_true", help="Move mouse in circular mode")

    parser.add_argument("-m", "--mode", help="Available options")

    args = parser.parse_args()
    mode = args.mode

    if args.seconds:
        moveMouseEveySeconds = int(args.seconds)

    if args.pixels:
        pixels_to_move = int(args.pixels)

    if args.circular:
        mouse_direction_delta = 1

    