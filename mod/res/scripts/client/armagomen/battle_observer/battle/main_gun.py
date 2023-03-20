from math import ceil

from armagomen.battle_observer.components.controllers.players_damage_controller import damage_controller
from armagomen.battle_observer.meta.battle.main_gun_meta import MainGunMeta
from armagomen.constants import MAIN_GUN, GLOBAL
from gui.battle_control.battle_constants import FEEDBACK_EVENT_ID
from gui.battle_control.controllers.battle_field_ctrl import IBattleFieldListener


class MainGun(MainGunMeta, IBattleFieldListener):

    def __init__(self):
        super(MainGun, self).__init__()
        self.gunScore = GLOBAL.ZERO
        self.gunLeft = GLOBAL.ZERO
        self._warning = False
        self.totalEnemiesHP = GLOBAL.ZERO
        self.playerDamage = GLOBAL.ZERO

    def _populate(self):
        super(MainGun, self)._populate()
        damage_controller.onPlayerDamaged += self.onPlayerDamaged
        feedback = self.sessionProvider.shared.feedback
        if feedback is not None:
            feedback.onPlayerFeedbackReceived += self.onPlayerFeedbackReceived
        arena = self._arenaVisitor.getArenaSubscription()
        if arena is not None:
            arena.onVehicleKilled += self.onVehicleKilled

    def _dispose(self):
        damage_controller.onPlayerDamaged -= self.onPlayerDamaged
        feedback = self.sessionProvider.shared.feedback
        if feedback is not None:
            feedback.onPlayerFeedbackReceived -= self.onPlayerFeedbackReceived
        arena = self._arenaVisitor.getArenaSubscription()
        if arena is not None:
            arena.onVehicleKilled -= self.onVehicleKilled
        super(MainGun, self)._dispose()

    def onVehicleKilled(self, targetID, *args, **kwargs):
        if self.playerVehicleID == targetID:
            self._warning = True
            self.updateMainGun()

    def updateTeamHealth(self, alliesHP, enemiesHP, totalAlliesHP, totalEnemiesHP):
        if enemiesHP < self.gunLeft and not self._warning:
            self._warning = True
            self.updateMainGun()
        if self.totalEnemiesHP != totalEnemiesHP:
            self.totalEnemiesHP = totalEnemiesHP
            self.gunScore = max(MAIN_GUN.MIN_GUN_DAMAGE, int(ceil(totalEnemiesHP * MAIN_GUN.DAMAGE_RATE)))
            self.updateMainGun()

    def updateMainGun(self):
        self.gunLeft = self.gunScore - self.playerDamage
        self.as_gunDataS(self.gunLeft, self.gunScore, self._warning)

    def onPlayerDamaged(self, attackerID, damage):
        if damage > self.gunScore and self._arenaDP.isAlly(attackerID) and attackerID != self.playerVehicleID:
            self.gunScore = damage
            self.updateMainGun()

    def onPlayerFeedbackReceived(self, events):
        if self.isPostmortemSwitchedToAnotherVehicle():
            return
        for event in events:
            if event.getType() == FEEDBACK_EVENT_ID.PLAYER_DAMAGED_HP_ENEMY:
                self.playerDamage += event.getExtra().getDamage()
                self.updateMainGun()
