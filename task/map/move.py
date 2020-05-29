from typing import Optional

from manager.map_manager import MapManager
from task.task import Task


class Move(Task):

    def __init__(self, map_manager: MapManager):
        self.__map_manager = map_manager
        self.__next_task = None

    def start(self):
        pass

    def update(self):

        mm = self.__map_manager
        event_manager = mm.event_manager
        player = mm.player

        player.move()

        if player.is_moving():
            return

        if player.is_die():
            from task.map.game_over import GameOver
            self.__next_task = GameOver(self.__map_manager)
            return

        enemy = event_manager.get_enemy(player.map_coordinate)
        if enemy is not None:
            from task.map.battle import Battle
            self.__next_task = Battle(mm, enemy)
            return

        event_manager.enemy_update()

        if event_manager.is_floor_clear():
            from task.map.change_floor import ChangeFloor
            self.__next_task = ChangeFloor(self.__map_manager)
            return

        treasure_box = event_manager.get_treasure_box(player.map_coordinate)
        if treasure_box is not None:
            from task.map.get_item import GetItem
            self.__next_task = GetItem(mm, treasure_box.get_item())
            mm.event_manager.remove_treasure(
                treasure_box
            )
            return

        from task.map.input_wait import InputWait
        self.__next_task = InputWait(self.__map_manager)

    def draw(self):
        mm = self.__map_manager
        mm.draw_map()
        mm.draw_parameter()
        mm.draw_floor_info()

    def exit(self):
        pass

    def get_next_task(self) -> Optional[Task]:
        return self.__next_task
