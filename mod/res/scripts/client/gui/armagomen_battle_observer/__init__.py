from .main import mod_battleObserver


def init():
    if mod_battleObserver.isLoading:
        mod_battleObserver.start()


def fini():
    if mod_battleObserver.isLoading:
        mod_battleObserver.fini()
