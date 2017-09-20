from pymkbot.image.async_image_grabber import AsyncImageGrabber
from pymkbot.utils.async_executor import AsyncExecutor


class AsyncConsumer:
    def __init__(self, callback):
        self._working = False
        self._updated = False
        self._callback = callback
        self._executor = AsyncExecutor()
        self._current_image = None
        self._current_result = None

    def _process(self):
        self._working = True
        self._updated = False
        img = self._current_image.copy()
        res = self._callback(img)
        if res is not None:
            self._current_result = res
        if self._updated:
            self._process()
        else:
            self._working = False

    def update(self, current_image):
        self._current_image = current_image
        self._updated = True
        if self._working:
            return
        self._executor.call_soon_threadsafe(self._process)

    @property
    def result(self):
        return self._current_result.copy()


class AsyncImageProvider:
    def __init__(self, *, debug_image_size=None):
        self._consumers = []
        self._image_grabber = AsyncImageGrabber(region=(0, 30, 320, 270), debug_image_size=debug_image_size)
        self._image_grabber.set_callback(self._on_grabber_update)
        self._image_grabber.begin_recording()

    def _on_grabber_update(self):
        current_image = self._image_grabber.image
        for consumer in self._consumers:
            consumer.update(current_image)

    def register_consumer(self, consumer_callback):
        self._consumers.append(AsyncConsumer(consumer_callback))
