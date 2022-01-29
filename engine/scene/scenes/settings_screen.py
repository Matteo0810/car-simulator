from engine.scene.scene import Scene


class SettingsScreen(Scene):

    def __init__(self, root):
        super().__init__(root)

        self.add_label((self.mid_width - 60, 200), "Options", 25)
        self.add_button((self.mid_width - 30, 260), "Musique", SettingsScreen.music_onclick, 20)
        self.add_button((self.mid_width - 30, 310), "Retour", self.gui.previous_scene, 20)
    
    @staticmethod
    def music_onclick():
        import main
        if main.MUSIC_ON:
            main.stop_music()
        else:
            main.start_music()
