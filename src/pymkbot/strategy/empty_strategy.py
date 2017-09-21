from pymkbot.strategy.strategy import Strategy


class EmptyStrategy(Strategy):
    def _release(self):
        pass

    def stop(self):
        pass

    def resume(self):
        pass