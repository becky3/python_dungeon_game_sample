import random

from const import Direction, Color
from game.game_info import GameInfo
from game.game_system import GameSystem
from model.item import Item
from model.mover import Mover
from model.dungeon import Dungeon, FloorType
from model.draw_object.text import Text
from model.draw_object.image import Image
from model.character_chip import CharacterChip
from model.event.event import Event
from manager.debug_manager import DebugManager
from model.stats import Stats


class Player(Event):

    class CharacterType:
        NORMAL = 0
        DIE = 1

    __IMAGE = "resource/image/player.png"

    @property
    def stats(self) -> Stats:
        return self.__stats

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
        self.__damage_view_time = 0
        self.__stats = self.__get_default_stats()

    def __get_default_stats(self) -> Stats:
        return Stats(
            level=1,
            max_hp=300,
            strength=100,
            satiation=300,
            potion=0,
            bom=0
        )

    def reset_stats(self):
        self.__stats = self.__get_default_stats()

        if DebugManager.is_debug:
            for _ in range(1, DebugManager.level):
                self.stats.level_up()
            self.stats.add_potion(DebugManager.potion)
            self.stats.add_bom(DebugManager.bom)

    def add_item(self, item: Item):
        item_type = item.item_type
        if item_type == Item.Type.POTION:
            self.stats.add_potion(1)
            return
        if item_type == Item.Type.BOM:
            self.stats.add_bom(1)
            return
        if item_type == Item.Type.SA_SPOILED:
            self.stats.set_satiation(
                int(self.stats.satiation / 2)
            )
            return
        if item_type == Item.Type.SA_ADD_20:
            self.__stats.add_satiation(20)
            return
        if item_type == Item.Type.SA_ADD_100:
            self.__stats.add_satiation(100)
            return

    def setup_start_position(self):

        floor_map = self.__dungeon.floor_map
        height, width = floor_map.shape

        while True:
            y = random.randint(3, height - 4)
            x = random.randint(3, width - 4)
            self.set_position((y, x))
            if floor_map[y, x] == FloorType.FLOOR:
                break
        self.__direction = Direction.DOWN

    def set_character_type(self, _type: int):
        self.__character_chip.set_character_no(_type)

    def use_item(self, item: Item):
        if item.item_type == Item.Type.POTION:
            self.__stats.add_hp(500)
            self.__stats.add_potion(-1)
        if item.item_type == Item.Type.BOM:
            self.__stats.add_bom(-1)

    def __can_move(self, direction: (int, int)) -> bool:
        if direction == Direction.NEWTRAL:
            return False

        next_position = self.__get_next_position(direction)

        floor_map = self.__dungeon.floor_map

        if not floor_map.is_in(next_position):
            return False

        if floor_map[next_position] == FloorType.WALL:
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
        self.__stats.hungry()
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
        damage = enemy.stats.strength \
            + random.randint(1, enemy.stats.level + 5)
        self.__stats.damage(damage)
        self.__damage_view_time = 10

    def back(self):
        y, x = self.__pre_direction
        self.add_position((y * -1, x * -1))

    def is_moving(self) -> bool:
        return self.__next_position is not None

    def is_level_up(self, target_enemy: object) -> bool:

        if self.stats.is_max_level():
            return False

        from model.event.enemy import Enemy
        enemy: Enemy = target_enemy
        return random.randint(0, enemy.stats.max_hp) \
            > random.randint(0, self.stats.max_hp)

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
            str(self.stats.pre_damage),
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
