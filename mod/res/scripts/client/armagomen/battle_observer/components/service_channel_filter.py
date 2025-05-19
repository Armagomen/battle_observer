from armagomen._constants import GLOBAL, SERVICE_CHANNEL
from armagomen.battle_observer.settings import user_settings
from armagomen.utils.common import overrideMethod
from chat_shared import SYS_MESSAGE_TYPE
from messenger.proto.bw.ServiceChannelManager import ServiceChannelManager

channel_filter = set()


@overrideMethod(ServiceChannelManager, "__addClientMessage")
def addClientMessage(base, *args, **kwargs):
    aux_data = kwargs.get(SERVICE_CHANNEL.AUX_DATA)
    if aux_data and type(aux_data) == list:
        first_element = aux_data[GLOBAL.ZERO]
        if not isinstance(first_element, dict) and first_element in channel_filter:
            return
    return base(*args, **kwargs)


@overrideMethod(ServiceChannelManager, "onReceiveSysMessage")
def onReceiveSysMessage(base, manager, chatAction):
    if chatAction.has_key(SERVICE_CHANNEL.DATA):
        data = dict(chatAction[SERVICE_CHANNEL.DATA])
        if data.get(SERVICE_CHANNEL.TYPE, None) in channel_filter:
            return
    return base(manager, chatAction)


@overrideMethod(ServiceChannelManager, "onReceivePersonalSysMessage")
def onReceivePersonalSysMessage(base, manager, chatAction):
    if chatAction.has_key(SERVICE_CHANNEL.DATA):
        data = dict(chatAction[SERVICE_CHANNEL.DATA])
        if data.get(SERVICE_CHANNEL.TYPE, None) in channel_filter:
            return
    return base(manager, chatAction)


def _onModSettingsChanged(config, blockID):
    if blockID == SERVICE_CHANNEL.NAME:
        channel_filter.clear()
        if config[GLOBAL.ENABLED]:
            for name, enabled in config[SERVICE_CHANNEL.KEYS].iteritems():
                if enabled:
                    item = SYS_MESSAGE_TYPE.lookup(name)
                    if item is not None:
                        channel_filter.add(item.index())
                    else:
                        channel_filter.add(name)


user_settings.onModSettingsChanged += _onModSettingsChanged


def fini():
    user_settings.onModSettingsChanged -= _onModSettingsChanged
