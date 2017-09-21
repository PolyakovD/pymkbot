import time

from pymkbot.keyboard.directkeys import keyboard, press_key, release_key

class MenuControl:
    def __init__(self):
        self._keybindings = keyboard[0]

    def move(self, direction):
        press_key(self._keybindings[direction])
        time.sleep(0.05)
        release_key(self._keybindings[direction])
        time.sleep(0.05)

    def select(self):
        press_key(self._keybindings['BLOCK'])
        time.sleep(0.05)
        release_key(self._keybindings['BLOCK'])
        time.sleep(0.05)

    def start(self):
        press_key(self._keybindings['START'])
        time.sleep(0.05)
        release_key(self._keybindings['START'])
        time.sleep(0.05)