from armagomen._constants import AVG_EFFICIENCY_HANGAR, EFFICIENCY_ICONS_SIZE, GLOBAL, IMAGE_DIR
from armagomen.battle_observer.components.controllers import cachedVehicleData
from armagomen.battle_observer.meta.lobby.hangar_efficiency_meta import HangarEfficiencyMeta
from armagomen.utils.events import g_events
from armagomen.utils.logging import logDebug
from gui.impl.lobby.battle_results.random_battle_results_view import RandomBattleResultsView
from gui.impl.lobby.crew.container_vews.personal_file.personal_file_view import PersonalFileView
from gui.impl.lobby.crew.container_vews.quick_training.quick_training_view import QuickTrainingView
from gui.impl.lobby.crew.container_vews.service_record.service_record_view import ServiceRecordView
from gui.impl.lobby.crew.container_vews.skills_training.skills_training_view import SkillsTrainingView
from gui.impl.lobby.crew.tankman_container_view import TankmanContainerView
from gui.impl.lobby.hangar.random.random_hangar import RandomHangar
from gui.impl.lobby.mode_selector.mode_selector_view import ModeSelectorView

NOT_SHOW = (QuickTrainingView, SkillsTrainingView, ServiceRecordView, PersonalFileView, ModeSelectorView, RandomBattleResultsView,
            TankmanContainerView)
ALL_VIEWS = (RandomHangar,) + NOT_SHOW


class HangarEfficiency(HangarEfficiencyMeta):
    EFFICIENCY_ICONS = {
        "assistIcon": "<img src='{}/efficiency/help.png' {}>".format(IMAGE_DIR, EFFICIENCY_ICONS_SIZE),
        "blockedIcon": "<img src='{}/efficiency/armor.png' {}>".format(IMAGE_DIR, EFFICIENCY_ICONS_SIZE),
        "damageIcon": "<img src='{}/efficiency/damage.png' {}>".format(IMAGE_DIR, EFFICIENCY_ICONS_SIZE),
        "winRateIcon": "<img src='{}/efficiency/wins.png' {}>".format(IMAGE_DIR, EFFICIENCY_ICONS_SIZE),
        "stunIcon": "<img src='{}/efficiency/stun.png' {}>".format(IMAGE_DIR, EFFICIENCY_ICONS_SIZE),
        "spottedIcon": "<img src='{}/efficiency/detection.png' {}>".format(IMAGE_DIR, EFFICIENCY_ICONS_SIZE),
        "battlesIcon": "<img src='{}/efficiency/battles.png' {}>".format(IMAGE_DIR, EFFICIENCY_ICONS_SIZE),
    }

    def __init__(self):
        super(HangarEfficiency, self).__init__()
        self.enabled = False
        self.is_hangar = False

    def _populate(self):
        super(HangarEfficiency, self)._populate()
        g_events.onModSettingsChanged += self.onModSettingsChanged
        self.gui.windowsManager.onWindowShowingStatusChanged += self.onWindowShowingStatusChanged
        cachedVehicleData.onChanged += self.update
        self.onModSettingsChanged(AVG_EFFICIENCY_HANGAR.NAME, self.settings)

    def _dispose(self):
        cachedVehicleData.onChanged -= self.update
        self.gui.windowsManager.onWindowShowingStatusChanged -= self.onWindowShowingStatusChanged
        g_events.onModSettingsChanged -= self.onModSettingsChanged
        super(HangarEfficiency, self)._dispose()

    def update(self, data):
        logDebug("Hangar Efficiency enabled: {} Data: {}", self.enabled, data)
        if not self.enabled or data is None:
            return
        value = GLOBAL.EMPTY_LINE
        settings_map = [
            (AVG_EFFICIENCY_HANGAR.DAMAGE, "{damageIcon}{tankAvgDamage}"),
            (AVG_EFFICIENCY_HANGAR.ASSIST, "{assistIcon}{tankAvgAssist}"),
            (AVG_EFFICIENCY_HANGAR.BLOCKED, "{blockedIcon}{tankAvgBlocked}"),
            (AVG_EFFICIENCY_HANGAR.STUN, "{stunIcon}{tankAvgStun}", data.tankAvgStun),
            (AVG_EFFICIENCY_HANGAR.BATTLES, "{battlesIcon}{battles}"),
            (AVG_EFFICIENCY_HANGAR.WIN_RATE, "{winRateIcon}{winRate:.2f}%"),
            (AVG_EFFICIENCY_HANGAR.MARKS_ON_GUN, "{marksOnGunIcon}{marksOnGunValue:.2f}%", data.marksAvailable)
        ]
        text = [tpl[1] for tpl in settings_map if self.getSettings().get(tpl[0]) and tpl[-1]]
        if text:
            params = data._asdict()
            params.update(self.EFFICIENCY_ICONS)
            value = "  ".join(text).format(**params)
        self.as_updateValueS(value)

    def onModSettingsChanged(self, name, data):
        if name == AVG_EFFICIENCY_HANGAR.NAME:
            if self.enabled != data[GLOBAL.ENABLED]:
                self.enabled = data[GLOBAL.ENABLED]
                if self.enabled:
                    self.as_addToStageS()
                else:
                    self.as_clearSceneS()
            if self.enabled:
                cachedVehicleData.onVehicleChanged()

    def onWindowShowingStatusChanged(self, uniqueID, newStatus):
        if not self.enabled or newStatus not in self.SHOWING_STATUS_TO_VALUE:
            return

        window = self.gui.windowsManager.getWindow(uniqueID).content
        # logDebug("Hangar Efficiency Window: {}", repr(window))
        if not isinstance(window, ALL_VIEWS):
            return

        status_value = self.SHOWING_STATUS_TO_VALUE[newStatus]

        if isinstance(window, RandomHangar):
            self.is_hangar = status_value
            self.setVisible(self.is_hangar)
        elif isinstance(window, NOT_SHOW):
            self.setVisible(self.is_hangar and not status_value)
