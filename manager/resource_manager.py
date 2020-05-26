import pygame
from model.draw_object.image import Image


class ResourceManager:

    __images = {}

    @classmethod
    def get_image(cls, file_path: str) -> Image:
        if file_path in cls.__images.keys():
            return cls.__images[file_path]

        data = pygame.image.load(file_path)
        cls.__images[file_path] = data

        return data

    @classmethod
    def clear_images(cls):
        cls.__images = {}
