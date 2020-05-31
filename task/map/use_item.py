from typing import Optional

from manager.map_manager import MapManager
from task.task import Task
from manager.sound_manager import SE
from model.item import Item
from model.draw_object.image import Image
from model.event.enemy import Enemy
from model.event.treasure_box import TreasureBox
from model.dungeon import FloorType


class UseItem(Task):

    def __init__(self, map_manager: MapManager, item: Item):
        self.__map_manager = map_manager
        self.__next_task: Task = None
        self.__item = item
        self.__get_item = None
        self.__is_level_up = False

    def start(self):
        mm = self.__map_manager
        item = self.__item
        se: str

        if item.item_type == Item.Type.POTION:
            se = SE.POTION
        elif item.item_type == Item.Type.BOM:
            se = SE.BOM

        mm.player.use_item(item)
        mm.game_system.play_se(se)

    def update(self):

        item_type = self.__item.item_type
        if item_type == Item.Type.POTION:
            self.__potion_update()
        elif item_type == Item.Type.BOM:
            self.__bom_update()

    def __potion_update(self):
        if self.__map_manager.game_system.timer < 8:
            return

        from task.map.wait_input import WaitInput
        self.__next_task = WaitInput(self.__map_manager)

    def __bom_update(self):
        mm = self.__map_manager
        if mm.game_system.timer < 8:
            return

        self.__attack_bom_at_area()

        if self.__get_item is not None:
            from task.map.get_item import GetItem
            self.__next_task = GetItem(mm, self.__get_item)
            return

        if self.__is_level_up:
            from task.map.level_up import LevelUp
            self.__next_task = LevelUp(mm)
            return

        from task.map.wait_input import WaitInput
        self.__next_task = WaitInput(self.__map_manager)

    def draw(self):

        mm = self.__map_manager
        mm.draw_map()
        mm.draw_parameter()

        item_type = self.__item.item_type
        if item_type == Item.Type.POTION:
            self.__potion_draw()
        elif item_type == Item.Type.BOM:
            self.__bom_draw()

    def __potion_draw(self):
        pass

    def __bom_draw(self):

        mm = self.__map_manager
        game_system = mm.game_system
        timer = game_system.timer
        player_y, player_x = mm.player.map_coordinate
        player_position = mm.game_info.convert_map_to_display(
            (player_x, player_y)
        )
        angle = timer * 90
        scale = timer * 0.25
        x = player_position[0] + 8 - (scale * 16)
        y = player_position[1] + 8 - (scale * 16)

        bom_image = Image(
            "resource/image/bom.png",
            (x, y),
            transform=(angle, scale)
        )
        game_system.add_draw_object(bom_image)

    def exit(self):
        pass

    def __attack_bom_at_area(self):

        player_y, player_x = self.__map_manager.player.map_coordinate

        for y in range(-1, 2):
            for x in range(-1, 2):
                self.__attack_bom_at_position((
                    y + player_y,
                    x + player_x
                ))

    def __attack_bom_at_position(self, position: (int, int)):

        event_manager = self.__map_manager.event_manager
        floor_map = self.__map_manager.dungeon.floor_map
        enemy_map = event_manager.enemy_map
        treasure_map = event_manager.treasure_map
        player = self.__map_manager.player

        if not floor_map.is_in(position):
            return

        enemy: Enemy = enemy_map[position]
        if enemy is not None:
            enemy.stats.damage(1000)

            if enemy.stats.is_die():
                event_manager.remove_enemy(enemy)
                item = enemy.get_item()

                if item is not None:
                    self.__get_item = item

                if player.is_level_up(enemy):
                    self.__is_level_up = True

        treasure_box: TreasureBox = treasure_map[position]
        if treasure_box is not None:
            event_manager.remove_treasure(treasure_box)

        floor_map[position] = FloorType.FLOOR

    def get_next_task(self) -> Optional[Task]:
        return self.__next_task
