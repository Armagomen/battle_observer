from armagomen._constants import AVG_EFFICIENCY_HANGAR, EFFICIENCY_ICONS_SIZE, GLOBAL, IMAGE_DIR
from armagomen.battle_observer.components.controllers import cachedVehicleData
from armagomen.battle_observer.meta.lobby.hangar_efficiency_meta import HangarEfficiencyMeta
from armagomen.utils.common import safe_import
from armagomen.utils.events import g_events
from armagomen.utils.logging import logDebug


def import_views():
    content = safe_import("gui.impl.lobby.hangar.random.random_hangar", "RandomHangar")

    hide = (
            safe_import("gui.impl.lobby.crew.container_vews.quick_training.quick_training_view", "QuickTrainingView") +
            safe_import("gui.impl.lobby.crew.container_vews.skills_training.skills_training_view", "SkillsTrainingView") +
            safe_import("gui.impl.lobby.crew.container_vews.service_record.service_record_view", "ServiceRecordView") +
            safe_import("gui.impl.lobby.crew.container_vews.personal_file.personal_file_view", "PersonalFileView") +
            safe_import("gui.impl.lobby.mode_selector.mode_selector_view", "ModeSelectorView") +
            safe_import("gui.impl.lobby.battle_results.random_battle_results_view", "RandomBattleResultsView") +
            safe_import("gui.impl.lobby.crew.tankman_container_view", "TankmanContainerView")
    )

    return content, hide, content + hide


CONTENT_VIEWS, NOT_SHOW, ALL_VIEWS = import_views()


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
        self.visible = False
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
        logDebug("Hangar Efficiency enabled: {}, Data: {}", self.enabled, data)
        if not self.enabled:
            return
        value = GLOBAL.EMPTY_LINE
        if data is None:
            self.as_updateValueS(value)
            return
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
                    self.setVisible(self.visible)
                else:
                    self.as_clearSceneS()
            if self.enabled:
                cachedVehicleData.onVehicleChanged()

    def onWindowShowingStatusChanged(self, uniqueID, newStatus):
        if newStatus not in self.SHOWING_STATUS_TO_VALUE:
            return
        window = self.gui.windowsManager.getWindow(uniqueID).content
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
                self.setVisible(self.visible)
