import math
import random

from const import Direction, Color
from game.game_info import GameInfo
from game.game_system import GameSystem
from model.item import Item
from model.mover import Mover
from model.dungeon import Dungeon
from model.draw_object.text import Text
from model.draw_object.image import Image
from model.character_chip import CharacterChip
from model.event.event import Event
from manager.debug_manager import DebugManager


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
    def bom(self) -> int:
        return self.__bom

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
        self.__game_system = game_system
        self.__game_info = game_info
        self.__mover = Mover()
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
        self.__bom = 0

        self.__level = 0
        self.__hp = 0
        self.__max_hp = 0
        self.__strength = 0
        self.__limit_level = 99
        self.__limit_strength = 999
        self.__limit_hp = 999
        self.__pre_damage = 0
        self.__damage_view_time = 0

    def reset_status(self):
        self.__level = 1
        self.__max_hp = 300
        self.__hp = self.__max_hp
        self.__strength = 100
        self.__satiation = 300
        self.__potion = 0
        self.__bom = 0

        if DebugManager.is_debug:
            for _ in range(1, DebugManager.level):
                self.level_up()
            self.__potion = DebugManager.potion
            self.__bom = DebugManager.bom

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
        if item_type == Item.Type.BOM:
            self.__bom += 1
            return
        if item_type == Item.Type.SA_SPOILED:
            self.__satiation = int(self.__satiation / 2)
            return
        if item_type == Item.Type.SA_ADD_20:
            self.__satiation += 20
            return
        if item_type == Item.Type.SA_ADD_100:
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

    def use_item(self, item: Item):
        if item.item_type == Item.Type.POTION:
            self.__add_hp(500)
            self.__potion -= 1
            if self.__potion <= 0:
                self.__potion = 0
        if item.item_type == Item.Type.BOM:
            self.__bom -= 1
            if self.__bom <= 0:
                self.__bom = 0

    def __can_move(self, direction: (int, int)) -> bool:
        if direction == Direction.NEWTRAL:
            return False

        next_position = self.__get_next_position(direction)

        floor_map = self.__dungeon.floor_map

        if not floor_map.is_in(next_position):
            return False

        if floor_map[next_position] == 9:
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

    def level_up(self):
        self.__level += 1
        if self.__level > self.__limit_level:
            self.__level = self.__limit_level
        hp = random.randint(10, 20 + math.floor(self.__level / 2))
        strength = random.randint(5, 10 + math.floor(self.__level / 2))
        self.__add_max_hp(hp)
        self.__add_hp(hp)
        self.__add_strength(strength)

    def ready_move(self, direction: (int, int)) -> bool:

        if not self.__can_move(direction):
            return False

        next_position = self.__get_next_position(direction)

        self.__next_position = next_position
        self.__direction = direction
        self.__hungry_by_move()
        self.__pre_direction = direction

        self.__mover.ready()

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
        value = self.__mover.get_next_plan()
        position = (
            self.y + float(y) * value,
            self.x + float(x) * value
        )
        self.set_position(position)
        if not self.__mover.have_plan():
            self.__moved()

    def __moved(self):
        self.set_position(self.__next_position)
        self.__next_position = None

    def battle(self, target_enemy: object):
        from model.event.enemy import Enemy
        enemy: Enemy = target_enemy
        damage = enemy.strength + random.randint(1, enemy.level + 5)
        self.__add_hp(-damage)
        self.__pre_damage = damage
        self.__damage_view_time = 10

    def __add_hp(self, value: int):
        self.__hp += value
        if self.__hp < 0:
            self.__hp = 0

        if self.__hp > self.__max_hp:
            self.__hp = self.__max_hp

    def __add_strength(self, value: int):
        self.__strength += value
        if self.__strength > self.__limit_strength:
            self.__strength = self.__limit_strength

    def __add_max_hp(self, value: int):
        self.__max_hp += value
        if self.__max_hp > self.__limit_hp:
            self.__max_hp = self.__limit_hp

    def back(self):
        y, x = self.__pre_direction
        self.add_position((y * -1, x * -1))

    def is_moving(self) -> bool:
        return self.__next_position is not None

    def is_level_up(self, target_enemy: object) -> bool:

        if self.__level >= self.__limit_level:
            return False

        from model.event.enemy import Enemy
        enemy: Enemy = target_enemy
        return random.randint(0, enemy.max_hp) \
            > random.randint(0, self.__max_hp)

    def set_direction(self, direction: int):
        self.__direction = direction

    def move(self):

        if self.__next_position is None:
            return

        self.__do_move()

    def __draw_damage(self, position: (int, int)):

        game_system = self.__game_system

        adjust = self.__damage_view_time
        x = position[0]
        y = position[1] + self.height - 16 + adjust

        text = Text(
            str(self.__pre_damage),
            (x, y),
            Color.YELLOW,
            font_size=Text.FontSize.NORMAL,
            is_absolute_position=False
        )
        game_system.add_draw_object(text)

    def draw(self):
        position = self.__game_info.convert_map_to_display(
            (self.x, self.y)
        )
        image = self.__get_animation_image()
        image.set_position(position)
        self.__game_system.add_draw_object(image)
        if self.__damage_view_time > 0:
            self.__damage_view_time -= 1
            self.__draw_damage(position)
