# coding=utf-8
from collections import defaultdict
from math import ceil

from armagomen.battle_observer.meta.battle.main_gun_meta import MainGunMeta
from armagomen.constants import MAIN_GUN, GLOBAL
from gui.battle_control.controllers.battle_field_ctrl import IBattleFieldListener
from helpers import getClientLanguage

language = getClientLanguage()
if language == 'uk':
    I18N_LOW_HEALTH = "Низьке здоров'я ворога"
elif language in ('ru', 'be'):
    I18N_LOW_HEALTH = "Низкое здоровье врага"
else:
    I18N_LOW_HEALTH = "Low enemy health"


class MainGun(MainGunMeta, IBattleFieldListener):

    def __init__(self):
        super(MainGun, self).__init__()
        self.macros = defaultdict(lambda: GLOBAL.CONFIG_ERROR)
        self.gunScore = GLOBAL.ZERO
        self.gunLeft = GLOBAL.ZERO
        self.isLowHealth = False
        self.totalEnemiesHP = GLOBAL.ZERO
        self.playersDamage = defaultdict(int)
        self.playerDamage = GLOBAL.ZERO
        self.maxDamage = GLOBAL.ZERO
        self.dealtMoreDamage = False

    def _populate(self):
        super(MainGun, self)._populate()
        self.macros.update(mainGunIcon=self.settings[MAIN_GUN.GUN_ICON],
                           mainGunDoneIcon=GLOBAL.EMPTY_LINE, mainGunFailureIcon=GLOBAL.EMPTY_LINE)
        arena = self._arenaVisitor.getArenaSubscription()
        if arena is not None:
            arena.onVehicleHealthChanged += self.onPlayersDamaged

    def _dispose(self):
        arena = self._arenaVisitor.getArenaSubscription()
        if arena is not None:
            arena.onVehicleHealthChanged -= self.onPlayersDamaged
        super(MainGun, self)._dispose()

    def updateTeamHealth(self, alliesHP, enemiesHP, totalAlliesHP, totalEnemiesHP):
        if enemiesHP < self.gunLeft and not self.isLowHealth:
            self.isLowHealth = True
            self.updateMainGun()
        if self.totalEnemiesHP != totalEnemiesHP:
            self.totalEnemiesHP = totalEnemiesHP
            self.gunScore = max(MAIN_GUN.MIN_GUN_DAMAGE, int(ceil(totalEnemiesHP * MAIN_GUN.DAMAGE_RATE)))
            self.updateMainGun()

    def updateMainGun(self):
        if not self.isLowHealth:
            self.gunLeft = (self.maxDamage if self.dealtMoreDamage else self.gunScore) - self.playerDamage
        self.updateMacrosDict()
        self.as_mainGunTextS(self.settings[MAIN_GUN.TEMPLATE] % self.macros)

    def updateMacrosDict(self):
        achieved = self.gunLeft <= GLOBAL.ZERO
        self.macros[MAIN_GUN.INFO] = GLOBAL.EMPTY_LINE if achieved or self.isLowHealth else self.gunLeft
        self.macros[MAIN_GUN.DONE_ICON] = self.settings[MAIN_GUN.DONE_ICON] if achieved else GLOBAL.EMPTY_LINE
        if not achieved and self.isLowHealth:
            self.macros[MAIN_GUN.FAILURE_ICON] = self.settings[MAIN_GUN.FAILURE_ICON] + I18N_LOW_HEALTH
        else:
            self.macros[MAIN_GUN.FAILURE_ICON] = GLOBAL.EMPTY_LINE

    def onPlayersDamaged(self, targetID, attackerID, damage):
        if self._arenaDP.isAlly(attackerID) and not self.isLowHealth:
            self.playersDamage[attackerID] += damage
            if self.playersDamage[attackerID] > self.maxDamage:
                self.maxDamage = self.playersDamage[attackerID]
            self.playerDamage = self.playersDamage[self.playerVehicleID]
            self.dealtMoreDamage = self.maxDamage > self.playerDamage > self.gunScore
            if attackerID == self.playerVehicleID or self.dealtMoreDamage:
                self.updateMainGun()
