from armagomen._constants import ARCADE, POSTMORTEM
from armagomen.battle_observer.settings import user_settings
from armagomen.utils.common import overrideMethod
from AvatarInputHandler.control_modes import PostMortemControlMode


@overrideMethod(PostMortemControlMode, "enable")
def enablePostMortem(base, mode, **kwargs):
    if POSTMORTEM.PARAMS in kwargs:
        kwargs[POSTMORTEM.PARAMS] = (mode.camera.angles, user_settings.arcade_camera[ARCADE.START_DEAD_DIST])
    kwargs[POSTMORTEM.CAM_MATRIX] = mode.camera.camera.matrix
    kwargs.setdefault(POSTMORTEM.DURATION, 2.0)
    return base(mode, **kwargs)
