from time import strftime

from armagomen._constants import CLOCK
from armagomen.battle_observer.meta.lobby.base_mod_meta import SHOWING_STATUS_TO_VALUE
from armagomen.battle_observer.meta.lobby.date_times_meta import DateTimesMeta
from armagomen.utils.common import ENCODING_ERRORS, ENCODING_LOCALE
from armagomen.utils.events import g_events
from comp7.gui.impl.lobby.hangar.comp7_hangar import Comp7Hangar
from comp7_light.gui.impl.lobby.hangar.comp7_light_hangar import Comp7LightHangar
from gui.impl.lobby.hangar.random.random_hangar import RandomHangar
from last_stand.gui.impl.lobby.hangar_view import HangarView

CONTENT_VIEWS = (RandomHangar, Comp7LightHangar, Comp7Hangar, HangarView)


class DateTimes(DateTimesMeta):

    def _populate(self):
        super(DateTimes, self)._populate()
        g_events.onModSettingsChanged += self.onModSettingsChanged

    def onModSettingsChanged(self, name, data):
        if name == CLOCK.NAME:
            self.as_onSettingsChanged(data)

    def _dispose(self):
        g_events.onModSettingsChanged -= self.onModSettingsChanged
        super(DateTimes, self)._dispose()

    def getTimeString(self):
        return unicode(strftime(self.settings[CLOCK.IN_LOBBY][CLOCK.FORMAT]), ENCODING_LOCALE, ENCODING_ERRORS)

    def onWindowShowingStatusChanged(self, uniqueID, newStatus):
        window = self.gui.windowsManager.getWindow(uniqueID).content
        if isinstance(window, CONTENT_VIEWS) and newStatus in SHOWING_STATUS_TO_VALUE:
            self.setVisible(SHOWING_STATUS_TO_VALUE[newStatus])
