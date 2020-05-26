import pygame


class Music:
    TITLE = "resource/sound/title.ogg"
    DUNGEON = "resource/sound/title.ogg"
    GAME_OVER = "resource/sound/title.ogg"


class SE:
    ATTACK = ""
    BOM = ""
    POTION = ""
    LEVEL_UP = ""
    WIN = ""


class SoundManager:

    def play_music(self, file_path: str):
        self.stop_music()
        pygame.mixer_music.load(file_path)
        pygame.mixer_music.play(-1)

    def stop_music(self):
        pygame.mixer_music.stop()

    def play_se(self, file_path: str):
        pygame.mixer.Sound(file_path).play()
