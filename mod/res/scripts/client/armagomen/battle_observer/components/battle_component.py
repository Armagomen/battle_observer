import math

from CurrentVehicle import g_currentVehicle
from PlayerEvents import g_playerEvents
from armagomen.battle_observer.settings.default_settings import settings
from armagomen.constants import MAIN, GLOBAL, DAMAGE_LOG
from armagomen.utils.common import setMaxFrameRate, logDebug
from gui.battle_control.controllers import msgs_ctrl

BASE_NOTIFICATIONS = (msgs_ctrl._ALLY_KILLED_SOUND, msgs_ctrl._ENEMY_KILLED_SOUND)


def onModSettingsChanged(_settings, blockID):
    if blockID == MAIN.NAME:
        if _settings[MAIN.ENABLE_FPS_LIMITER]:
            setMaxFrameRate(_settings[MAIN.MAX_FRAME_RATE])
        if _settings[MAIN.DISABLE_SCORE_SOUND] and msgs_ctrl._ALLY_KILLED_SOUND is not None:
            msgs_ctrl._ALLY_KILLED_SOUND = msgs_ctrl._ENEMY_KILLED_SOUND = None
        elif not _settings[MAIN.DISABLE_SCORE_SOUND] and msgs_ctrl._ALLY_KILLED_SOUND is None:
            msgs_ctrl._ALLY_KILLED_SOUND, msgs_ctrl._ENEMY_KILLED_SOUND = BASE_NOTIFICATIONS


def onArenaCreated():
    if settings.log_total[GLOBAL.ENABLED]:
        try:
            dossier = g_currentVehicle.getDossier()
            if dossier:
                damage = dossier.getRandomStats().getAvgDamage()
                assist = dossier.getRandomStats().getDamageAssistedEfficiencyWithStan()
                if damage is not None:
                    damage = math.floor(damage)
                    DAMAGE_LOG.AVG_DAMAGE_DATA = damage
                if assist is not None:
                    assist = math.floor(assist)
                logDebug("set vehicle efficiency (avgDamage: {}, avgAssist: {})", damage, assist)
        except AttributeError:
            DAMAGE_LOG.AVG_DAMAGE_DATA = GLOBAL.ZERO


g_playerEvents.onArenaCreated += onArenaCreated
settings.onModSettingsChanged += onModSettingsChanged
