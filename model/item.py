class Item():

    class Type:
        POTION = 0
        BLAZE_GEM = 1
        FOOD_SPOILED = 2
        FOOD_ADD_20 = 3
        FOOD_ADD_100 = 4

    __IMAGE_FILE_PATHS = [
        "resource/image/potion.png",
        "resource/image/blaze_gem.png",
        "resource/image/spoiled.png",
        "resource/image/apple.png",
        "resource/image/meat.png",
    ]

    __NAMES = [
        "Potion",
        "Blaze gem",
        "Food spoiled.",
        "Food +20",
        "Food +100",
    ]

    @property
    def item_type(self) -> int:
        return self.__item_type

    @property
    def name(self) -> str:
        return self.__NAMES[self.__item_type]

    @property
    def image_file_path(self) -> str:
        return self.__IMAGE_FILE_PATHS[self.__item_type]

    def __init__(self, item_type: int):
        self.__item_type = item_type
