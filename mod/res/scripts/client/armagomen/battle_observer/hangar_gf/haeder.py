from armagomen._constants import GLOBAL, HANGAR_HEADER, LOBBY_ALIASES
from armagomen.battle_observer.settings import user_settings
from armagomen.utils.common import TimeInterval
from armagomen.utils.events import g_events
from armagomen.utils.logging import logDebug
from frameworks.wulf import ViewModel
from gui.impl import backport
from gui.impl.gen import R
from gui.impl.pub.view_component import ViewComponent
from helpers import dependency
from helpers.time_utils import getTimeDeltaFromNow, makeLocalServerTime, ONE_DAY, ONE_HOUR, ONE_MINUTE, ONE_SECOND
from openwg_gameface import gf_mod_inject, ModDynAccessor
from skeletons.gui.game_control import IGameSessionController


class HeaderModel(ViewModel):

    def __init__(self, properties=3, commands=0):
        super(HeaderModel, self).__init__(properties=properties, commands=commands)

    def _initialize(self):
        super(HeaderModel, self)._initialize()

        self._addStringProperty(HANGAR_HEADER.PREMIUM_TIMER, '')
        self._addBoolProperty(HANGAR_HEADER.SHOP, False)
        self._addBoolProperty(HANGAR_HEADER.WOT_PLUS, False)

        gf_mod_inject(self, LOBBY_ALIASES.HEADER,
                      styles=['coui://gui/gameface/mods/armagomen/battle_observer/hangar/header/header.css'],
                      modules=['coui://gui/gameface/mods/armagomen/battle_observer/hangar/header/header.js']
                      )

    def setTimerValue(self, value):
        # type: (str) -> None
        self._setString(0, value)

    def getTimerValue(self):
        # type: () -> str
        return self._getString(0)

    def setShopDisable(self, value):
        # type: (bool) -> None
        self._setBool(1, value)

    def getShopDisable(self):
        # type: () -> bool
        return self._getBool(1)

    def setPlusDisable(self, value):
        # type: (bool) -> None
        self._setBool(2, value)

    def getPlusDisable(self):
        # type: () -> bool
        return self._getBool(2)


class HeaderView(ViewComponent[HeaderModel]):
    viewLayoutID = ModDynAccessor(LOBBY_ALIASES.HEADER)
    gameSession = dependency.descriptor(IGameSessionController)

    def __init__(self):
        logDebug("hangar module: {} viewLayoutID: {}", LOBBY_ALIASES.HEADER, self.viewLayoutID())
        super(HeaderView, self).__init__(
            layoutID=self.viewLayoutID(),
            model=HeaderModel
        )

        day = backport.text(R.strings.menu.header.account.premium.days()).replace(".", "")
        hour = backport.text(R.strings.menu.header.account.premium.hours()).replace(".", "")
        self.days = "{0:d} %s. {1:02d}:{2:02d}" % day
        self.hours = "{1:d} %s. {2:02d}:{3:02d}" % hour
        self.__isPremium = False
        self.__activeTime = 0
        self._timeInterval = TimeInterval(ONE_MINUTE, self, 'updateTime')

    @property
    def viewModel(self):
        return super(HeaderView, self).getViewModel()

    @staticmethod
    def _getPremiumLabelText(template, delta):
        days, delta = divmod(delta, ONE_DAY)
        hours, delta = divmod(delta, ONE_HOUR)
        mins, secs = divmod(delta, ONE_MINUTE)
        return template.format(days, hours, mins, secs)

    def _onLoading(self):
        super(HeaderView, self)._onLoading()
        self.__isPremium = self.gameSession._stats.isPremium
        self.__activeTime = self.gameSession._stats.activePremiumExpiryTime
        g_events.onModSettingsChanged += self.onModSettingsChanged
        self.gameSession.onPremiumNotify += self.__onPremiumNotify
        self.onModSettingsChanged(HANGAR_HEADER.NAME, user_settings.hangar_header)

    def _finalize(self):
        self.gameSession.onPremiumNotify -= self.__onPremiumNotify
        g_events.onModSettingsChanged -= self.onModSettingsChanged
        self.toggleInterval(False)
        super(HeaderView, self)._finalize()

    def updateTime(self):
        delta = int(getTimeDeltaFromNow(makeLocalServerTime(self.__activeTime)))
        content, interval = (self.days, ONE_MINUTE) if delta > ONE_DAY else (self.hours, ONE_SECOND)
        self.viewModel.setTimerValue(self._getPremiumLabelText(content, delta))
        if self._timeInterval.interval != interval:
            self._timeInterval.interval = interval

    def toggleInterval(self, enabled):
        if self._timeInterval.isStarted() and enabled:
            return
        self._timeInterval.stop()
        self.viewModel.setTimerValue(GLOBAL.EMPTY_LINE)
        if enabled:
            self._timeInterval.start()
            self.updateTime()

    def onModSettingsChanged(self, name, data):
        if name == HANGAR_HEADER.NAME:
            if HANGAR_HEADER.PREMIUM_TIMER in data:
                self.toggleInterval(data[HANGAR_HEADER.PREMIUM_TIMER] and self.__isPremium)
            if HANGAR_HEADER.SHOP in data:
                self.viewModel.setShopDisable(data[HANGAR_HEADER.SHOP])
            if HANGAR_HEADER.WOT_PLUS in data:
                self.viewModel.setPlusDisable(data[HANGAR_HEADER.WOT_PLUS])

    def __onPremiumNotify(self, isPremium, _, activePremiumExpiryTime):
        if isPremium and self.__activeTime != activePremiumExpiryTime:
            self.__activeTime = activePremiumExpiryTime
            self.updateTime()
        if isPremium != self.__isPremium:
            self.__isPremium = isPremium
            self.toggleInterval(user_settings.hangar_header[HANGAR_HEADER.PREMIUM_TIMER] and isPremium)
