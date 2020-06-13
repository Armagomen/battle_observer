from chat_shared import SYS_MESSAGE_TYPE
from messenger.proto.bw.ServiceChannelManager import ServiceChannelManager
from ..core.bo_constants import SERVICE_CHANNEL, GLOBAL
from ..core.core import overrideMethod
from ..core.events import g_events

channel_filter = set()


@overrideMethod(ServiceChannelManager, "__addClientMessage")
def addClientMessage(base, *args, **kwargs):
    auxData = kwargs.get(SERVICE_CHANNEL.AUX_DATA)
    if auxData and type(auxData) is list and auxData[GLOBAL.FIRST] in channel_filter:
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


def onSettingsChanged(config, blockID):
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


g_events.onSettingsChanged += onSettingsChanged
