from time import strftime

from armagomen._constants import CLOCK, GLOBAL
from armagomen.battle_observer.meta.lobby.date_times_meta import DateTimesMeta
from armagomen.utils.common import ENCODING_ERRORS, ENCODING_LOCALE, safe_import
from armagomen.utils.events import g_events
from armagomen.utils.logging import logDebug
from gui.shared.utils.TimeInterval import TimeInterval


def import_views():
    content = safe_import((
        ("battle_royale.gui.impl.lobby.views.battle_royale_hangar_view", "BattleRoyaleHangarView"),
        ("comp7.gui.impl.lobby.hangar.comp7_hangar", "Comp7Hangar"),
        ("comp7_light.gui.impl.lobby.hangar.comp7_light_hangar", "Comp7LightHangar"),
        ("frontline.gui.impl.lobby.hangar_view", "FrontlineHangar"),
        ("fun_random.gui.impl.lobby.hangar.fun_random_hangar", "FunRandomHangar"),
        ("gui.impl.lobby.hangar.random.random_hangar", "RandomHangar"),
        ("last_stand.gui.impl.lobby.hangar_view", "HangarView"),
    ))

    hide = safe_import((
        ("gui.impl.lobby.crew.container_vews.personal_file.personal_file_view", "PersonalFileView"),
        ("gui.impl.lobby.crew.container_vews.quick_training.quick_training_view", "QuickTrainingView"),
        ("gui.impl.lobby.crew.container_vews.service_record.service_record_view", "ServiceRecordView"),
        ("gui.impl.lobby.crew.container_vews.skills_training.skills_training_view", "SkillsTrainingView"),
        ("gui.impl.lobby.crew.tankman_container_view", "TankmanContainerView"),
    ))

    return content, hide, content + hide


CONTENT_VIEWS, NOT_SHOW, ALL_VIEWS = import_views()


class DateTimes(DateTimesMeta):

    def __init__(self):
        super(DateTimes, self).__init__()
        self.enabled = False
        self.visible = False
        self.is_hangar = False
        self._timeInterval = TimeInterval(1.0, self, 'updateTime')

    def _populate(self):
        super(DateTimes, self)._populate()
        if CONTENT_VIEWS and NOT_SHOW:
            g_events.onModSettingsChanged += self.onModSettingsChanged
            self.gui.windowsManager.onWindowShowingStatusChanged += self.onWindowShowingStatusChanged
            self.onModSettingsChanged(CLOCK.NAME, self.settings)

    def _dispose(self):
        if CONTENT_VIEWS and NOT_SHOW:
            self.gui.windowsManager.onWindowShowingStatusChanged -= self.onWindowShowingStatusChanged
            g_events.onModSettingsChanged -= self.onModSettingsChanged
            self.toggleInterval(False)
        super(DateTimes, self)._dispose()

    def updateTime(self):
        self.as_updateTimeS(unicode(strftime(self.settings[CLOCK.IN_LOBBY][CLOCK.FORMAT]), ENCODING_LOCALE, ENCODING_ERRORS))

    def toggleInterval(self, enabled):
        self.setVisible(enabled)
        if enabled:
            self.updateTime()
            if not self._timeInterval.isStarted():
                self._timeInterval.start()
        else:
            self._timeInterval.stop()

    def onModSettingsChanged(self, name, data):
        if name == CLOCK.NAME and self.enabled != data[CLOCK.IN_LOBBY][GLOBAL.ENABLED]:
            self.enabled = data[CLOCK.IN_LOBBY][GLOBAL.ENABLED]
            if self.enabled:
                self.as_addToStageS()
            else:
                self.as_clearSceneS()
            self.toggleInterval(self.visible and self.enabled)

    def onWindowShowingStatusChanged(self, uniqueID, newStatus):
        if newStatus not in self.SHOWING_STATUS_TO_VALUE:
            return
        window = self.gui.windowsManager.getWindow(uniqueID).content
        logDebug("Window {} changed to {}", window, newStatus)
        if not isinstance(window, ALL_VIEWS):
            return
        visible = self.visible
        if isinstance(window, CONTENT_VIEWS):
            self.is_hangar = visible = self.SHOWING_STATUS_TO_VALUE[newStatus]
        elif isinstance(window, NOT_SHOW):
            visible = self.is_hangar and not self.SHOWING_STATUS_TO_VALUE[newStatus]
        if self.visible != visible:
            self.visible = visible
            if self.enabled:
                self.toggleInterval(self.visible)
