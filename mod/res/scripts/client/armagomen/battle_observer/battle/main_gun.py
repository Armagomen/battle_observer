from collections import defaultdict
from math import ceil

from armagomen.constants import MAIN_GUN, GLOBAL, POSTMORTEM
from armagomen.battle_observer.meta.battle.main_gun_meta import MainGunMeta
from gui.battle_control import avatar_getter
from gui.battle_control.battle_constants import FEEDBACK_EVENT_ID
from gui.battle_control.controllers.battle_field_ctrl import IBattleFieldListener


class MainGun(MainGunMeta, IBattleFieldListener):

    def __init__(self):
        super(MainGun, self).__init__()
        self.macros = None
        self._gunScore = GLOBAL.ZERO
        self.gunLeft = GLOBAL.ZERO
        self.gunIcons = None
        self.healthFailed = False
        self.playerDead = False

    def onEnterBattlePage(self):
        super(MainGun, self).onEnterBattlePage()
        self.updateMainGun()
        feedback = self.sessionProvider.shared.feedback
        if feedback:
            feedback.onPlayerFeedbackReceived += self.__onPlayerFeedbackReceived
        handler = avatar_getter.getInputHandler()
        if handler is not None:
            handler.onCameraChanged += self.onCameraChanged

    def onExitBattlePage(self):
        feedback = self.sessionProvider.shared.feedback
        if feedback:
            feedback.onPlayerFeedbackReceived -= self.__onPlayerFeedbackReceived
        handler = avatar_getter.getInputHandler()
        if handler is not None:
            handler.onCameraChanged += self.onCameraChanged
        super(MainGun, self).onExitBattlePage()

    def _populate(self):
        super(MainGun, self)._populate()
        self.macros = defaultdict(lambda: GLOBAL.CONFIG_ERROR, mainGunIcon=self.settings[MAIN_GUN.GUN_ICON],
                                  mainGunColor=self.colors[MAIN_GUN.NAME][MAIN_GUN.COLOR],
                                  mainGunDoneIcon=GLOBAL.EMPTY_LINE, mainGunFailureIcon=GLOBAL.EMPTY_LINE)
        self.gunIcons = {
            True: [self.settings[MAIN_GUN.DONE_ICON], self.settings[MAIN_GUN.FAILURE_ICON]],
            False: [GLOBAL.EMPTY_LINE, GLOBAL.EMPTY_LINE]
        }

    def updateTeamHealth(self, alliesHP, enemiesHP, totalAlliesHP, totalEnemiesHP):
        if not self._gunScore:
            self._gunScore = max(MAIN_GUN.MIN_GUN_DAMAGE, int(ceil(totalEnemiesHP * MAIN_GUN.DAMAGE_RATE)))
            self.gunLeft = self._gunScore
        if not self.playerDead:
            self.healthFailed = enemiesHP < self.gunLeft
            self.updateMainGun()

    def __onPlayerFeedbackReceived(self, events, *a, **kw):
        for event in events:
            if event.getType() == FEEDBACK_EVENT_ID.PLAYER_DAMAGED_HP_ENEMY:
                self.updateMainGun(damage=int(event.getExtra().getDamage()))

    def updateMainGun(self, damage=0):
        self.gunLeft -= damage
        achieved = self.gunLeft <= GLOBAL.ZERO
        self.macros["mainGun"] = GLOBAL.EMPTY_LINE if achieved else self.gunLeft
        self.macros["mainGunDoneIcon"] = self.gunIcons[achieved][GLOBAL.FIRST]
        self.macros["mainGunFailureIcon"] = self.gunIcons[self.healthFailed or self.playerDead][GLOBAL.LAST]
        self.as_mainGunTextS(self.settings[MAIN_GUN.TEMPLATE] % self.macros)

    def onCameraChanged(self, ctrlMode, vehicleID=None):
        if ctrlMode in POSTMORTEM.MODES and self.gunLeft > GLOBAL.ZERO:
            self.playerDead = True
            self.updateMainGun()
