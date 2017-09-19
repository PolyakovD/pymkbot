from datetime import datetime
from pymkbot.strategy.strategy import Strategy


class EmptyStrategy(Strategy):
    def do_action(self):
        pass
        # print("current time - " + str(datetime.now()))
