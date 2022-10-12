# coding=utf-8
from collections import defaultdict, namedtuple
from math import ceil

from armagomen.battle_observer.meta.battle.main_gun_meta import MainGunMeta
from armagomen.constants import MAIN_GUN, GLOBAL
from gui.battle_control.controllers.battle_field_ctrl import IBattleFieldListener
from helpers import getClientLanguage

CRITERIA = namedtuple("CRITERIA", ("PLAYER_DAMAGE", "LOW_HEALTH", "TOTAL_HEALTH", "DEALT_MORE"))(0, 1, 2, 3)

language = getClientLanguage()
if language == 'uk':
    I18N_CRITERIA = {CRITERIA.LOW_HEALTH: "Низьке здоров'я ворога"}
elif language in ('ru', 'be'):
    I18N_CRITERIA = {CRITERIA.LOW_HEALTH: "Низкое здоровье врага"}
else:
    I18N_CRITERIA = {CRITERIA.LOW_HEALTH: "Low enemy health"}


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
                           mainGunDoneIcon=GLOBAL.EMPTY_LINE, mainGunFailureIcon=GLOBAL.EMPTY_LINE)

    def updateTeamHealth(self, alliesHP, enemiesHP, totalAlliesHP, totalEnemiesHP):
        if enemiesHP < self.gunLeft and not self.isLowHealth:
            self.isLowHealth = True
            self.updateMainGun(criteria=CRITERIA.LOW_HEALTH)
        if self.totalEnemiesHP != totalEnemiesHP:
            self.totalEnemiesHP = totalEnemiesHP
            self.gunScore = max(MAIN_GUN.MIN_GUN_DAMAGE, int(ceil(totalEnemiesHP * MAIN_GUN.DAMAGE_RATE)))
            self.updateMainGun(criteria=CRITERIA.TOTAL_HEALTH)

    def updateMainGun(self, criteria=None):
        if criteria is None:
            return
        if not self.isLowHealth:
            self.gunLeft = (self.maxDamage if self.dealtMoreDamage else self.gunScore) - self.playerDamage
        elif criteria == CRITERIA.PLAYER_DAMAGE:
            criteria = CRITERIA.LOW_HEALTH
        self.updateMacrosDict(criteria)
        self.as_mainGunTextS(self.settings[MAIN_GUN.TEMPLATE] % self.macros)

    def updateMacrosDict(self, criteria):
        achieved = self.gunLeft <= GLOBAL.ZERO
        self.macros[MAIN_GUN.INFO] = GLOBAL.EMPTY_LINE if achieved or self.isLowHealth else self.gunLeft
        self.macros[MAIN_GUN.DONE_ICON] = self.settings[MAIN_GUN.DONE_ICON] if achieved else GLOBAL.EMPTY_LINE
        if not achieved and self.isLowHealth:
            self.macros[MAIN_GUN.FAILURE_ICON] = self.settings[MAIN_GUN.FAILURE_ICON] + I18N_CRITERIA.get(criteria)
        else:
            self.macros[MAIN_GUN.FAILURE_ICON] = GLOBAL.EMPTY_LINE

    def onPlayersDamaged(self, targetID, attackerID, damage):
        if self._arenaDP.isAlly(attackerID) and not self.isLowHealth:
            self.playersDamage[attackerID] += damage
            if self.playersDamage[attackerID] > self.maxDamage:
                self.maxDamage = self.playersDamage[attackerID]
            self.playerDamage = self.playersDamage[self._player.playerVehicleID]
            self.dealtMoreDamage = self.maxDamage > self.playerDamage > self.gunScore
            if attackerID == self._player.playerVehicleID or self.dealtMoreDamage:
                self.updateMainGun(criteria=CRITERIA.PLAYER_DAMAGE if not self.dealtMoreDamage else CRITERIA.DEALT_MORE)
