from SoundGroups import g_instance

from armagomen.utils.common import callback, cancelCallback


class CONSTANTS:
    def __init__(self):
        pass

    COUNTDOWN_TICKING = 'time_countdown'
    STOP_TICKING = 'time_countdown_stop'
    ONE_SECOND = 1.0
    ZERO = 0
    ONE = 1


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

    def start(self, *args):
        if self._callback is not None:
            self.stop()


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
        sound = g_instance.getSound2D(wwiseEventName)
        if sound is not None:
            sound.play()
            self.__sounds[wwiseEventName] = sound

    def stop(self):
        super(SixthSenseTimer, self).stop()
        if self._play_sound and self._isTicking:
            self.callWWISE(CONSTANTS.STOP_TICKING)
            self._isTicking = False

    def timeTicking(self, seconds):
        if seconds > CONSTANTS.ZERO:
            self._callback = callback(CONSTANTS.ONE_SECOND, lambda: self.timeTicking(seconds - CONSTANTS.ONE))
            self._func_update(seconds)
        else:
            self.stop()

    def start(self, seconds):
        super(SixthSenseTimer, self).start()
        self.timeTicking(seconds)
        if self._play_sound and not self._isTicking:
            self.callWWISE(CONSTANTS.COUNTDOWN_TICKING)
            self._isTicking = True

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
        self._callback = callback(self._interval, self.update)
        self._function()

    def start(self):
        super(CyclicTimerEvent, self).start()
        self.update()
