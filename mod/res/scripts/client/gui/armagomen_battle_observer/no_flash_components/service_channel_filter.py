import re

from chat_shared import SYS_MESSAGE_TYPE
from gui.SystemMessages import pushMessage, SM_TYPE
from gui.shared.personality import ServicesLocator
from helpers import getClientLanguage
from messenger.proto.bw.ServiceChannelManager import ServiceChannelManager
from notification.NotificationListView import NotificationListView
from notification.NotificationPopUpViewer import NotificationPopUpViewer
from ..core import cfg
from ..core.bo_constants import SERVICE_CHANNEL, GLOBAL, URLS
from ..core.utils.common import openWebBrowser, overrideMethod

channel_filter = set()


@overrideMethod(ServiceChannelManager, "__addClientMessage")
def addClientMessage(base, *args, **kwargs):
    aux_data = kwargs.get(SERVICE_CHANNEL.AUX_DATA)
    if aux_data and type(aux_data) is list:
        first_element = aux_data[GLOBAL.FIRST]
        if type(first_element) is not dict and first_element in channel_filter:
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


def onModSettingsChanged(config, blockID):
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


cfg.onModSettingsChanged += onModSettingsChanged


@overrideMethod(NotificationListView, "onClickAction")
@overrideMethod(NotificationPopUpViewer, "onClickAction")
def clickAction(base, view, typeID, entityID, action):
    if action in URLS.DONATE:
        return openWebBrowser(action)
    return base(view, typeID, entityID, action)


def onConnected():
    if getClientLanguage().lower() in GLOBAL.RU_LOCALIZATION:
        pushMessage(URLS.DONATE_RU_MESSAGE, type=SM_TYPE.Warning)
    else:
        pushMessage(URLS.DONATE_EU_MESSAGE, type=SM_TYPE.Warning)


ServicesLocator.connectionMgr.onConnected += onConnected
