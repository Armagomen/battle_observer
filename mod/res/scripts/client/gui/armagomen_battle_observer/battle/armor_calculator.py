from collections import defaultdict

from AvatarInputHandler import AvatarInputHandler
from aih_constants import SHOT_RESULT
from gui.Scaleform.daapi.view.battle.shared.crosshair.plugins import ShotResultIndicatorPlugin
from gui.battle_control import avatar_getter
from ..core.battle_cache import cache as g_cache
from ..core.bo_constants import ARMOR_CALC, GLOBAL, VEHICLE
from ..core.config import cfg
from ..core.events import g_events
from ..meta.battle.armor_calc_meta import ArmorCalcMeta

config = cfg.armor_calculator


class ArmorCalculator(ArmorCalcMeta):

    def __init__(self):
        super(ArmorCalculator, self).__init__()
        self._visible = False
        self.p100 = GLOBAL.F_ONE
        self.p500 = GLOBAL.F_ONE
        self.calcCache = GLOBAL.ZERO
        self.calcMacro = defaultdict(lambda: GLOBAL.CONFIG_ERROR)
        self.messages = ARMOR_CALC.DEFAULT_MESSAGES
        self.messages.update(config[ARMOR_CALC.MESSAGES])
        self.typeColors = cfg.colors[ARMOR_CALC.NAME]
        self.template = config[ARMOR_CALC.TEMPLATE]
        self.showCalcPoints = config[ARMOR_CALC.SHOW_POINTS]
        self.showTextMessage = config[ARMOR_CALC.SHOW_MESSAGE]
        self.wg_updateColor = ShotResultIndicatorPlugin._ShotResultIndicatorPlugin__updateColor

    def onEnterBattlePage(self):
        super(ArmorCalculator, self).onEnterBattlePage()
        ammo = self.sessionProvider.shared.ammo
        if ammo is not None:
            ammo.onGunReloadTimeSet += self.onGunReload
        g_events.onPlayerVehicleDeath += self.clearView
        handler = avatar_getter.getInputHandler()
        if handler is not None:
            if isinstance(handler, AvatarInputHandler):
                handler.onCameraChanged += self.onCameraChanged
        self.updateShootParams()

    def onExitBattlePage(self):
        ammo = self.sessionProvider.shared.ammo
        if ammo is not None:
            ammo.onGunReloadTimeSet -= self.onGunReload
        g_events.onPlayerVehicleDeath -= self.clearView
        handler = avatar_getter.getInputHandler()
        if handler is not None:
            if isinstance(handler, AvatarInputHandler):
                handler.onCameraChanged -= self.onCameraChanged
        super(ArmorCalculator, self).onExitBattlePage()

    def _populate(self):
        super(ArmorCalculator, self)._populate()
        self.as_startUpdateS(config)
        ShotResultIndicatorPlugin._ShotResultIndicatorPlugin__updateColor = lambda *args: self.updateColor(*args)

    def _dispose(self):
        ShotResultIndicatorPlugin._ShotResultIndicatorPlugin__updateColor = self.wg_updateColor
        super(ArmorCalculator, self)._dispose()

    def onCameraChanged(self, ctrlMode, *args, **kwargs):
        self.as_onControlModeChangedS(ctrlMode)

    def updateShootParams(self):
        shotParams = g_cache.player.getVehicleDescriptor().shot
        self.p100, self.p500 = shotParams.piercingPower
        self.calcMacro.update(piercingPower=self.p100, caliber=shotParams.shell.caliber)

    def onGunReload(self, shellID, state):
        if state.isReloadingFinished():
            self.updateShootParams()
            if self._visible:
                self.as_armorCalcS(self.template % self.calcMacro)

    def updateColor(self, iPlugin, markerType, targetPos, collision, direction):
        colors = iPlugin._ShotResultIndicatorPlugin__colors
        armor_sum, counted_armor, result = self.getCountedArmor(collision, targetPos, direction)
        if result in colors:
            color = colors[result]
            cache = iPlugin._ShotResultIndicatorPlugin__cache
            setGunMarkerColor = iPlugin._parentObj.setGunMarkerColor
            if cache[markerType] != result and setGunMarkerColor(markerType, color):
                cache[markerType] = result
                if self.showTextMessage:
                    self.as_setCalcMessageS(bool(result), self.messages.get(color, GLOBAL.EMPTY_LINE))
                if counted_armor is None:
                    self.clearView()
                    return
            if self.showCalcPoints and result != SHOT_RESULT.UNDEFINED:
                self.pushCountedResultToFlash(armor_sum, color, counted_armor)

    def pushCountedResultToFlash(self, armorSum, color, countedArmor):
        if self.calcCache != countedArmor:
            self.calcCache = countedArmor
            if countedArmor:
                self.calcMacro[ARMOR_CALC.MACROS_COLOR] = self.typeColors[color]
                self.calcMacro[ARMOR_CALC.MACROS_CALCED_ARMOR] = countedArmor
                self.calcMacro[ARMOR_CALC.MACROS_ARMOR] = armorSum
                self.calcMacro[ARMOR_CALC.MACROS_PIERCING_RESERVE] = self.p100 - countedArmor
                self.as_armorCalcS(self.template % self.calcMacro)
                self.setVisible(True)

    def setVisible(self, value):
        if not self._visible or self._visible != value:
            self._visible = value

    def clearView(self, *args):
        if self.showCalcPoints:
            self.as_armorCalcS(GLOBAL.EMPTY_LINE)
        if self.showTextMessage:
            self.as_setCalcMessageS(False, GLOBAL.EMPTY_LINE)
        self.setVisible(False)

    def getCountedArmor(self, collision, targetPos, direction):
        if collision and collision.isVehicle:
            entity = collision.entity
            if entity.publicInfo[VEHICLE.TEAM] != g_cache.allyTeam and entity.isAlive():
                details = self.getAllCollisionDetails(targetPos, direction, entity)
                if details is not None:
                    notUseCos = GLOBAL.ZERO
                    useCos = GLOBAL.ZERO
                    armorSum = GLOBAL.ZERO
                    fDist = details[GLOBAL.FIRST][GLOBAL.FIRST] + details[GLOBAL.LAST][GLOBAL.FIRST]
                    midDist = fDist * ARMOR_CALC.HALF
                    for dist, hitAngleCos, matInfo, compIdx in details:
                        if midDist > dist and matInfo:
                            if compIdx not in ARMOR_CALC.SKIP_DETAILS and hitAngleCos > GLOBAL.ZERO:
                                useCos += matInfo.armor / hitAngleCos
                            else:
                                notUseCos += matInfo.armor
                            armorSum += matInfo.armor
                    counted_armor = useCos + notUseCos
                    return armorSum, counted_armor, self.getShotResult(counted_armor, targetPos)
        return ARMOR_CALC.NONEDATA

    def getShotResult(self, countedArmor, targetPos):
        power = self.p100
        if power != self.p500:
            dist = (targetPos - g_cache.player.getOwnVehiclePosition()).length
            if dist > ARMOR_CALC.MIN_DIST:
                result = power + (self.p500 - power) * (dist - ARMOR_CALC.MIN_DIST) / ARMOR_CALC.EFFECTIVE_DISTANCE
                power = max(self.p500, result)
        if countedArmor < power * ARMOR_CALC.GREAT_PIERCED:
            return SHOT_RESULT.GREAT_PIERCED
        elif countedArmor > power * ARMOR_CALC.NOT_PIERCED:
            return SHOT_RESULT.NOT_PIERCED
        else:
            return SHOT_RESULT.LITTLE_PIERCED

    @staticmethod
    def getAllCollisionDetails(targetPos, direction, entity):
        startPoint = targetPos - direction * ARMOR_CALC.BACKWARD_LENGTH
        endPoint = targetPos + direction * ARMOR_CALC.FORWARD_LENGTH
        return entity.collideSegmentExt(startPoint, endPoint)
