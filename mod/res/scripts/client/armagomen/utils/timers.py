from collections import namedtuple
from functools import partial

from armagomen.utils.common import addCallback, cancelCallback
from SoundGroups import g_instance

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

    def __init__(self):
        super(SixthSenseTimer, self).__init__()
        self.__sounds = dict()
        self.__soundID = None

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

    def setSound(self, soundID):
        self.__soundID = soundID

    def handleTimer(self, seconds):
        self.cancelCallback()
        raise NotImplementedError

    def timeTicking(self, seconds):
        self.cancelCallback()
        if seconds > CONSTANTS.ZERO:
            self._callback = addCallback(CONSTANTS.ONE_SECOND, partial(self.timeTicking, seconds - CONSTANTS.ONE))
            if self.__soundID is not None:
                self.callWWISE(self.__soundID)
        self.handleTimer(seconds)

    def destroyTimer(self):
        for sound in self.__sounds.values():
            sound.stop()
        self.__sounds.clear()
        self.__soundID = None


class CyclicTimerEvent(Timer):
    __slots__ = ("_interval", "_callback", "_function")

    def __init__(self, updateInterval, function):
        super(CyclicTimerEvent, self).__init__()
        self._interval = float(updateInterval)
        self._function = function

    def update(self):
        self._callback = addCallback(self._interval, self.update)
        self._function()

    def start(self):
        super(CyclicTimerEvent, self).start()
        self.update()
