import sys

import requirement

requirement.check()

from helpers.dotenv import dotenv
from engine.scene.frame import Frame

if sys.platform == 'win32':
    import windows_sound as sound_module


MUSIC_ON = False


def start_music():
    try:
        sound_module.playsound("musics/title_screen.wav", 1)  # volume est inutilisé
    except BaseException as e:
        print("L'environnement ne permet pas de lancer une musique")
        print(str(e))
    
    global MUSIC_ON
    MUSIC_ON = True


def stop_music():
    try:
        sound_module.stopsound()
    except BaseException as e:
        print("L'environnement ne permet pas d'arreter une musique")
        print(str(e))
    
    global MUSIC_ON
    MUSIC_ON = False


if __name__ == "__main__":
    dotenv()
    
    frame = Frame()
    frame.show()
