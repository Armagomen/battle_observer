from armagomen._constants import CLOCK, GLOBAL, LOBBY_ALIASES
from armagomen.battle_observer.settings import IBOSettingsLoader
from armagomen.utils.common import ENCODING_ERRORS, ENCODING_LOCALE
from armagomen.utils.events import g_events
from armagomen.utils.logging import logDebug
from frameworks.wulf import ViewModel
from gui.impl.pub.view_component import ViewComponent
from gui.shared.utils.TimeInterval import TimeInterval
from helpers import dependency
from openwg_gameface import gf_mod_inject, ModDynAccessor
from time import strftime


class ClockModel(ViewModel):

    def __init__(self, properties=1, commands=0):
        super(ClockModel, self).__init__(properties=properties, commands=commands)

    def _initialize(self):
        super(ClockModel, self)._initialize()

        self._addStringProperty('clock', '')

        gf_mod_inject(self, LOBBY_ALIASES.DATE_TIME,
                      styles=['coui://gui/gameface/mods/armagomen/battle_observer/hangar/clock/clock.css'],
                      modules=['coui://gui/gameface/mods/armagomen/battle_observer/hangar/clock/clock.js']
                      )

    def setContent(self, value):
        # type: (str) -> None
        self._setString(0, value)

    def getContent(self):
        # type: () -> str
        return self._getString(0)


class DateTimesView(ViewComponent[ClockModel]):
    viewLayoutID = ModDynAccessor(LOBBY_ALIASES.DATE_TIME)
    settingsLoader = dependency.descriptor(IBOSettingsLoader)

    def __init__(self):

        logDebug("hangar module: {} viewLayoutID: {}", LOBBY_ALIASES.DATE_TIME, self.viewLayoutID())
        super(DateTimesView, self).__init__(
            layoutID=self.viewLayoutID(),
            model=ClockModel
        )
        self.__enabled = False
        self.__hangarEnabled = False
        self.__clockFormat = CLOCK.DEFAULT_FORMAT_HANGAR
        self._timeInterval = TimeInterval(1.0, self, 'updateTime')

    @property
    def viewModel(self):
        return super(DateTimesView, self).getViewModel()

    @property
    def settings(self):
        return self.settingsLoader.getSettingDictByAliasLobby(LOBBY_ALIASES.DATE_TIME)

    def _onLoading(self):
        super(DateTimesView, self)._onLoading()
        g_events.onModSettingsChanged += self.onModSettingsChanged
        self.onModSettingsChanged(CLOCK.NAME, self.settings)

    def _finalize(self):
        g_events.onModSettingsChanged -= self.onModSettingsChanged
        self.toggleInterval(False)
        super(DateTimesView, self)._finalize()

    def updateTime(self):
        time = "<span>{}</span>".format(strftime(self.__clockFormat))
        self.viewModel.setContent(unicode(time, ENCODING_LOCALE, ENCODING_ERRORS))

    def toggleInterval(self, enabled):
        if self._timeInterval.isStarted() and enabled:
            return
        self._timeInterval.stop()
        self.viewModel.setContent(GLOBAL.EMPTY_LINE)
        if enabled:
            self.updateTime()
            self._timeInterval.start()

    def onModSettingsChanged(self, name, data):
        if name == CLOCK.NAME:
            in_lobby = data.get(CLOCK.IN_LOBBY)
            if in_lobby:
                u_format = in_lobby.get(CLOCK.FORMAT, self.__clockFormat)
                if not u_format.lower().startswith("tab"):
                    self.__clockFormat = u_format
                self.__hangarEnabled = in_lobby.get(GLOBAL.ENABLED, self.__hangarEnabled)
            self.__enabled = data.get(GLOBAL.ENABLED, self.__enabled)
            self.toggleInterval(self.__enabled and self.__hangarEnabled)
