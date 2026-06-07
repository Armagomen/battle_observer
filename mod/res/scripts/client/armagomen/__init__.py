from armagomen._logger import IALogger

__all__ = ['IALogger']


def register_logger():
    from helpers.dependency import _g_manager, DependencyManager
    from armagomen._logger import _ALogger

    manager = _g_manager  # type: DependencyManager
    manager.addInstance(IALogger, _ALogger(), finalizer='fini')


inited = False
if not inited:
    register_logger()
    inited = True
