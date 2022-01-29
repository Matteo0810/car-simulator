import sys


class VersionException(Exception):
    pass


def check():
    if sys.version_info < (3, 9):
        raise VersionException('Version python invalide >= 3.9.')
    
    for module in ["tkinter", "pygame"]:
        try:
            __import__(module)
        except ImportError:
            raise RuntimeError(f'Veuillez installer le module {module}.')
