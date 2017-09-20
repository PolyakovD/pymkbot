import json
import os
from pathlib import Path

import cv2

from pymkbot.image.async_image_provider import AsyncImageProvider


class GoodMovesSerializer:
    def __init__(self, strat, path):
        self._strat = strat
        self._path = Path(path)
        self._idx = 0

    def load(self):
        moves = []
        for file in os.listdir(str(self._path)):
            name, ext = os.path.splitext(file)
            try:
                idx = int(name)
                if idx >= self._idx:
                    self._idx = idx + 1
            except:
                pass
            if ext == 'json':
                with open(str(self._path / file), 'r') as f:
                    move = json.load(f)
                    moves.append(move)
        self._strat.add_good_moves(moves)

    def on_save_coomand(self):
        moves = self._strat.remember()
        img = cv2.cvtColor(AsyncImageProvider.get_image().copy(), cv2.COLOR_RGB2BGR)
        cv2.imwrite(str(self._path / (str(self._idx) + '.png')), img)
        with open(str(self._path / (str(self._idx) + '.json')), 'w') as f:
            json.dump(moves, f)
        self._idx += 1