import math
import random
from typing import Dict, Tuple, List
from FindPath import shortest_path_with_obstacles, check_destination_point


class User:
    _coordinates = {}  # Словарь с ключами = номеру юнита, значениями = объект юнита (Глобальный словрь, показывающий живых на карте)
    __counter: int = 0
    __resources = [100, 100]

    def __init__(self, _type="", name="", hp=0, defense_points=0, attack_points=0, attack_range=0, move_range=0,
                 price=0):
        self._type = _type
        self._name: str = name
        self._hp: int = hp
        self._defense_points: int = defense_points
        self._attack_points: int = attack_points
        self._attack_range: int = attack_range
        self._move_range: int = move_range
        self._price: int = price
        self._current_coordinates: Tuple[int, ...] = (0, User.__counter)
        self._number: str = str(User.__counter + 1)
        self.my_dict = {}  # Словарь для юнитов, которых может атаковать текущий юнит (ключ - номер юнита, значение - объект юнита)
        self.flag = False  # Флаг, показывающий, атаковал ли данный юнит боса
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
    def fill_coordinates(cls, name: str, params=None) -> None:
        if name == "мечник":
            User("Пеший", "Мечник", 50, 8, 5, 1, 3, 10)
        elif name == "копьеносец":
            User("Пеший", "Копьеносец", 35, 4, 3, 1, 6, 15)
        elif name == "топорщик":
            User("Пеший", "Топорщик", 45, 3, 9, 1, 4, 20)
        elif name == "лучник с длинным луком":
            User("Лучник", "Лучник с длинным луком", 30, 8, 6, 5, 2, 15)
        elif name == "лучник с коротким луком":
            User("Лучник", "Лучник с коротким луком", 25, 4, 3, 3, 4, 19)
        elif name == "арбалетчик":
            User("Лучник", "Лучник с коротким луком", 25, 4, 3, 3, 4, 19)
        elif name == "рыцарь":
            User("Всадник", "Рыцарь", 30, 3, 5, 1, 6, 20)
        elif name == "кирасир":
            User("Всадник", "Кирасир", 50, 7, 2, 1, 5, 23)
        elif name == "конный лучник":
            User("Всадник", "Конный лучник", 25, 2, 3, 3, 5, 25)
        elif name == "мега лучник":
            User("Лучник", "Мега лучник", 500, 1000, 1000, 500, 500, 10000)
        elif params is not None:
            User(*params)

    @classmethod
    def clear(cls):
        cls._coordinates.clear()
        cls.__counter = 0

    def change_hp(self, other):
        self._defense_points -= other.attack_points
        if self._defense_points < 0:
            self._hp += self._defense_points
            self._defense_points = 0

    @classmethod
    def get_resources(cls):
        return cls.__resources

    @classmethod
    def set_resources(cls, value):
        cls.__resources = value

    def __str__(self):  # вывод характеристик юнита
        if self.is_alive():
            return (
                f"тип = {self._name}, номер на карте = {self._number}, здоровье = {self._hp}, защита = {self._defense_points}, "
                f"атака = {self._attack_points}, "
                f"дальность атаки = {self._attack_range}, перемещение = {self._move_range}, стоимость = {self._price}, "
                f"текущие координаты = {self._current_coordinates}\n")
        else:
            return f"{self._name} {self._number} мертв\n"

    def is_alive(self):
        return self._hp > 0

    def change_attack_points(self):
        for unit in User._coordinates.values():
            if unit.flag:
                unit._attack_points += 1

    def create_master_of_weapon(self):
        print(f"{self._name} {self._number} убил босса и стал Мастером оружия, его характеристики:")
        self._type = "Крутой"
        self._name = "Мастер оружия"
        self._hp = 50
        self._defense_points = 8
        self._attack_points = 8
        self._attack_range = 6
        self._move_range = 6
        self.change_attack_points()
        print(self)

    def can_attack(self,
                   bot_dic):  # метод, проверяющий, кого может атаковать текущий юнит, возвращается словарь, ключ- номер юнита, значение - объект юнита
        for number, unit in bot_dic.items():
            if math.sqrt((self._current_coordinates[0] - unit.current_coordinates[0]) ** 2 + (
                    self._current_coordinates[1] - unit.current_coordinates[1]) ** 2) <= self._attack_range:
                self.my_dict[str(unit.number)] = unit
        return self.my_dict

    def attack(self, battlefield, bot_dic) -> None:  # метод, проводящий атаку
        global num
        if not self.can_attack(bot_dic):
            print("Вы никого не можете атаковать")
        else:
            print("Вы можете атаковать юнитов под номерами:", *self.my_dict.keys())
            num = input("Выберете юнита, которого хотите атаковать: ")
            while num not in self.my_dict.keys():
                num = input("Этого юнита нет в списке, выберете другого: ")
            unit = self.my_dict[num]
            unit.change_hp(self)
            if num.isupper():  # Если номер юнита - заглавная буква (босс), то флаг = true
                self.flag = True
            if not unit.is_alive():
                unit.update_map_after_attack(battlefield)
                del self.my_dict[num]
                if num.isupper():  # Если убитый юнит - заглавная буква(босс), то объект класса, который убил босса, становится мастером оружия
                    self.create_master_of_weapon()
                    print(battlefield)
                    return True
                    # User.__resources = list(map(lambda x: x + random.randint(5, 10), User.__resources))
                    # print(f"Ваши ресурсы: дерево - {User.__resources[0]}, камень - {User.__resources[1]}\n")
                else:  # Иначе просто выводим сообщение о том, что какого-то юнита убили
                    User.__resources = list(map(lambda x: x + random.randint(1, 5), User.__resources))
                    print(unit)
                    print(f"Ваши ресурсы: дерево - {User.__resources[0]}, камень - {User.__resources[1]}\n")
                    print(battlefield)
                    return True
            else:
                print(f"Вы атаковали юнита под номером {num}, его характеристики: {unit}\n")
                print(battlefield)
                return False

    def update_map_after_attack(self, battle_field) -> None:
        row = self._current_coordinates[0]
        col = self._current_coordinates[1]
        battle_field.field[row][col] = "*"
        del User._coordinates[self._number]

    def update_map_after_move(self, battle_field, destination: Tuple[int, ...]) -> None:
        battle_field.field[self._current_coordinates[0]][self._current_coordinates[1]] = "*"
        battle_field.field[destination[0]][destination[1]] = self._number
        self._current_coordinates = (destination[0], destination[1])
        self.my_dict = {}
        User._coordinates[self._number] = self

    def move(self, battle_field) -> None:
        destination = tuple(map(int, input("Введите координаты точки назначения:").split()))
        shortest_path = shortest_path_with_obstacles(battle_field.field, self._current_coordinates, destination,
                                                     self._type)
        while True:
            if check_destination_point(battle_field.field, destination):
                if self._move_range >= shortest_path != -1.0:
                    self.update_map_after_move(battle_field, destination)
                    print(f"Вы успешно переместились в точку {destination[0], destination[1]}\n")
                    print(battle_field)
                    return shortest_path
                    break
                else:
                    print(f"Вам не хватает очков перемещения для достижения данной клетки\n")
                    destination = tuple(map(int, input("Введите другие координаты точки назначения:").split()))
                    shortest_path = shortest_path_with_obstacles(battle_field.field, self._current_coordinates,
                                                                 destination, self._type)
            else:
                destination = tuple(map(int, input("Введите другие координаты точки назначения:").split()))
                shortest_path = shortest_path_with_obstacles(battle_field.field, self._current_coordinates, destination,
                                                             self._type)

    @classmethod
    def show_all_units(cls):
        for unit in cls._coordinates.values():
            print(unit)
