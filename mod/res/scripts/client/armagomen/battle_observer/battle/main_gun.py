import math

from armagomen._constants import MAIN_GUN
from armagomen.battle_observer.components.controllers import damage_controller
from armagomen.battle_observer.meta.battle.main_gun_meta import MainGunMeta
from gui.battle_control.battle_constants import FEEDBACK_EVENT_ID
from gui.battle_control.controllers.battle_field_ctrl import IBattleFieldListener


class MainGun(MainGunMeta, IBattleFieldListener):

    def __init__(self):
        super(MainGun, self).__init__()
        self._warning = False
        self.gunScore = 0
        self.playerDamage = 0
        self.totalEnemiesHP = 0

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
        if self.totalEnemiesHP != totalEnemiesHP:
            self.totalEnemiesHP = totalEnemiesHP
            self.gunScore = max(MAIN_GUN.MIN_GUN_DAMAGE, int(math.ceil(totalEnemiesHP * MAIN_GUN.DAMAGE_RATE)))
            self.updateMainGun()
        elif not self._warning and enemiesHP < self.gunScore - self.playerDamage:
            self._warning = True
            self.updateMainGun()

    def updateMainGun(self):
        self.as_gunDataS(self.playerDamage, self.gunScore, self._warning)

    def onPlayerDamaged(self, attackerID, damage):
        if damage > self.gunScore and attackerID != self.playerVehicleID:
            self.gunScore = damage
            self.updateMainGun()

    def onPlayerFeedbackReceived(self, events):
        if self.isPlayerVehicle:
            for event in events:
                if event.getType() == FEEDBACK_EVENT_ID.PLAYER_DAMAGED_HP_ENEMY:
                    self.playerDamage += event.getExtra().getDamage()
                    self.updateMainGun()
