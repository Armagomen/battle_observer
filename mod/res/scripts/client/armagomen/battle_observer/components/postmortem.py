from AvatarInputHandler.control_modes import PostMortemControlMode
from armagomen.battle_observer.core import settings
from armagomen.bo_constants import POSTMORTEM, GLOBAL, ARCADE
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
    kwargs[POSTMORTEM.DURATION] = GLOBAL.ONE_SECOND
    if not ((mode._isPostmortemDelayEnabled() or bool(kwargs.get('respawn', False)))
            and bool(kwargs.get('bPostmortemDelay'))):
        mode._PostMortemControlMode__postmortemDelay = PostmortemDelay()

        def setDelayDisabled():
            mode._PostMortemControlMode__postmortemDelay = None

        callback(GLOBAL.ONE_SECOND, setDelayDisabled)
    return base(mode, **kwargs)
