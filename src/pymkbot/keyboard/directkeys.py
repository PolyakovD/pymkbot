# This code is licensed under: https://creativecommons.org/licenses/by-sa/3.0/ since it's coming from stackoverflow.
# direct inputs
# source to this solution and code:
# http://stackoverflow.com/questions/14489013/simulate-python-keypresses-for-controlling-a-game
# http://www.gamespp.com/directx/directInputKeyboardScanCodes.html

import ctypes
import time

SendInput = ctypes.windll.user32.SendInput

kbd_player1 = {
    'HIGH_KICK': 0x18,
    'LOW_KICK': 0x19,
    'HIGH_PUNCH': 0x16,
    'LOW_PUNCH': 0x24,
    'BLOCK': 0x39,
    'STEP_IN': 0x21,
    'STEP_OUT': 0x13,
    'RUN': 0x10,
    'START': 0x14,
    'UP': 0x11,
    'LEFT': 0x1E,
    'DOWN': 0x1F,
    'RIGHT': 0x20}

kbd_player2 = {
    'HIGH_KICK': 0x4D,
    'LOW_KICK': 0x51,
    'HIGH_PUNCH': 0x4B,
    'LOW_PUNCH': 0x4F,
    'BLOCK': 0x52,
    'STEP_IN': 0x47,
    'STEP_OUT': 0x49,
    'RUN': 0x4C,
    'START': 0x51,
    'UP': 0x2F,
    'LEFT': 0x30,
    'DOWN': 0x31,
    'RIGHT': 0x32}



# C struct redefinitions
PUL = ctypes.POINTER(ctypes.c_ulong)


class KeyBdInput(ctypes.Structure):
    _fields_ = [("wVk", ctypes.c_ushort),
                ("wScan", ctypes.c_ushort),
                ("dwFlags", ctypes.c_ulong),
                ("time", ctypes.c_ulong),
                ("dwExtraInfo", PUL)]


class HardwareInput(ctypes.Structure):
    _fields_ = [("uMsg", ctypes.c_ulong),
                ("wParamL", ctypes.c_short),
                ("wParamH", ctypes.c_ushort)]


class MouseInput(ctypes.Structure):
    _fields_ = [("dx", ctypes.c_long),
                ("dy", ctypes.c_long),
                ("mouseData", ctypes.c_ulong),
                ("dwFlags", ctypes.c_ulong),
                ("time", ctypes.c_ulong),
                ("dwExtraInfo", PUL)]


class Input_I(ctypes.Union):
    _fields_ = [("ki", KeyBdInput),
                ("mi", MouseInput),
                ("hi", HardwareInput)]


class Input(ctypes.Structure):
    _fields_ = [("type", ctypes.c_ulong),
                ("ii", Input_I)]


# Actuals Functions


def press_key(hex_key_code):
    if isinstance(hex_key_code, tuple):
        for single_code in hex_key_code:
            press_key(single_code)
        return
    extra = ctypes.c_ulong(0)
    ii_ = Input_I()
    ii_.ki = KeyBdInput(0, hex_key_code, 0x0008, 0, ctypes.pointer(extra))
    x = Input(ctypes.c_ulong(1), ii_)
    ctypes.windll.user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))


def release_key(hex_key_code):
    if isinstance(hex_key_code, tuple):
        for single_code in hex_key_code:
            release_key(single_code)
        return
    extra = ctypes.c_ulong(0)
    ii_ = Input_I()
    ii_.ki = KeyBdInput(0, hex_key_code, 0x0008 | 0x0002, 0, ctypes.pointer(extra))
    x = Input(ctypes.c_ulong(1), ii_)
    ctypes.windll.user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))


if __name__ == '__main__':
    press_key(0x11)
    time.sleep(1)
    release_key(0x11)
    time.sleep(1)
