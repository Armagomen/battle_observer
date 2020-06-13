def check():
    from ..core.bw_utils import logWarning
    from ..core.bo_constants import API_VERSION
    try:
        from gui.modsListApi import g_modsListApi
        from gui.vxSettingsApi import vxSettingsApi, vxSettingsApiEvents, __version__
    except ImportError as err:
        msg = "%s: Settings API not loaded" % repr(err)
        logWarning(msg)
    else:
        from distutils.version import LooseVersion
        if LooseVersion(__version__) >= LooseVersion(API_VERSION):
            from .config_interface import ConfigInterface
            c_Interface = ConfigInterface(g_modsListApi, vxSettingsApi, vxSettingsApiEvents)
            c_Interface.start()
        else:
            msg = "Settings API not loaded, v{} it`s fake or not supported api, current version is {}, " \
                  "please remove old versions from mods dir.".format(__version__, API_VERSION)
            logWarning(msg)
