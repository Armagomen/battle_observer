from time import strftime

from armagomen._constants import CLOCK
from armagomen.battle_observer.meta.lobby.date_times_meta import DateTimesMeta
from armagomen.utils.common import ENCODING_ERRORS, ENCODING_LOCALE
from armagomen.utils.events import g_events
from frameworks.wulf.gui_constants import ShowingStatus
from gui.impl.lobby.hangar.random.random_hangar import HangarWindow
from helpers import dependency
from skeletons.gui.impl import IGuiLoader

SHOWING_STATUS_TO_VALUE = {ShowingStatus.SHOWN.value: True, ShowingStatus.HIDDEN.value: False}


class DateTimes(DateTimesMeta):
    gui = dependency.descriptor(IGuiLoader)

    def _populate(self):
        super(DateTimes, self)._populate()
        g_events.onModSettingsChanged += self.onModSettingsChanged
        self.gui.windowsManager.onWindowShowingStatusChanged += self.onWindowShowingStatusChanged

    def onModSettingsChanged(self, name, data):
        if name == CLOCK.NAME:
            self.as_onSettingsChanged(data)

    def _dispose(self):
        g_events.onModSettingsChanged -= self.onModSettingsChanged
        self.gui.windowsManager.onWindowShowingStatusChanged -= self.onWindowShowingStatusChanged
        super(DateTimes, self)._dispose()

    def getTimeString(self):
        return unicode(strftime(self.settings[CLOCK.IN_LOBBY][CLOCK.FORMAT]), ENCODING_LOCALE, ENCODING_ERRORS)

    def onWindowShowingStatusChanged(self, uniqueID, newStatus):
        window = self.gui.windowsManager.getWindow(uniqueID)
        if isinstance(window, HangarWindow) and newStatus in SHOWING_STATUS_TO_VALUE:
            self.setVisible(SHOWING_STATUS_TO_VALUE[newStatus])
