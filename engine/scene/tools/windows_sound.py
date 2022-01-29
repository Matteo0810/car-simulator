import winsound

from helpers.dotenv import get_env


def playsound(name):
    winsound.PlaySound(get_env("ASSETS_DIR") + name, winsound.SND_FILENAME | winsound.SND_LOOP | winsound.SND_ASYNC)


def stopsound():
    winsound.PlaySound(None, winsound.SND_PURGE)
