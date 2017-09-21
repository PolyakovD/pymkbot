from pymkbot.utils.async_executor import AsyncExecutor


class Metastrategy:
    def __init__(self):
        #self._strategy = strategy
        #self._strategy.prepare()
        self._executor = AsyncExecutor()
        self._strategies = {}
        self._halt = True
        self._idx = 0

    def _run_strategy(self, strategy):
        strategy.prepare()
        strategy.resume()

    def _resume_strategy(self, strategy):
        strategy.resume()

    def add_strategy(self, strategy):
        executor = AsyncExecutor()
        executor.call_soon_threadsafe(self._run_strategy(strategy))
        self._strategies[self._idx] = (executor, strategy)
        self._idx += 1

    def _run(self):
        pass

    def run(self):
        self._executor.call_soon_threadsafe(self._run)