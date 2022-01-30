import sys
import pkgutil


class VersionException(Exception):
    pass


def check():
    if sys.version_info < (3, 9):
        raise VersionException('Version python invalide >= 3.9.')
    
    for module in ["tkinter", "pygame"]:
        if not pkgutil.get_loader(module):
            raise RuntimeError(f'Veuillez installer le module {module}.')
