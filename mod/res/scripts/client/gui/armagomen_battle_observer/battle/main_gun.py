from collections import defaultdict
from math import ceil

from gui.battle_control.battle_constants import FEEDBACK_EVENT_ID
from ..core.battle_cache import cache, g_health
from ..core.bo_constants import MAIN_GUN, GLOBAL
from ..core.config import cfg
from ..core.events import g_events
from ..meta.battle.main_gun_meta import MainGunMeta

config = cfg.main_gun


class MainGun(MainGunMeta):

    def __init__(self):
        super(MainGun, self).__init__()
        self.macros = defaultdict(GLOBAL.CONFIG_ERROR)
        self._damage = GLOBAL.ZERO
        self._gunScore = GLOBAL.ZERO
        self.enabled = False
        self.gunLeft = 0
        self.maxDamage = 0
        self.gunIcons = {
            True: [config[MAIN_GUN.DONE_ICON], config[MAIN_GUN.FAILURE_ICON]],
            False: [GLOBAL.EMPTY_LINE, GLOBAL.EMPTY_LINE]
        }
        self.healthFailed = False
        self.damageFailed = False
        self.playerDead = False

    def onEnterBattlePage(self):
        super(MainGun, self).onEnterBattlePage()
        self.enabled = self.mainGunSettingsUpdate()
        if config[MAIN_GUN.DYNAMIC] and self.enabled:
            feedback = self.sessionProvider.shared.feedback
            if feedback:
                feedback.onPlayerFeedbackReceived += self.__onPlayerFeedbackReceived
            g_events.onPlayerVehicleDeath += self.onPlayerVehicleDeath
            g_events.onMainGunHealthChanged += self.onMainGunHealthChanged
            self.updateMainGun()
        elif not config[MAIN_GUN.DYNAMIC] and self.enabled:
            self.macros.update(mainGun=self._gunScore)
            self.as_mainGunTextS(config[MAIN_GUN.TEMPLATE] % self.macros)

    def onExitBattlePage(self):
        if config[MAIN_GUN.DYNAMIC] and self.enabled:
            feedback = self.sessionProvider.shared.feedback
            if feedback:
                feedback.onPlayerFeedbackReceived -= self.__onPlayerFeedbackReceived
            g_events.onMainGunHealthChanged -= self.onMainGunHealthChanged
            g_events.onPlayerVehicleDeath -= self.onPlayerVehicleDeath
        self.macros.clear()
        self._damage = GLOBAL.ZERO
        self.enabled = False
        super(MainGun, self).onExitBattlePage()

    def _populate(self):
        super(MainGun, self)._populate()
        self.as_startUpdateS(config[GLOBAL.SETTINGS])

    def onMainGunHealthChanged(self, attackerID, team):
        if not self.playerDead:
            attackerDamage = cache.playersDamage[attackerID]
            if attackerDamage > self.maxDamage > self._gunScore:
                self.maxDamage = attackerDamage
            if team == cache.enemyTeam:
                self.healthFailed = g_health.getTeamCurrent(team) < self.gunLeft
                self.updateMainGun()

    def mainGunSettingsUpdate(self):
        isRandomBattle = self.sessionProvider.arenaVisitor.gui.isRandomBattle()
        if isRandomBattle:
            maxHealth = g_health.getTeamMaximum(cache.enemyTeam)
            self._gunScore = max(MAIN_GUN.MIN_GUN_DAMAGE, int(ceil(maxHealth * MAIN_GUN.DAMAGE_RATE)))
            self.macros.update(mainGunIcon=config[MAIN_GUN.GUN_ICON],
                               mainGunColor=cfg.colors[MAIN_GUN.NAME][MAIN_GUN.COLOR],
                               mainGunDoneIcon=GLOBAL.EMPTY_LINE, mainGunFailureIcon=GLOBAL.EMPTY_LINE)
        return isRandomBattle

    def __onPlayerFeedbackReceived(self, events, *a, **kw):
        for event in events:
            if event.getType() == FEEDBACK_EVENT_ID.PLAYER_DAMAGED_HP_ENEMY:
                self._damage += int(event.getExtra().getDamage())
                self.damageFailed = self._damage < self.maxDamage
                if not self.damageFailed:
                    self.maxDamage = self._damage
                self.updateMainGun()

    def updateMainGun(self):
        self.gunLeft = max(self._gunScore, self.maxDamage) - self._damage
        gunFailed = self.healthFailed or self.damageFailed or self.playerDead
        mainGunAchieved = self.gunLeft <= GLOBAL.ZERO and not gunFailed
        self.macros.update(mainGun=GLOBAL.EMPTY_LINE if mainGunAchieved else self.gunLeft,
                           mainGunDoneIcon=self.gunIcons[mainGunAchieved][GLOBAL.FIRST],
                           mainGunFailureIcon=self.gunIcons[gunFailed][GLOBAL.LAST])
        self.as_mainGunTextS(config[MAIN_GUN.TEMPLATE] % self.macros)

    def onPlayerVehicleDeath(self, killerID):
        if self.gunLeft > GLOBAL.ZERO:
            self.playerDead = True
            self.updateMainGun()
