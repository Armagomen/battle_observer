import SoundGroups
from gui.Scaleform.daapi.view.battle.shared.battle_timers import _WWISE_EVENTS
from .common import callback, cancelCallback
from ..bo_constants import GLOBAL


class Timer(object):
    __slots__ = ("_callback", "_func_hide")

    def __init__(self):
        self._callback = None
        self._func_hide = None

    def stop(self):
        """handle stop timer, callback will be stopped on next cycle tick after timeout"""
        if self._callback is not None:
            cancelCallback(self._callback)
            self._callback = None
            if self._func_hide is not None:
                self._func_hide()


class SixthSenseTimer(Timer):
    __slots__ = ("_callback", "_func_hide", "_func_update", "_isTicking", "_play_sound", "__sounds")

    def __init__(self, update, hide, play_sound):
        super(SixthSenseTimer, self).__init__()
        self._func_update = update
        self._play_sound = play_sound
        self._func_hide = hide
        self._isTicking = False
        self.__sounds = dict()

    def callWWISE(self, wwiseEventName):
        sound = SoundGroups.g_instance.getSound2D(wwiseEventName)
        if sound is not None:
            if sound.isPlaying:
                sound.restart()
            else:
                sound.play()
            self.__sounds[wwiseEventName] = sound

    def stop(self):
        super(SixthSenseTimer, self).stop()
        for sound in self.__sounds.values():
            sound.stop()
        self.__sounds.clear()

    def start(self, seconds):
        if seconds > 0:
            if self._callback is not None:
                cancelCallback(self._callback)
                self._callback = None
            self._func_update(seconds)
            seconds -= GLOBAL.ONE
            self._callback = callback(GLOBAL.ONE_SECOND, lambda: self.start(seconds))
            if self._play_sound and not self._isTicking:
                self.callWWISE(_WWISE_EVENTS.COUNTDOWN_TICKING)
                self._isTicking = True
        else:
            if self._play_sound and self._isTicking:
                self._isTicking = False
            self.stop()

    @property
    def callback(self):
        return self._callback


class CyclicTimerEvent(Timer):
    __slots__ = ("_interval", "_callback", "_func_hide", "_function")

    def __init__(self, updateInterval, function):
        super(CyclicTimerEvent, self).__init__()
        self._interval = float(updateInterval)
        self._function = function

    def start(self):
        self._function()
        self._callback = callback(self._interval, self.start)
