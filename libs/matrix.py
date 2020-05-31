import numpy as np


class Matrix:

    @property
    def rows(self) -> int:
        return self.__data.shape[0]

    @property
    def columns(self) -> int:
        return self.__data.shape[1]

    @property
    def shape(self) -> (int, int):
        return self.__data.shape

    def __getitem__(self, position: (int, int)) -> any:
        y, x = position
        return self.__data[y, x]

    def __setitem__(self, position: (int, int), value: any):
        y, x = position
        self.__data[y, x] = value

    def __init__(self, rows=0, columns=0, dtype="int8"):
        self.__data: np.array
        if dtype == "object":
            self.__data = np.empty((rows, columns), dtype=dtype)
        else:
            self.__data = np.zeros((rows, columns), dtype=dtype)

    def is_in(self, position: (int, int)) -> bool:
        y, x = position
        return 0 <= x < self.columns and 0 <= y < self.rows

    def get_not_empty_values(self) -> []:
        if self.__data.dtype == "object":
            # is None だと where の期待通りではないので、 Flake8 の警告を無効化
            return self.__data[np.where(self.__data != None)].tolist()   # noqa: E771, E501

        return self.__data[np.where(self.__data != 0)].tolist()
