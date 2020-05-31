import pygame
from model.draw_object.image import Image


class ResourceManager:

    __images = {}
    __sounds = {}

    @classmethod
    def get_image(cls, file_path: str) -> Image:
        if file_path in cls.__images.keys():
            return cls.__images[file_path]

        data = pygame.image.load(file_path)
        cls.__images[file_path] = data

        return data

    @classmethod
    def get_sound(cls, file_path: str) -> pygame.mixer.Sound:
        if file_path in cls.__sounds.keys():
            return cls.__sounds[file_path]

        data = pygame.mixer.Sound(file_path)
        cls.__sounds[file_path] = data

        return data

    @classmethod
    def clear_images(cls):
        cls.__images = {}
