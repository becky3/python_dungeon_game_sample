class RangeValue():

    @property
    def value(self) -> int:
        return self.__value

    def __init__(self,
                 value: int,
                 value_range: (int, int)
                 ):
        self.__value = value
        self.__min_value, self.__max_value = value_range
        self.__correction_value

    def __correction_value(self):
        if self.__value < self.__min_value:
            self.__value = self.__min_value
        elif self.__value > self.__max_value:
            self.__value = self.__max_value

    def is_max(self) -> bool:
        return self.__value == self.__max_value

    def is_min(self) -> bool:
        return self.__value == self.__min_value

    def add(self, value: int):
        self.__value += value
        self.__correction_value()

    def set_value(self, value: int):
        self.__value = value
        self.__correction_value()

    def change_max(self, value: int):
        self.__max_value = value
        self.__correction_value()

    def change_min(self, value: int):
        self.__min_value = value
        self.__correction_value()
