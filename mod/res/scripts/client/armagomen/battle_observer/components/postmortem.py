from armagomen._constants import ARCADE, POSTMORTEM
from armagomen.battle_observer.settings import user
from armagomen.utils.common import callback, overrideMethod
from AvatarInputHandler.control_modes import PostMortemControlMode


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
        kwargs[POSTMORTEM.PARAMS] = (mode.camera.angles, user.arcade_camera[ARCADE.START_DEAD_DIST])
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
