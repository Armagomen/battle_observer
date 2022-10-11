import BigWorld
from Math import Matrix, Vector3

from armagomen.utils.common import overrideMethod, logError
from avatar_components.avatar_chat_key_handling import AvatarChatKeyHandling
from math_utils import createTranslationMatrix

getVehicleMatrixProviderErr = "fixed: AvatarChatKeyHandling __getVehicleMatrixProvider, {}"


@overrideMethod(AvatarChatKeyHandling, "__getVehicleMatrixProvider")
def __getVehicleMatrixProviderFix(base, chatKey, cmd, vehicleID=None):
    try:
        return base(chatKey, cmd, vehicleID=vehicleID)
    except Exception as err:
        logError(getVehicleMatrixProviderErr, repr(err))
        if vehicleID is None:
            vehicleID = chatKey._AvatarChatKeyHandling__getVehicleIDByCmd(cmd)
        vehicle = BigWorld.entities.get(vehicleID)
        if vehicle is None:
            position = BigWorld.player().arena.positions.get(vehicleID)
            if position is not None:
                maxDistance = 600.0
                playerVehiclePosition = BigWorld.player().getOwnVehiclePosition()
                if Vector3(position).distSqrTo(playerVehiclePosition) > maxDistance * maxDistance:
                    direction = Vector3(position) - playerVehiclePosition
                    direction.normalise()
                    return createTranslationMatrix(playerVehiclePosition + direction * maxDistance)
                return createTranslationMatrix(position)
            return
        else:
            return Matrix(vehicle.matrix)
