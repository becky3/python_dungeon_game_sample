from pygame import locals


class Key:
    LEFT = locals.K_LEFT
    UP = locals.K_UP
    DOWN = locals.K_DOWN
    LEFT = locals.K_LEFT
    RIGHT = locals.K_RIGHT
    SPACE = locals.K_SPACE
    RETURN = locals.K_RETURN
    a = locals.K_a
    p = locals.K_p
    b = locals.K_b
    r = locals.K_r
    s = locals.K_s


class Color:
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    BLUE = (0, 0, 255)
    YELLOW = (255, 255, 0)
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
