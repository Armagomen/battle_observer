# coding=utf-8
from armagomen._constants import MAIN, VEHICLE
from armagomen.battle_observer.settings import user_settings
from armagomen.utils.common import isReplay, overrideMethod
from armagomen.utils.keys_listener import g_keysListener
from Avatar import PlayerAvatar
from frameworks.wulf import WindowLayer
from gui.Scaleform.genConsts.BATTLE_VIEW_ALIASES import BATTLE_VIEW_ALIASES
from helpers import dependency, getClientLanguage
from messenger.MessengerEntry import g_instance
from PlayerEvents import g_playerEvents
from skeletons.gui.app_loader import IAppLoader
from skeletons.gui.battle_session import IBattleSessionProvider
from Vehicle import Vehicle

if getClientLanguage().lower() in ("uk", "be"):
    LOCKED_MESSAGE = 'Save Shot: Постріл у {} заблоковано'
else:
    LOCKED_MESSAGE = 'Save Shot: Shot in {} blocked'


class SaveShootLite(object):
    sessionProvider = dependency.descriptor(IBattleSessionProvider)
    appLoader = dependency.descriptor(IAppLoader)

    def __init__(self):
        user_settings.onModSettingsChanged += self.onModSettingsChanged
        g_playerEvents.onAvatarReady += self.onAvatarReady
        g_playerEvents.onAvatarBecomeNonPlayer += self.onAvatarBecomeNonPlayer
        self.enabled = user_settings.main[MAIN.SAVE_SHOT] and not isReplay()
        self.unlock = False
        self.vehicleErrorComponent = None
        overrideMethod(PlayerAvatar, "shoot")(self.shoot)

    def shoot(self, base, avatar, isRepeat=False):
        if isRepeat or not self.enabled or self.unlock or self.checkTarget(avatar):
            return base(avatar, isRepeat=isRepeat)
        vehicle_info = self.sessionProvider.getArenaDP().getVehicleInfo(avatar.target.id)
        message = LOCKED_MESSAGE.format(vehicle_info.vehicleType.shortName)
        g_instance.gui.addClientMessage(message)
        if self.vehicleErrorComponent is not None:
            self.vehicleErrorComponent.as_showYellowMessageS(None, message)

    def onModSettingsChanged(self, config, blockID):
        if blockID == MAIN.NAME:
            self.enabled = config[MAIN.SAVE_SHOT] and not isReplay()

    def onAvatarReady(self):
        if not self.enabled:
            return
        g_keysListener.registerComponent(self.keyEvent)
        battlePage = self.appLoader.getApp().containerManager.getContainer(WindowLayer.VIEW).getView()
        if battlePage is None:
            return
        self.vehicleErrorComponent = battlePage.components.get(BATTLE_VIEW_ALIASES.VEHICLE_ERROR_MESSAGES)

    def onAvatarBecomeNonPlayer(self):
        self.unlock = False
        self.vehicleErrorComponent = None

    @staticmethod
    def checkTarget(avatar):
        if avatar._PlayerAvatar__autoAimVehID != 0:
            return True
        if avatar.target is not None and isinstance(avatar.target, Vehicle):
            return avatar.target.isAlive() and avatar.target.publicInfo[VEHICLE.TEAM] != avatar.team
        return True

    def keyEvent(self, isKeyDown):
        self.unlock = isKeyDown


save_shoot_lite = SaveShootLite()


def fini():
    user_settings.onModSettingsChanged -= save_shoot_lite.onModSettingsChanged
    g_playerEvents.onAvatarReady -= save_shoot_lite.onAvatarReady
    g_playerEvents.onAvatarBecomeNonPlayer -= save_shoot_lite.onAvatarBecomeNonPlayer
