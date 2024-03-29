from AvatarInputHandler.control_modes import PostMortemControlMode
from armagomen._constants import POSTMORTEM, ARCADE
from armagomen.battle_observer.settings.default_settings import settings
from armagomen.utils.common import overrideMethod, callback


class PostmortemDelay(object):

    def destroy(self):
        pass

    def start(self):
        pass

    def stop(self):
        pass

    def handleMouseEvent(self, *args):
        pass


@overrideMethod(PostMortemControlMode, "enable")
def enablePostMortem(base, mode, **kwargs):
    if POSTMORTEM.PARAMS in kwargs:
        kwargs[POSTMORTEM.PARAMS] = (mode.camera.angles, settings.arcade_camera[ARCADE.START_DEAD_DIST])
    kwargs[POSTMORTEM.CAM_MATRIX] = mode.camera.camera.matrix
    kwargs[POSTMORTEM.DURATION] = 1.0
    respawn = bool(kwargs.get('respawn', False))
    bPostmortemDelay = bool(kwargs.get('bPostmortemDelay', False))
    if not ((mode._isPostmortemDelayEnabled() or respawn) and bPostmortemDelay):
        mode._PostMortemControlMode__postmortemDelay = PostmortemDelay()

        def setDelayDisabled():
            mode._PostMortemControlMode__postmortemDelay = None

        callback(1.0, setDelayDisabled)
    return base(mode, **kwargs)
