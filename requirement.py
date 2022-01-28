import sys
import subprocess


class VersionException(Exception):
    pass


if sys.version_info >= (3, 9):
    raise VersionException('Version python invalide >= 3.9.')

for module in ["tkinter", "pygame"]:
    try:
        subprocess.call(f'pip install {module}')
    except ModuleNotFoundError:
        raise ModuleNotFoundError(f'Impossible d\'installer le module {module}.')
