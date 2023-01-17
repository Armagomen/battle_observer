from collections import namedtuple
from functools import partial

from SoundGroups import g_instance
from armagomen.utils.common import callback, cancelCallback

CONSTANTS = namedtuple("CONSTANTS", ("ONE_SECOND", "ZERO", "ONE"))(1.0, 0, 1)


class Timer(object):
    __slots__ = ("_callback",)

    def __init__(self):
        self._callback = None

    def cancelCallback(self):
        if self._callback is not None:
            cancelCallback(self._callback)
            self._callback = None

    def stop(self):
        self.cancelCallback()

    def start(self, *args):
        self.cancelCallback()


class SixthSenseTimer(Timer):
    __slots__ = ("_callback", "_func_hide", "_func_update", "_play_sound", "__sounds", "__soundID")

    def __init__(self, update, hide, soundID=None):
        super(SixthSenseTimer, self).__init__()
        self._func_update = update
        self._func_hide = hide
        self.__sounds = dict()
        self.__soundID = soundID

    def callWWISE(self, wwiseEventName):
        if wwiseEventName in self.__sounds:
            sound = self.__sounds[wwiseEventName]
        else:
            sound = g_instance.getSound2D(wwiseEventName)
            self.__sounds[wwiseEventName] = sound
        if sound is not None:
            if sound.isPlaying:
                sound.stop()
            sound.play()

    def timeTicking(self, seconds):
        self._callback = None
        if seconds <= CONSTANTS.ZERO:
            return self._func_hide()
        self._callback = callback(CONSTANTS.ONE_SECOND, partial(self.timeTicking, seconds - CONSTANTS.ONE))
        self._func_update(seconds)
        if self.__soundID is not None:
            self.callWWISE(self.__soundID)

    def start(self, seconds):
        super(SixthSenseTimer, self).start()
        self.timeTicking(seconds)

    def destroy(self):
        for sound in self.__sounds.values():
            sound.stop()
        self.__sounds.clear()


class CyclicTimerEvent(Timer):
    __slots__ = ("_interval", "_callback", "_func_hide", "_function")

    def __init__(self, updateInterval, function):
        super(CyclicTimerEvent, self).__init__()
        self._interval = float(updateInterval)
        self._function = function

    def update(self):
        self._callback = None
        self._callback = callback(self._interval, self.update)
        self._function()

    def start(self):
        super(CyclicTimerEvent, self).start()
        self.update()
