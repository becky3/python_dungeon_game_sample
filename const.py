from pygame import locals as l


class Key:
    LEFT = l.K_LEFT
    UP = l.K_UP
    DOWN = l.K_DOWN
    LEFT = l.K_LEFT
    RIGHT = l.K_RIGHT
    SPACE = l.K_SPACE
    RETURN = l.K_RETURN
    a = l.K_a
    p = l.K_p
    b = l.K_b
    r = l.K_r
    s = l.K_s


class Color:
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    CYAN = (0, 255, 255)


class Direction:
    NEWTRAL = (0, 0)
    UP = (-1, 0)
    RIGHT = (0, 1)
    DOWN = (1, 0)
    LEFT = (0, -1)

    @classmethod
    def get_order(cls, direction: int) -> int:
        if direction == cls.UP:
            return 0
        if direction == cls.RIGHT:
            return 1
        if direction == cls.DOWN:
            return 2
        if direction == cls.LEFT:
            return 3
        return -1