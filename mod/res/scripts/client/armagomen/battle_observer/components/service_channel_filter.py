from armagomen._constants import SERVICE_CHANNEL
from armagomen.battle_observer.settings.interface import IBOSettingsLoader
from armagomen.utils.common import toggleOverride
from chat_shared import SYS_MESSAGE_TYPE
from helpers import dependency
from messenger.proto.bw.ServiceChannelManager import ServiceChannelManager


class ServiceChannelFilter(object):
    settingsLoader = dependency.descriptor(IBOSettingsLoader)

    def __init__(self):
        self.enabled = False
        self.channel_filter = set()
        self.settingsLoader.onModSettingsChanged += self._onModSettingsChanged

    def fini(self):
        self.channel_filter.clear()
        self.settingsLoader.onModSettingsChanged -= self._onModSettingsChanged

    def addClientMessage(self, base, *args, **kwargs):
        aux_data = kwargs.get(SERVICE_CHANNEL.AUX_DATA)
        if aux_data and type(aux_data) == list:
            first_element = aux_data[0]
            if not isinstance(first_element, dict) and first_element in self.channel_filter:
                return None
        return base(*args, **kwargs)

    def onReceiveMessage(self, base, manager, chatAction, *args, **kwargs):
        if chatAction.has_key(SERVICE_CHANNEL.DATA):
            data = dict(chatAction[SERVICE_CHANNEL.DATA])
            if data.get(SERVICE_CHANNEL.TYPE, None) in self.channel_filter:
                return None
        return base(manager, chatAction, *args, **kwargs)

    def _onModSettingsChanged(self, name, data):
        if name == SERVICE_CHANNEL.NAME:
            for setting, enabled in data.items():
                item = SYS_MESSAGE_TYPE.lookup(setting)
                key = item.index() if item is not None else setting
                if enabled:
                    self.channel_filter.add(key)
                else:
                    self.channel_filter.discard(key)

            enabled = bool(self.channel_filter)

            if self.enabled != enabled:
                self.enabled = enabled
                toggleOverride(ServiceChannelManager, "onReceivePersonalSysMessage", self.onReceiveMessage, self.enabled)
                toggleOverride(ServiceChannelManager, "onReceiveSysMessage", self.onReceiveMessage, self.enabled)
                toggleOverride(ServiceChannelManager, "__addClientMessage", self.addClientMessage, self.enabled)


c_filter = ServiceChannelFilter()


def fini():
    c_filter.fini()
