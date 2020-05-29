class Mover():

    def __init__(self, walk_frame: int = 2):
        self.__walk_frame = walk_frame
        self.__walk_plan = []

    def ready(self):
        one_value = 1.0 / float(self.__walk_frame)
        self.__walk_plan = [one_value] * self.__walk_frame

    def get_next_plan(self) -> float:
        return self.__walk_plan.pop()

    def have_plan(self) -> float:
        return len(self.__walk_plan) > 0
