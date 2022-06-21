#!/usr/bin/env python

import argparse
import time
from datetime import datetime
from pynput.mouse import Controller as MouseController
from pynput.keyboard import Key, Controller as KeyboardController

mouse = MouseController()
keyboard = KeyboardController()

needMoveMousePointer = False
isShiftKeyPressed = False
pixelsQuantityToMove = 1
principalMousePointerDirection = 0
secondsToMoveMousePointer = 1
mouse_direction = 0


def set_custom_seconds():
    global secondsToMoveMousePointer, pixelsQuantityToMove, isShiftKeyPressed, needMoveMousePointer, principalMousePointerDirection

    parser = argparse.ArgumentParser(
        description="This program moves the mouse or press a key when it detects that you are away. ")

    parser.add_argument(
        "-s", "--seconds", type=int,
        help="Define seconds for idle")

    parser.add_argument(
        "-p", "--pixels", type=int,
        help="Set how many pixels the mouse should move. Default 1.")

    parser.add_argument(
        "-c", "--circular", action='store_true',
        help="Move mouse in a circle, default movement is diagonally")

    parser.add_argument(
        "-m", "--mode",
        help="Available options: keyboard, mouse, both; default is mouse. ")

    args = parser.parse_args()
    mode = args.mode

    if args.seconds:
        secondsToMoveMousePointer = int(args.seconds)

    if args.pixels:
        pixelsQuantityToMove = int(args.pixels)

    if args.circular:
        principalMousePointerDirection = 1

    is_both_enabled = 'both' == mode
    is_keyboard_enabled = 'keyboard' == mode or is_both_enabled
    is_mouse_enabled = 'mouse' == mode or is_both_enabled or mode is None

    print('---------- S t a r t ----------')
    if is_keyboard_enabled:
        isShiftKeyPressed = True
        print(get_now_timestamp(), "Keyboard is enabled")

    if is_mouse_enabled:
        needMoveMousePointer = True
        print(get_now_timestamp(), "Mouse is enabled, moving", pixelsQuantityToMove, 'pixels',
              '(circularly)' if principalMousePointerDirection == 1 else '')

    print(get_now_timestamp(), 'Running every', str(secondsToMoveMousePointer), 'seconds')
    print('---------- E n d ----------')


def move_mouse_when_unable_to_move(expected_mouse_position):
    if expected_mouse_position != mouse.position:
        mouse.position = (pixelsQuantityToMove, pixelsQuantityToMove)


def move_mouse():
    print('Actual position', mouse.position)
    global mouse_direction
    delta_x = pixelsQuantityToMove if mouse_direction == 0 or mouse_direction == 3 else -pixelsQuantityToMove
    delta_y = pixelsQuantityToMove if mouse_direction == 0 or mouse_direction == 1 else -pixelsQuantityToMove
    new_x = currentPosition[0] + delta_x
    new_y = currentPosition[1] + delta_y
    mouse_direction = (mouse_direction + principalMousePointerDirection) % 4
    mouse.position = (new_x, new_y)
    print('Mouse position in line 98', mouse.position)
    move_mouse_when_unable_to_move(mouse.position)
    current_position = mouse.position
    print(get_now_timestamp(), 'Moved mouse to: ', current_position)
    return current_position


def press_shift_key():
    keyboard.press(Key.shift)
    keyboard.release(Key.shift)
    print(get_now_timestamp(), 'Shift key pressed')


def get_now_timestamp():
    now = datetime.now()
    return now.strftime("%H:%M:%S")


def execute_keep_awake_action():
    print(get_now_timestamp(), 'Idle detection')

    if needMoveMousePointer:
        move_mouse()

    if isShiftKeyPressed:
        press_shift_key()


set_custom_seconds()
lastSavePosition = (0, 0)

while 1:
    currentPosition = mouse.position
    is_user_away = currentPosition == lastSavePosition
    if is_user_away:
        execute_keep_awake_action()
        currentPosition = mouse.position
    if not is_user_away:
        print('Actual position', mouse.position)
        print(get_now_timestamp(), 'User activity detected')
    lastSavePosition = currentPosition
    time.sleep(secondsToMoveMousePointer)
    print('----------- Next iteration -----------')
