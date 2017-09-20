import asyncio
from threading import Thread, Condition


class AsyncExecutor:
    def __init__(self):
        self._ready = Condition()
        self._ready.acquire()
        self._thread = Thread(target=self._init_executor)
        self._thread.daemon = True
        self._loop = None
        self._thread.start()
        self._ready.wait()
        self._ready.release()

    def _init_executor(self):
        self._loop = asyncio.new_event_loop()
        self._ready.acquire()
        self._ready.notify()
        self._ready.release()
        self._loop.run_forever()

    @asyncio.coroutine
    def _wrap_func(self, func, *args, **kwargs):
        return func(*args, **kwargs)

    def map(self, func, *args, **kwargs):
        return self._loop.create_task(self._wrap_func(func, *args, **kwargs))

    def run(self, func, *args, **kwargs):
        return self._loop.create_task(func(*args, **kwargs))

    def call_soon_threadsafe(self, func, *args, **kwargs):
        self._loop.call_soon_threadsafe(func, *args, **kwargs)
