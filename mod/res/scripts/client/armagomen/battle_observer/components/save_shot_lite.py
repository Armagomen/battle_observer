# coding=utf-8
from Avatar import PlayerAvatar
from PlayerEvents import g_playerEvents
from armagomen.battle_observer.settings.default_settings import settings
from armagomen.constants import VEHICLE, MAIN
from armagomen.utils.common import overrideMethod, isReplay
from armagomen.utils.keys_listener import g_keysListener
from frameworks.wulf import WindowLayer
from gui.Scaleform.genConsts.BATTLE_VIEW_ALIASES import BATTLE_VIEW_ALIASES
from gui.shared.personality import ServicesLocator
from helpers import getClientLanguage, dependency
from messenger.MessengerEntry import g_instance
from skeletons.gui.battle_session import IBattleSessionProvider

lang = getClientLanguage()
if lang == 'uk':
    LOCKED_MESSAGE = 'Save Shot: Постріл у {} заблокований'
elif lang in ('ru', 'be'):
    LOCKED_MESSAGE = 'Save Shot: Выстрел в {} заблокирован'
else:
    LOCKED_MESSAGE = 'Save Shot: Shot in {} blocked'


class SaveShootLite(object):
    sessionProvider = dependency.descriptor(IBattleSessionProvider)

    def __init__(self):
        settings.onModSettingsChanged += self.onModSettingsChanged
        g_playerEvents.onAvatarReady += self.onEnterBattlePage
        g_playerEvents.onAvatarBecomeNonPlayer += self.onExitBattlePage
        self.enabled = False
        self.unlockShoot = False
        self.vehicleErrorComponent = None
        overrideMethod(PlayerAvatar, "shoot")(self.shoot)

    def shoot(self, base, avatar, isRepeat=False):
        if not self.enabled or self.unlockShoot or avatar.autoAimVehicle or not self.is_targetAllyOrDeath(avatar):
            return base(avatar, isRepeat=isRepeat)
        if isRepeat:
            return
        vehicleInfoVO = self.sessionProvider.getArenaDP().getVehicleInfo(avatar.target.id)
        message = LOCKED_MESSAGE.format(vehicleInfoVO.vehicleType.shortName)
        g_instance.gui.addClientMessage(message)
        if self.vehicleErrorComponent is not None:
            self.vehicleErrorComponent.as_showYellowMessageS(None, message)

    def onModSettingsChanged(self, config, blockID):
        if blockID == MAIN.NAME:
            self.enabled = config[MAIN.SAVE_SHOT] and not isReplay()

    def onEnterBattlePage(self):
        if self.enabled:
            g_keysListener.registerComponent(self.keyEvent)
            app = ServicesLocator.appLoader.getApp()
            if app is None:
                return
            battlePage = app.containerManager.getContainer(WindowLayer.VIEW).getView()
            if battlePage is None:
                return
            self.vehicleErrorComponent = battlePage.components.get(BATTLE_VIEW_ALIASES.VEHICLE_ERROR_MESSAGES)

    def onExitBattlePage(self):
        self.unlockShoot = False
        self.vehicleErrorComponent = None

    @staticmethod
    def is_targetAllyOrDeath(avatar):
        if avatar.target is not None and avatar.target.__class__.__name__ == VEHICLE.VEHICLE:
            return not avatar.target.isAlive() or avatar.target.publicInfo[VEHICLE.TEAM] == avatar.team
        return False

    def keyEvent(self, isKeyDown):
        self.unlockShoot = isKeyDown


save_shoot_lite = SaveShootLite()
