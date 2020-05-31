import pygame

from manager.resource_manager import ResourceManager


class Music:
    TITLE = "resource/music/title.ogg"
    DUNGEON = "resource/music/dungeon.ogg"
    GAME_OVER = "resource/music/game_over.ogg"


class SE:
    ATTACK = "resource/se/attack.wav"
    ENEMY_DOWN = "resource/se/enemy_down.wav"
    GOOD_ITEM = "resource/se/good_item.wav"
    BAD_ITEM = "resource/se/bad_item.wav"
    CHANGE_FLOOR = "resource/se/change_floor.wav"
    BOM = "resource/se/bom.wav"
    POTION = "resource/se/potion.wav"
    LEVEL_UP = "resource/se/level_up.wav"
    BUMP = "resource/se/bump.wav"


class SoundManager:

    def play_music(self, file_path: str):
        self.stop_music()
        pygame.mixer_music.load(file_path)
        pygame.mixer_music.play(-1)

    def stop_music(self):
        pygame.mixer_music.stop()

    def play_se(self, file_path: str):
        ResourceManager.get_sound(file_path).play()
