from armagomen._constants import AVG_EFFICIENCY_HANGAR, GLOBAL, IMAGE_DIR, LOBBY_ALIASES
from armagomen.battle_observer.components.controllers import cachedVehicleData
from armagomen.battle_observer.settings import user_settings
from armagomen.utils.events import g_events
from armagomen.utils.logging import logDebug
from frameworks.wulf import ViewModel
from gui.impl.pub.view_component import ViewComponent
from openwg_gameface import gf_mod_inject, ModDynAccessor


class HangarEfficiencyModel(ViewModel):

    def __init__(self, properties=1, commands=0):
        super(HangarEfficiencyModel, self).__init__(properties=properties, commands=commands)

    def _initialize(self):
        super(HangarEfficiencyModel, self)._initialize()

        self._addStringProperty('effHtmlText', '')

        gf_mod_inject(self, LOBBY_ALIASES.EFFICIENCY,
                      styles=['coui://gui/gameface/mods/armagomen/battle_observer/hangar/efficiency/efficiency.css'],
                      modules=['coui://gui/gameface/mods/armagomen/battle_observer/hangar/efficiency/efficiency.js']
                      )

    def setContent(self, value):
        # type: (str) -> None
        self._setString(0, value)

    def getContent(self):
        # type: () -> str
        return self._getString(0)


EFFICIENCY_ICONS = {
    "assistIcon": "<img class='bo_effIcon' src='{}/efficiency/help.png'>".format(IMAGE_DIR),
    "blockedIcon": "<img class='bo_effIcon' src='{}/efficiency/armor.png'>".format(IMAGE_DIR),
    "damageIcon": "<img class='bo_effIcon' src='{}/efficiency/damage.png'>".format(IMAGE_DIR),
    "winRateIcon": "<img class='bo_effIcon' src='{}/efficiency/wins.png'>".format(IMAGE_DIR),
    "stunIcon": "<img class='bo_effIcon' src='{}/efficiency/stun.png'>".format(IMAGE_DIR),
    "spottedIcon": "<img class='bo_effIcon' src='{}/efficiency/detection.png'>".format(IMAGE_DIR),
    "battlesIcon": "<img class='bo_effIcon' src='{}/efficiency/battles.png'>".format(IMAGE_DIR),
}


class HangarEfficiencyView(ViewComponent[HangarEfficiencyModel]):
    viewLayoutID = ModDynAccessor(LOBBY_ALIASES.EFFICIENCY)

    def __init__(self):
        logDebug("hangar module: {} viewLayoutID: {}", LOBBY_ALIASES.EFFICIENCY, self.viewLayoutID())
        super(HangarEfficiencyView, self).__init__(
            layoutID=self.viewLayoutID(),
            model=HangarEfficiencyModel
        )

    @property
    def viewModel(self):
        return super(HangarEfficiencyView, self).getViewModel()

    def _onLoading(self, *args, **kwargs):
        super(HangarEfficiencyView, self)._onLoading()
        self.subscribe()
        logDebug("hangar module '{}' loaded", LOBBY_ALIASES.EFFICIENCY)

    def _finalize(self):
        self.unsubscribe()
        super(HangarEfficiencyView, self)._finalize()
        logDebug("hangar module '{}' dispose", LOBBY_ALIASES.EFFICIENCY)

    @property
    def settings(self):
        return user_settings.getSettingDictByAliasLobby(LOBBY_ALIASES.EFFICIENCY)

    def subscribe(self):
        g_events.onModSettingsChanged += self.onModSettingsChanged
        cachedVehicleData.onChanged += self.update
        self.onModSettingsChanged(AVG_EFFICIENCY_HANGAR.NAME, self.settings)

    def unsubscribe(self):
        cachedVehicleData.onChanged -= self.update
        g_events.onModSettingsChanged -= self.onModSettingsChanged

    def update(self, data):
        value = GLOBAL.EMPTY_LINE
        if not self.settings["enabled"] and self.viewModel.getContent() or data is None:
            self.viewModel.setContent(value)
            return

        settings_map = [
            (AVG_EFFICIENCY_HANGAR.DAMAGE, "{damageIcon}<span>{tankAvgDamage}</span>"),
            (AVG_EFFICIENCY_HANGAR.ASSIST, "{assistIcon}<span>{tankAvgAssist}</span>"),
            (AVG_EFFICIENCY_HANGAR.BLOCKED, "{blockedIcon}<span>{tankAvgBlocked}</span>"),
            (AVG_EFFICIENCY_HANGAR.STUN, "{stunIcon}<span>{tankAvgStun}</span>", data.tankAvgStun),
            (AVG_EFFICIENCY_HANGAR.BATTLES, "{battlesIcon}<span>{battles}</span>"),
            (AVG_EFFICIENCY_HANGAR.WIN_RATE, "{winRateIcon}<span>{winRate:.2f}%</span>"),
            (AVG_EFFICIENCY_HANGAR.MARKS_ON_GUN, "{marksOnGunIcon}<span>{marksOnGunValue:.2f}%</span>", data.marksAvailable)
        ]
        text = [tpl[1] for tpl in settings_map if self.settings.get(tpl[0]) and tpl[-1]]
        if text:
            params = data._asdict()
            params.update(EFFICIENCY_ICONS)
            value = GLOBAL.EMPTY_LINE.join(text).format(**params)
        self.viewModel.setContent(value)

    def onModSettingsChanged(self, name, data):
        if name == AVG_EFFICIENCY_HANGAR.NAME:
            if data[GLOBAL.ENABLED]:
                cachedVehicleData.onVehicleChanged()
            else:
                self.viewModel.setContent(GLOBAL.EMPTY_LINE)
