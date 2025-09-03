from time import strftime

from armagomen._constants import CLOCK
from armagomen.battle_observer.meta.lobby.date_times_meta import DateTimesMeta
from armagomen.utils.common import ENCODING_ERRORS, ENCODING_LOCALE
from armagomen.utils.events import g_events
from comp7.gui.impl.lobby.hangar.comp7_hangar import Comp7Hangar
from comp7_light.gui.impl.lobby.hangar.comp7_light_hangar import Comp7LightHangar
from gui.impl.lobby.crew.container_vews.personal_file.personal_file_view import PersonalFileView
from gui.impl.lobby.crew.container_vews.quick_training.quick_training_view import QuickTrainingView
from gui.impl.lobby.crew.container_vews.service_record.service_record_view import ServiceRecordView
from gui.impl.lobby.crew.container_vews.skills_training.skills_training_view import SkillsTrainingView
from gui.impl.lobby.hangar.random.random_hangar import RandomHangar
from last_stand.gui.impl.lobby.hangar_view import HangarView

CONTENT_VIEWS = (RandomHangar, Comp7LightHangar, Comp7Hangar, HangarView)
NOT_SHOW = (QuickTrainingView, SkillsTrainingView, ServiceRecordView, PersonalFileView)


class DateTimes(DateTimesMeta):

    def __init__(self):
        super(DateTimes, self).__init__()
        self.is_hangar = False

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

    # def onWindowShowingStatusChanged(self, uniqueID, newStatus):
    #     window = self.gui.windowsManager.getWindow(uniqueID).content
    #     if isinstance(window, CONTENT_VIEWS) and newStatus in self.SHOWING_STATUS_TO_VALUE:
    #         self.is_hangar = self.SHOWING_STATUS_TO_VALUE[newStatus]
    #         self.setVisible(self.is_hangar)
    #     if isinstance(window, NOT_SHOW) and newStatus in self.SHOWING_STATUS_TO_VALUE:
    #         self.setVisible(self.is_hangar and not self.SHOWING_STATUS_TO_VALUE[newStatus])

    def onWindowShowingStatusChanged(self, uniqueID, newStatus):
        if newStatus not in self.SHOWING_STATUS_TO_VALUE:
            return

        status_value = self.SHOWING_STATUS_TO_VALUE[newStatus]
        window = self.gui.windowsManager.getWindow(uniqueID).content

        if isinstance(window, CONTENT_VIEWS):
            self.is_hangar = status_value
            self.setVisible(self.is_hangar)
        elif isinstance(window, NOT_SHOW):
            self.setVisible(self.is_hangar and not status_value)
