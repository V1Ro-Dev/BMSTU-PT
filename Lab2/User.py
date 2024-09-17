import math
from typing import Dict, Tuple
from Find_Path import shortest_path_with_obstacles, check_destination_point
from No_Inheritance import Bot_Unit


class User:
    """ Base unit class"""
    _coordinates: Dict[str, object] = {}  # Словарь с ключами = номеру юнита, значениями = объект юнита (Глобальный словрь, показывающий живых на карте)
    __counter: int = 0

    def __init__(self, name="", hp=0, defense_points=0, attack_points=0, attack_range=0, move_range=0, price=0):
        self._name: str = name
        self._hp: int = hp
        self._defense_points: int = defense_points
        self._attack_points: int = attack_points
        self._attack_range: int = attack_range
        self._move_range: int = move_range
        self._price: int = price
        self._current_coordinates: Tuple[int, ...] = (0, User.__counter)
        self._number: str = str(User.__counter + 1)
        self.my_dict: Dict[str, object] = {}  # Словарь для юнитов, которых может атаковать текущий юнит (ключ - номер юнита, значение - объект юнита)
        User._coordinates[self._number] = self
        User.__counter += 1

    @property
    def name(self):
        return self._name

    @property
    def hp(self):
        return self._hp

    @property
    def defense_points(self):
        return self._defense_points

    @property
    def attack_points(self):
        return self._attack_points

    @property
    def attack_range(self):
        return self._attack_range

    @property
    def move_range(self):
        return self._move_range

    @property
    def price(self):
        return self._price

    @property
    def current_coordinates(self):
        return self._current_coordinates

    @property
    def number(self):
        return self._number

    @classmethod
    def show_coordinates(cls):
        return cls._coordinates

    @classmethod
    def fill_coordinates(cls, name):
        if name == "мечник":
            User("Мечник", 50, 8, 5, 1, 3, 10)
        elif name == "копьеносец":
            User("Копьеносец", 35, 4, 3, 1, 6, 15)
        elif name == "топорщик":
            User("Топорщик", 45, 3, 9, 1, 4, 20)
        elif name == "лучник с длинным луком":
            User("Лучник с длинным луком", 30, 8, 6, 5, 2, 15)
        elif name == "лучник с коротким луком":
            User("Лучник с коротким луком", 25, 4, 3, 3, 4, 19)
        elif name == "арбалетчик":
            User("Лучник с коротким луком", 25, 4, 3, 3, 4, 19)
        elif name == "рыцарь":
            User("Рыцарь", 30, 3, 5, 1, 6, 20)
        elif name == "кирасир":
            User("Кирасир", 50, 7, 2, 1, 5, 23)
        elif name == "конный лучник":
            User("Конный лучник", 25, 2, 3, 3, 5, 25)
        elif name == "мега лучник":
            User("Мега лучник", 500, 1000, 1000, 500, 500, 10000)

    @classmethod
    def clear(cls):
        cls._coordinates.clear()
        cls.__counter = 0

    def change_hp(self, other):
        self._defense_points -= other.attack_points
        if self._defense_points < 0:
            self._hp += self._defense_points
            self._defense_points = 0

    def __str__(self):  # вывод характеристик юнита
        if self.is_alive():
            return (
                f"тип = {self._name}, номер на карте = {self._number}, здоровье = {self._hp}, защита = {self._defense_points}, "
                f"атака = {self._attack_points}, "
                f"дальность атаки = {self._attack_range}, перемещение = {self._move_range}, стоимость = {self._price}, "
                f"текущие координаты = {self._current_coordinates}")
        else:
            return f"{self._name} {self._number} мертв"

    def is_alive(self):
        return self._hp > 0

    def can_attack(self, bot_dic):  # метод, проверяющий, кого может атаковать текущий юнит, возвращается словарь, ключ- номер юнита, значение - объект юнита
        for number, unit in bot_dic.items():
            if math.sqrt((self._current_coordinates[0] - unit.current_coordinates[0]) ** 2 + (self._current_coordinates[1] - unit.current_coordinates[1]) ** 2) <= self._attack_range:                                  # and self.__number != unit.__number and unit.__number.isdigit() == False:
                self.my_dict[str(unit.number)] = unit
        return self.my_dict

    def attack(self, battlefield, bot_dic):  # метод, проводящий атаку
        global num
        if not self.can_attack(bot_dic):
            print("Вы никого не можете атаковать")
        else:
            print("Вы можете атаковать юнитов под номерами:", *self.my_dict.keys())
            num = input("Выберете юнита, которого хотите атаковать:")
            while num not in self.my_dict.keys():
                num = input("Этого юнита нет в списке, выберете другого:")
            unit = self.my_dict[num]
            unit.change_hp(self)
            if not unit.is_alive():
                unit.update_map_after_attack(battlefield)
                del self.my_dict[num]
                print(f"Вы атаковали юнита под номером {num}, его характеристики: {unit}")
                print(battlefield)
            else:
                print(f"Вы атаковали юнита под номером {num}, его характеристики: {unit}")
                print(battlefield)

    def update_map_after_attack(self, battle_field):
        row = self._current_coordinates[0]
        col = self._current_coordinates[1]
        battle_field.field[row][col] = "*"
        del User._coordinates[self._number]

    def update_map_after_move(self, battle_field, destination):
        battle_field.field[self._current_coordinates[0]][self._current_coordinates[1]] = "*"
        battle_field.field[destination[0]][destination[1]] = self._number
        self._current_coordinates = (destination[0], destination[1])
        self.my_dict = {}
        User._coordinates[self._number] = self

    def move(self, battle_field):
        destination = tuple(map(int, input("Введите координаты точки назначения:").split()))
        shortest_path = shortest_path_with_obstacles(battle_field.field, self._current_coordinates, destination, self._name)
        while True:
            if check_destination_point(battle_field.field, destination):
                if self._move_range >= shortest_path != -1.0:
                    self.update_map_after_move(battle_field, destination)
                    print(f"Вы успешно переместились в точку {destination[0], destination[1]}")
                    print(battle_field)
                    break
                else:
                    print(f"Вам не хватает очков перемещения для достижения данной клетки")
                    destination = tuple(map(int, input("Введите другие координаты точки назначения:").split()))
                    shortest_path = shortest_path_with_obstacles(battle_field.field, self._current_coordinates, destination, self._name)
            else:
                destination = tuple(map(int, input("Введите другие координаты точки назначения:").split()))
                shortest_path = shortest_path_with_obstacles(battle_field.field, self._current_coordinates, destination, self.name)