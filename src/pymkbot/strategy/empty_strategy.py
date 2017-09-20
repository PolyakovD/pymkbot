from pymkbot.strategy.strategy import Strategy


class EmptyStrategy(Strategy):
    def do_action(self):
        pass

    def _release(self):
        pass
