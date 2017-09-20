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
    _running = False
    _consumers = {}
    _image_grabber = None

    @classmethod
    def launch(cls, *, debug_image_size=None):
        assert not cls._running
        cls._image_grabber = AsyncImageGrabber(region=(0, 30, 320, 270), debug_image_size=debug_image_size)
        cls._image_grabber.set_callback(cls._on_grabber_update)
        cls._image_grabber.begin_recording()

    @classmethod
    def _on_grabber_update(cls):
        current_image = cls._image_grabber.image
        for consumer in cls._consumers.values():
            consumer.update(current_image)

    @classmethod
    def register_consumer(cls, name, consumer_callback):
        cls._consumers[name] = AsyncConsumer(consumer_callback)

    @classmethod
    def get_image(cls):
        if not cls._image_grabber:
            return None
        return cls._image_grabber.image

    @classmethod
    def get_consumer_result(cls, consumer_name):
        return cls._consumers[consumer_name].result
