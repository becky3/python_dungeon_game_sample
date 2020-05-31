import math
import random

from libs.range_value import RangeValue


class Stats():

    @property
    def level(self) -> int:
        return self.__level.value

    @property
    def hp(self) -> int:
        return self.__hp.value

    @property
    def max_hp(self) -> int:
        return self.__max_hp.value

    @property
    def strength(self) -> int:
        return self.__strength.value

    @property
    def satiation(self) -> int:
        return self.__satiation.value

    @property
    def potion(self) -> int:
        return self.__potion.value

    @property
    def bom(self) -> int:
        return self.__bom.value

    @property
    def pre_damage(self) -> int:
        return self.__pre_damage

    def __init__(self,
                 level: int,
                 max_hp: int,
                 strength: int,
                 satiation: int = 0,
                 potion: int = 0,
                 bom: int = 0,
                 limit_hp: int = 999,
                 limit_level: int = 99,
                 limit_strength: int = 999,
                 limit_satiation: int = 300,
                 limit_potion: int = 99,
                 limit_bom: int = 99
                 ):
        self.__level = RangeValue(level, (0, limit_level))
        self.__hp = RangeValue(max_hp, (0, max_hp))
        self.__max_hp = RangeValue(max_hp, (0, limit_hp))
        self.__strength = RangeValue(strength, (0, limit_strength))
        self.__satiation = RangeValue(satiation, (0, limit_satiation))
        self.__potion = RangeValue(potion, (0, limit_potion))
        self.__bom = RangeValue(bom, (0, limit_bom))
        self.__pre_damage = 0

    def level_up(self):
        self.__level.add(1)
        hp = random.randint(10, 20 + math.floor(self.__level.value / 2))
        strength = random.randint(5, 10 + math.floor(self.__level.value / 2))
        self.add_max_hp(hp)
        self.__strength.add(strength)

    def hungry(self):
        if self.__satiation.value <= 0:
            self.__hp.add(-5)
            return
        self.__satiation.add(-1)
        self.__hp.add(1 + math.floor(self.__level.value / 10))

    def damage(self, value: int):
        self.add_hp(-value)
        self.__pre_damage = value

    def add_hp(self, value: int):
        self.__hp.add(value)

    def add_max_hp(self, value: int, is_add_hp: bool = True):
        self.__max_hp.add(value)
        self.__hp.change_max(self.__max_hp.value)
        if is_add_hp:
            self.__hp.add(value)

    def add_potion(self, value: int):
        self.__potion.add(value)

    def add_bom(self, value: int):
        self.__bom.add(value)

    def add_satiation(self, value: int):
        self.__satiation.add(value)

    def set_satiation(self, value: int):
        self.__satiation.set_value(value)

    def is_die(self) -> bool:
        return self.__hp.is_min()

    def is_max_level(self) -> bool:
        return self.__level.is_max()
