import winsound

from helpers.dotenv import get_env


def playsound(name, volume):
    winsound.PlaySound(get_env("ASSETS_DIR") + name, winsound.SND_FILENAME | winsound.SND_LOOP | winsound.SND_ASYNC)
