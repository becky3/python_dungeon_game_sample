
import random

from libs.matrix import Matrix
from const import Direction
from game.game_info import GameInfo
from game.game_system import GameSystem
from model.item import Item
from model.dungeon import Dungeon
from model.draw_object.image import Image
from model.character_chip import CharacterChip
from model.event.event import Event


class Player(Event):

    class CharacterType:
        NORMAL = 0
        DIE = 1

    __IMAGE = "resource/image/player.png"

    @property
    def level(self) -> int:
        return self.__level

    @property
    def hp(self) -> int:
        return self.__hp

    @property
    def max_hp(self) -> int:
        return self.__max_hp

    @property
    def strength(self) -> int:
        return self.__strength

    @property
    def satiation(self) -> int:
        return self.__satiation

    @property
    def potion(self) -> int:
        return self.__potion

    @property
    def blazegem(self) -> int:
        return self.__blazegem

    @property
    def next_position(self) -> (int, int):
        return self.__next_position

    def __init__(self,
                 position: (float, float),
                 game_system: GameSystem,
                 game_info: GameInfo,
                 dungeon: Dungeon
                 ):
        super().__init__(position)

        self.__dungeon = dungeon
        self.__event_map: Matrix = None
        self.__game_system = game_system
        self.__game_info = game_info
        self.__walk_frame = 2
        self.__walk_plan = []
        self.__anime_frame = 0
        self.__pre_direction = Direction.NEWTRAL
        self.__next_position: (int, int) = None
        self.__character_chip = CharacterChip(
            (16, 16),
            (16 * 4, 16 * 4),
            direction_pattern_num=4
        )

        self.__direction = 0

        self.__satiation = 0
        self.__potion = 0
        self.__blazegem = 0

        self.__level = 0
        self.__hp = 0
        self.__max_hp = 0
        self.__strength = 0

    def reset_status(self):
        self.__level = 1
        self.__max_hp = 300
        self.__hp = self.__max_hp
        self.__strength = 100
        self.__satiation = 300
        self.__potion = 0
        self.__blazegem = 0

    # TODO: __init__で設定したい
    def set_event_map(self, event_map: Matrix):
        self.__event_map = event_map

    def __hungry_by_move(self):
        if self.__satiation <= 0:
            self.__add_hp(-5)
            return

        self.__satiation = self.__satiation - 1
        if self.__hp < self.__max_hp:
            self.__add_hp(1)

    def is_die(self) -> bool:
        return self.__hp <= 0

    def add_item(self, item: Item):
        item_type = item.item_type
        if item_type == Item.Type.POTION:
            self.__potion += 1
            return
        if item_type == Item.Type.BLAZE_GEM:
            self.__blazegem += 1
            return
        if item_type == Item.Type.FOOD_SPOILED:
            self.__satiation = int(self.__satiation / 2)
            return
        if item_type == Item.Type.FOOD_ADD_20:
            self.__satiation += 20
            return
        if item_type == Item.Type.FOOD_ADD_100:
            self.__satiation += 100
            return

    def setup_start_position(self):

        floor_map = self.__dungeon.floor_map
        height, width = floor_map.shape

        while True:
            y = random.randint(3, height - 4)
            x = random.randint(3, width - 4)
            self.set_position((y, x))
            if floor_map[y, x] == 0:
                break
        self.__direction = Direction.DOWN

    def set_character_type(self, _type: int):
        self.__character_chip.set_character_no(_type)

    def __can_move(self, direction: (int, int)) -> bool:
        if direction == Direction.NEWTRAL:
            return False

        next_position = self.__get_next_position(direction)

        if self.__dungeon.floor_map[next_position] == 9:
            return False

        return True

    def __get_direction_no(self) -> int:
        order = Direction.get_order(self.__direction)
        if order == -1:
            order = 2
        return order

    def __get_next_position(self, direction: (int, int)) -> (int, int):
        y, x = direction
        next_position = (
            self.map_coordinate[0] + y,
            self.map_coordinate[1] + x
        )
        return next_position

    def ready_move(self, direction: (int, int)) -> bool:

        if not self.__can_move(direction):
            return False

        next_position = self.__get_next_position(direction)

        self.__next_position = next_position
        self.__direction = direction
        self.__hungry_by_move()
        self.__pre_direction = direction

        one_value = 1.0 / float(self.__walk_frame)
        self.__walk_plan = [one_value] * self.__walk_frame

        return True

    def __get_animation_image(self) -> Image:
        file_path = self.__IMAGE
        rect = self.__character_chip.get_draw_rect(
            self.__get_direction_no(),
            self.__anime_frame
        )

        return Image(file_path, area_rect=rect)

    def __do_move(self):
        self.__anime_frame += 1
        y, x = self.__direction
        value = self.__walk_plan.pop()
        position = (
            self.y + float(y) * value,
            self.x + float(x) * value
        )
        self.set_position(position)
        if len(self.__walk_plan) == 0:
            self.__moved()

    def __moved(self):
        self.set_position(self.__next_position)
        self.__next_position = None

    def battle(self, enemy: object):
        # 相互importとなるため、関数内部で型解決
        from model.event.enemy import Enemy
        _enemy: Enemy = enemy
        damage = _enemy.strength + _enemy.level
        self.__add_hp(-damage)

    def __add_hp(self, value: int):
        self.__hp += value
        if self.__hp < 0:
            self.__hp = 0

        if self.__hp > self.__max_hp:
            self.__hp = self.__max_hp

    def back(self):
        y, x = self.__pre_direction
        self.add_position((y * -1, x * -1))

    def is_moving(self) -> bool:
        return self.__next_position is not None

    def set_direction(self, direction: int):
        self.__direction = direction

    def update(self):

        if self.__next_position is None:
            return

        self.__do_move()

    def draw(self):
        position = self.__game_info.convert_map_to_display(
            (self.x, self.y)
        )
        image = self.__get_animation_image()
        image.set_position(position)
        self.__game_system.add_draw_object(image)
