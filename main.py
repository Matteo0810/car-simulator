import sys

from helpers.dotenv import dotenv
from engine.scene.frame import Frame

if __name__ == "__main__":
    dotenv()
    
    if sys.platform == 'win32':
        import windows_sound as sound_module
    elif sys.platform == 'linux':
        pass
    
    try:
        sound_module.playsound("musics/title_screen.wav", 0.5)
    except:
        print("L'environnement ne permet pas de lancer une musique")
    
    frame = Frame()
    frame.show()
