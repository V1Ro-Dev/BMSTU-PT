from User import User
from typing import Dict, Tuple
from Find_Path import check_destination_point


class Bot(User):
    _bot_coordinates: Dict[str, object] = {}
    __char_counter: int = 96
    __counter: int = 14

    def __init__(self, name="", hp=0, defense_points=0, attack_points=0, attack_range=0, move_range=0, price=0):
        self._name: str = name
        self._hp: int = hp
        self._defense_points: int = defense_points
        self._attack_points: int = attack_points
        self._attack_range: int = attack_range
        self._move_range: int = move_range
        self._price: int = price
        self._current_coordinates: Tuple[int, ...] = (14, Bot.__counter)
        self._number: str = chr(Bot.__char_counter + 1)
        self.my_dict: Dict[str, object] = {}  # Словарь для юнитов, которых может атаковать текущий юнит (ключ - номер юнита, значение - объект юнита)
        Bot._bot_coordinates[self._number] = self
        Bot.__char_counter += 1
        Bot.__counter -= 1

    @classmethod
    def fill_coordinates(cls, name):
        if name == "мечник":
            Bot("Мечник", 50, 8, 5, 1, 3, 10)
        elif name == "копьеносец":
            Bot("Копьеносец", 35, 4, 3, 1, 6, 15)
        elif name == "топорщик":
            Bot("Топорщик", 45, 3, 9, 1, 4, 20)
        elif name == "лучник с длинным луком":
            Bot("Лучник с длинным луком", 30, 8, 6, 5, 2, 15)
        elif name == "лучник с коротким луком":
            Bot("Лучник с коротким луком", 25, 4, 3, 3, 4, 19)
        elif name == "арбалетчик":
            Bot("Лучник с коротким луком", 25, 4, 3, 3, 4, 19)
        elif name == "рыцарь":
            Bot("Рыцарь", 30, 3, 5, 1, 6, 20)
        elif name == "кирасир":
            Bot("Кирасир", 50, 7, 2, 1, 5, 23)
        elif name == "конный лучник":
            Bot("Конный лучник", 25, 2, 3, 3, 5, 25)

    @classmethod
    def show_coordinates(cls):
        return cls._bot_coordinates

    def attack(self, battlefield, unit_dic):  # метод, проводящий атаку
        if self.can_attack(unit_dic):
            num = list(self.my_dict.keys())[0]
            print(f"Юнит под номером {self._number} атакует юнита под номером {num}")
            unit = self.my_dict[num]
            unit.change_hp(self)
            if not unit.is_alive():
                unit.update_map_after_attack(battlefield)
                del self.my_dict[num]
                print(f"Юнит под номером {num}, был атакован, его характеристики: {unit}")
                print(battlefield)
            else:
                print(f"Юнит под номером {num}, был атакован, его характеристики: {unit}")
                print(battlefield)
        else:
            self.move(battlefield)

    def move(self, battle_field):
        row = self._current_coordinates[0] - 1
        col = self._current_coordinates[1]
        destination = (row, col)
        if check_destination_point(battle_field.field, destination, "Bot"):
            self.update_map_after_move(battle_field, destination)
            print(battle_field)
        else:
            print(f"Юнит под номером {self._number} не может передвинуться")

    def update_map_after_attack(self, battle_field):
        row = self._current_coordinates[0]
        col = self._current_coordinates[1]
        battle_field.field[row][col] = "*"
        del Bot._bot_coordinates[self._number]

    def update_map_after_move(self, battle_field, destination):
        battle_field.field[self._current_coordinates[0]][self._current_coordinates[1]] = "*"
        battle_field.field[destination[0]][destination[1]] = self._number
        self._current_coordinates = (destination[0], destination[1])
        self.my_dict = {}
        Bot._bot_coordinates[self._number] = self