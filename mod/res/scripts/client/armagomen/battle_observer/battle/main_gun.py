# coding=utf-8
from collections import defaultdict, namedtuple
from math import ceil

from armagomen.battle_observer.meta.battle.main_gun_meta import MainGunMeta
from armagomen.constants import MAIN_GUN, GLOBAL
from armagomen.utils.common import logDebug
from gui.battle_control.controllers.battle_field_ctrl import IBattleFieldListener
from helpers import getClientLanguage

CRITERIA = namedtuple("CRITERIA", ("PLAYER_DAMAGE", "LOW_HEALTH", "TOTAL_HEALTH", "DEALT_MORE"))(0, 1, 2, 3)

DEBUG_STRING = "MainGun: playerDamage={}, maxDamage={}, dealtMoreDamage={}, self.gunLeft={}, criteria={}"
ln = getClientLanguage().lower()

if ln == 'uk':
    I18N_CRITERIA = {CRITERIA.LOW_HEALTH: "Замало здоров'я у ворога",
                     CRITERIA.DEALT_MORE: "Інший гравець перевищує пошкодження"}
elif ln in ('ru', 'be'):
    I18N_CRITERIA = {CRITERIA.LOW_HEALTH: "Низкое здоровье врага",
                     CRITERIA.DEALT_MORE: "Больше урона у другого игрока"}
else:
    I18N_CRITERIA = {CRITERIA.LOW_HEALTH: "Low enemy health",
                     CRITERIA.DEALT_MORE: "More damage from another player"}


class MainGun(MainGunMeta, IBattleFieldListener):

    def __init__(self):
        super(MainGun, self).__init__()
        self.macros = defaultdict(lambda: GLOBAL.CONFIG_ERROR)
        self.gunScore = GLOBAL.ZERO
        self.gunLeft = GLOBAL.ZERO
        self.isLowHealth = False
        self.totalEnemiesHP = GLOBAL.ZERO
        self.playersDamage = defaultdict(int)

    def onEnterBattlePage(self):
        super(MainGun, self).onEnterBattlePage()
        arena = self._arenaVisitor.getArenaSubscription()
        if arena is not None:
            arena.onVehicleHealthChanged += self.onPlayersDamaged

    def onExitBattlePage(self):
        arena = self._arenaVisitor.getArenaSubscription()
        if arena is not None:
            arena.onVehicleHealthChanged -= self.onPlayersDamaged
        super(MainGun, self).onExitBattlePage()

    def _populate(self):
        super(MainGun, self)._populate()
        self.macros.update(mainGunIcon=self.settings[MAIN_GUN.GUN_ICON],
                           mainGunColor=self.colors[MAIN_GUN.NAME][MAIN_GUN.COLOR],
                           mainGunDoneIcon=GLOBAL.EMPTY_LINE, mainGunFailureIcon=GLOBAL.EMPTY_LINE)

    def updateTeamHealth(self, alliesHP, enemiesHP, totalAlliesHP, totalEnemiesHP):
        if enemiesHP < self.gunLeft and not self.isLowHealth:
            self.isLowHealth = True
            self.updateMainGun(criteria=CRITERIA.LOW_HEALTH)
        if self.totalEnemiesHP != totalEnemiesHP:
            self.totalEnemiesHP = totalEnemiesHP
            self.gunScore = max(MAIN_GUN.MIN_GUN_DAMAGE, int(ceil(totalEnemiesHP * MAIN_GUN.DAMAGE_RATE)))
            self.updateMainGun(criteria=CRITERIA.TOTAL_HEALTH)

    def checkDamage(self):
        playerDamage = self.playersDamage[self._player.playerVehicleID]
        maxDamage = max(self.playersDamage.itervalues())
        dealtMoreDamage = maxDamage > playerDamage > self.gunScore
        return dealtMoreDamage, maxDamage, playerDamage

    def updateMainGun(self, criteria=GLOBAL.EMPTY_LINE):
        dealtMoreDamage, maxDamage, playerDamage = self.checkDamage()
        if not self.isLowHealth:
            self.gunLeft = (maxDamage if dealtMoreDamage else self.gunScore) - playerDamage
            if dealtMoreDamage:
                criteria = CRITERIA.DEALT_MORE
        self.updateMacrosDict(dealtMoreDamage, criteria)
        logDebug(DEBUG_STRING, playerDamage, maxDamage, dealtMoreDamage, self.gunLeft, criteria)
        self.as_mainGunTextS(self.settings[MAIN_GUN.TEMPLATE] % self.macros)

    def updateMacrosDict(self, dealtMoreDamage, criteria):
        achieved = self.gunLeft <= GLOBAL.ZERO
        self.macros[MAIN_GUN.INFO] = GLOBAL.EMPTY_LINE if achieved or self.isLowHealth else self.gunLeft
        self.macros[MAIN_GUN.DONE_ICON] = self.settings[MAIN_GUN.DONE_ICON] if achieved else GLOBAL.EMPTY_LINE
        if not achieved and (self.isLowHealth or dealtMoreDamage):
            self.macros[MAIN_GUN.FAILURE_ICON] = self.settings[MAIN_GUN.FAILURE_ICON] + I18N_CRITERIA[criteria]
        else:
            self.macros[MAIN_GUN.FAILURE_ICON] = GLOBAL.EMPTY_LINE

    def onPlayersDamaged(self, targetID, attackerID, damage):
        if self._arenaDP.isAlly(attackerID):
            self.playersDamage[attackerID] += damage
            if attackerID == self._player.playerVehicleID:
                self.updateMainGun(criteria=CRITERIA.PLAYER_DAMAGE)
