__author__ = "Armagomen"
__version__ = "1.33.8"
__copyright__ = "Copyright 2014-2021, Armagomen"
__credits__ = ["Armagomen"]
__license__ = "CC BY-NC-SA 4.0"
__maintainer__ = "Armagomen"
__email__ = "armagomen@gmail.com"
__status__ = "Production"
__http__ = "localhost"
__all__ = ['init', 'fini']

from armagomen.battle_observer.core import m_core


def init():
    m_core.start()


def fini():
    m_core.onExit()
