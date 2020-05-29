import pygame

from const import Key, Direction


class InputManager:

    __key_pressed = []

    @classmethod
    def updateEvents(cls):
        cls.__key_pressed = pygame.key.get_pressed()

    @classmethod
    def get_push_direction(cls) -> int:

        if cls.isPush(Key.UP):
            return Direction.UP
        if cls.isPush(Key.RIGHT):
            return Direction.RIGHT
        if cls.isPush(Key.DOWN):
            return Direction.DOWN
        if cls.isPush(Key.LEFT):
            return Direction.LEFT
        return Direction.NEWTRAL

    @classmethod
    def isPush(cls, key_code: int) -> bool:
        if len(cls.__key_pressed) < key_code:
            return False
        return cls.__key_pressed[key_code]

    @classmethod
    def isQuit(cls) -> bool:
        for event in pygame.event.get():
            if event.type == pygame.locals.QUIT:
                return True
        return False
