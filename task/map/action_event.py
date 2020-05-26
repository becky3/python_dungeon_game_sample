from typing import Optional

from model.event.enemy import Enemy
from manager.map_manager import MapManager
from manager.sound_manager import SE
from task.task import Task


class ActionEvent(Task):

    def __init__(self, map_manager: MapManager):
        self.__map_manager = map_manager
        self.__next_task = None

    def start(self):
        pass

    def update(self):

        mm = self.__map_manager
        event_manager = mm.event_manager
        player = mm.player
        game_system = mm.game_system

        event = event_manager.current_event
        if event is None:
            from task.map.input_wait import InputWait
            self.__next_task = InputWait(self.__map_manager)
            return

        if isinstance(event, Enemy):
            event.damage()
            game_system.play_se(SE.ATTACK)

            if event.is_die():
                event_manager.remove_event(event)
            else:
                player.back()
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
