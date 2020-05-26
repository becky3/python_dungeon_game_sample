import pygame

class InputManager:

    __key_pressed = []

    @classmethod
    def updateEvents(cls):
        cls.__key_pressed = pygame.key.get_pressed()

    @classmethod
    def isPush(cls, key_code : int) -> bool:
        if len(cls.__key_pressed) < key_code:
            return False
        return cls.__key_pressed[key_code]

    @classmethod
    def isQuit(cls) -> bool:
        for event in pygame.event.get():
            if event.type == pygame.locals.QUIT:
                return True
        return False
