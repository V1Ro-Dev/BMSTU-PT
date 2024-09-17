import json
import pickle
import os
from User import User
from Bot import Bot
from tabulate import tabulate
from WelcomeText import text
from Town import Hospital, Forge, Barrack, Market, Academy, BuilderHut, Tavern, Building, \
    get_list_of_affordable_buildings, get_list_of_upgradeable_buildings, MilitaryAcademy
import random


class Menu:

    def __init__(self):
        print(text, "\n")
        self.__buildings = self.load_progress()
        self.__balance = 10 #int(input("Введите баланс: "))
        self.__bot_balance = 10
        self.__resources = self.__buildings["Ресурсы"]
        self.units = [User("Пеший", "Мечник", 50, 8, 5, 1, 3, 10),
                      User("Пеший", "Копьеносец", 35, 4, 3, 1, 6, 15),
                      User("Пеший", "Топорщик", 45, 3, 9, 1, 4, 20),
                      User("Лучник", "Лучник с длинным луком", 30, 8, 6, 5, 2, 15),
                      User("Лучник", "Лучник с коротким луком", 25, 4, 3, 3, 4, 19),
                      User("Лучник", "Арбалетчик", 40, 3, 7, 6, 2, 23),
                      User("Всадник", "Рыцарь", 30, 3, 5, 1, 6, 20),
                      User("Всадник", "Кирасир", 50, 7, 2, 1, 5, 23),
                      User("Всадник", "Конный лучник", 25, 2, 3, 3, 5, 25)]
        self.buffed_nums = []
        User.clear()

    def add_new_units(self):
        academy = self.__buildings["Академия"]
        for researched_unit in academy.pending_units:
            self.units.append(User(*researched_unit))
        User.clear()

    def show_description_of_units(self):
        self.add_new_units()
        print(
            f"На город готовится нападение. В городской казне есть сумма:{self.__balance} для покупки наемников, "
            f"защищающих город. Характеристики воинов:\n")
        table_data = []
        for unit in self.units:
            table_data.append(
                [unit.name, unit.hp, unit.defense_points, unit.attack_points, unit.attack_range, unit.move_range,
                 unit.price])

        headers = ["Name", "HP", "Defense Points", "Attack Points", "Attack Range", "Move Range", "Price"]
        print(tabulate(table_data, headers=headers, tablefmt="grid"))

    def check_unit(self, name: str) -> bool:
        for unit in self.units:
            if unit.name.lower() == name:
                return True
        return False

    def check_price(self, name: str) -> int:
        for unit in self.units:
            if unit.name.lower() == name:
                return unit.price
        return -1

    def buy_units(self):
        while self.__balance >= 10:
            unit_type = input("Выберете юнита, которого хотите купить. Необходимо ввести полное название: ")
            if self.check_unit(unit_type):
                if self.__balance >= self.check_price(unit_type):
                    self.__balance -= self.check_price(unit_type)
                    self.spawn_new_units(unit_type)
                    print(f"Вы успешно купили {unit_type}, ваш текущий баланс:{self.__balance}")
                else:
                    print(f"Недостаточно денег для покупки {unit_type}, введите другого юнита")
            else:
                print("Такого юнита не существует, введите корректное название")
        self.show_units()

    def spawn_new_units(self, unit_type):
        if not self.is_from_academy(unit_type):
            User.fill_coordinates(unit_type)

    def is_from_academy(self, unit_type):
        academy = self.__buildings["Академия"]
        for i in range(len(academy.pending_units)):
            if unit_type == academy.pending_units[i][1].lower():
                User.fill_coordinates(academy.pending_units[i][1], params=academy.pending_units[i])
                return True
        return False

    @staticmethod
    def buy_boss(unit_type):
        if unit_type in ["мечник", "копьеносец", "топорщик"]:
            Bot(f"Босс {unit_type}", 50, 8, 9, 1, 6, 10, "boss")
        elif unit_type in ["лучник с длинным луком", "лучник с коротким луком", "арбалетчик"]:
            Bot(f"Босс {unit_type}", 40, 8, 7, 6, 4, 15, "boss")
        else:
            Bot(f"Босс {unit_type}", 50, 7, 5, 3, 6, 20, "boss")

    def buy_units_for_bot(self):
        lst_of_units = ["мечник", "копьеносец", "топорщик", "лучник с длинным луком", "лучник с коротким луком",
                        "арбалетчик", "рыцарь", "кирасир", "конный лучник"]
        boss_bought = False
        while self.__bot_balance >= 10:
            unit_type = random.choice(lst_of_units)
            if self.__bot_balance >= self.check_price(unit_type):
                if not boss_bought:
                    self.buy_boss(unit_type)
                    self.__bot_balance -= self.check_price(unit_type)
                    boss_bought = True
                else:
                    self.__bot_balance -= self.check_price(unit_type)
                    Bot.fill_coordinates(unit_type)
        self.show_bot_units()

    def buy_mega_unit(self):
        print("Выберете юнита, которого хотите купить. Необходимо ввести полное название")
        unit_type = "мега лучник"
        User.fill_coordinates(unit_type)
        self.show_units()

    def buy_mega_unit_for_bot(self):
        print("Выберете юнита, которого хотите купить. Необходимо ввести полное название")
        unit_type = "мега лучник"
        Bot.fill_coordinates(unit_type)
        self.show_units()

    def buy_all_units(self):
        User.fill_coordinates("мечник")
        User.fill_coordinates("копьеносец")
        User.fill_coordinates("топорщик")
        User.fill_coordinates("топорщик")
        User.fill_coordinates("лучник с длинным луком")
        User.fill_coordinates("лучник с коротким луком")
        User.fill_coordinates("арбалетчик")
        User.fill_coordinates("лучник с длинным луком")
        User.fill_coordinates("лучник с коротким луком")
        User.fill_coordinates("арбалетчик")
        User.fill_coordinates("рыцарь")
        User.fill_coordinates("кирасир")
        User.fill_coordinates("конный лучник")
        User.fill_coordinates("рыцарь")
        self.show_units()

    def can_create_formation(self, type_of_units):
        counter_1 = 0
        counter_2 = 0
        counter_3 = 0
        for unit in User.show_coordinates().values():
            if unit._type == "Пеший":
                counter_1 += 1
            elif unit._type == "Лучник":
                counter_2 += 1
            else:
                counter_3 += 1
        if type_of_units == "пешие":
            return counter_1 >= 4
        elif type_of_units == "лучники":
            return counter_2 >= 6
        else:
            return counter_3 >= 4

    def buff(self):
        for number, unit in User.show_coordinates().items():
            if number in self.buffed_nums:
                print(unit)
                unit._hp += 2
                unit._attack_points += 2
                print(unit)
        print("Все юниты получили бафф")

    def debuff(self):
        for number, unit in User.show_coordinates().items():
            if number in self.buffed_nums:
                print(unit)
                unit._hp -= 2
                unit._attack_points -= 2
                print(unit)

    def create_formation(self, map):
        answer = input("Хотите построить своих юнитов? (Yes/No): ").lower()
        if answer == "yes":
            type_of_units = input("Какой тип юнитов вы хотите построить? (Пешие/Лучники/Всадники: ").lower()
            if self.can_create_formation(type_of_units):
                self.buffed_nums = map.update_map_after_formation(User.show_coordinates(), type_of_units)
                self.buff()
            else:
                print(f"Вашего количество {type_of_units} недостаточно для создания построения ")

    def apply_buff(self, map):
        User.show_all_units()
        for name, building in self.__buildings.items():
            if name != "Баланс" and name != "Ресурсы":
                if building.amount != 0:
                    if name == "Военная академия":
                        self.create_formation(map)
                    if name == "Ремесленная мастерская":
                        for i in range(building.amount):
                            self.__balance = building.update_balance(self.__balance)
                            self.save_progress()
                    if isinstance(building, Building):
                        building.up_feature(User.show_coordinates())
        User.show_all_units()

    def town_stage(self, map_):
        print(f"\nВаш баланс {self.__balance} монет\n")
        tree, stone = self.__resources
        print(f"Ваши ресурсы: дерево - {tree}, камень - {stone}\n")
        self.show_all_buildings()
        affordable_buildings_list = get_list_of_affordable_buildings(self.__buildings, [tree, stone])
        upgradable_buildings_list = get_list_of_upgradeable_buildings(self.__buildings, [tree, stone])
        action = input(
            "Выберете действие: 1 - покупка зданий, 2 - апгрейд зданий, 3 - зайти на рынок/академию, 4 - сидеть афк: ")
        print()
        if action == "1":
            self.buy_buildings(affordable_buildings_list, map_)
        elif action == "2":
            self.upgrade_buildings(upgradable_buildings_list)
        elif action == "3":
            self.visit_town(map_)
        else:
            self.apply_buff(map_)

    def upgrade_buildings(self, upgradable_buildings_list):
        if len(upgradable_buildings_list) == 0:
            print("Вы не можете прокачивать здания")
        else:
            building = input("Введите здание, которое хотите апгрейднуть: ")
            while building not in upgradable_buildings_list:
                building = input("Такого здания нет в списке доступных, выберете другое: ")
            self.helper_func_for_upgrading(building)

    def buy_buildings(self, affordable_buildings_list, map_):
        if len(affordable_buildings_list) == 0:
            print("Вы не можете покупать здания")
        else:
            building = input("Введите здание, которое хотите купить: ")
            while building not in affordable_buildings_list:
                building = input(
                    "Такого здания нет в списке доступных или оно уже было приобретено, выберете другое: ")
            self.helper_func_for_buying(building, map_)

    def visit_town(self, map_):
        print("Выберете здание, в которое хотите зайти:\n", "1 - Рынок\n", "2 - Академия")
        choice = input()
        if choice == "2":
            if self.__buildings["Академия"].amount == 1:
                self.__balance = self.__buildings["Академия"].research_new_unit(self.__balance)
                self.save_progress()
            else:
                print("Вы еще не купили это здание\n")
        else:
            if self.__buildings["Рынок"].amount == 1:
                self.__resources = self.__buildings["Рынок"].exchange(self.__resources)
                self.save_progress()
            else:
                print("Вы еще не купили это здание\n")
        self.apply_buff(map_)

    def helper_func_for_buying(self, building, map_):
        object_building = self.__buildings[building]
        self.__resources = object_building.buy(self.__resources)
        if building in ["Дом лекаря", "Казарма", "Кузница", "Таверна"]:
            object_building.up_feature(User.show_coordinates())
        elif building == "Академия":
            self.__balance = object_building.research_new_unit(self.__balance)
        elif building == "Рынок":
            self.__resources = object_building.exchange(self.__resources)
        elif building == "Военная академия":
            self.create_formation(map_)
        else:
            self.__balance = object_building.update_balance(self.__balance)
        self.save_progress()

    def helper_func_for_upgrading(self, building):
        object_building = self.__buildings[building]
        self.__resources = object_building.upgrade(self.__resources)
        if building in ["Дом лекаря", "Казарма", "Кузница", "Таверна"]:
            object_building.up_feature(User.show_coordinates())
        elif building == "Академия":
            self.__balance = object_building.research_new_unit(self.__balance)
        elif building == "Рынок":
            self.__resources = object_building.exchange(self.__resources)
        self.save_progress()

    def show_all_buildings(self):
        print("Ваш город в состоит из следующих зданий:")
        for name, building in self.__buildings.items():
            if name != "Баланс" and name != "Ресурсы":
                if building.amount != 0:
                    if name == "Ремесленная мастерская":
                        print(f"{name}, Количество зданий: {building.amount}")
                    elif isinstance(building, Building):
                        print(f"{name}, Уровень: {building.lvl}")
                    else:
                        print(name)
        print()

    def save_progress(self):
        directory = r"C:\Users\Матвей\PycharmProjects\MapEditor\Progress\progress"
        with open(directory, "wb") as f:
            self.__buildings["Баланс"] = self.__balance
            self.__buildings["Ресурсы"] = self.__resources
            pickle.dump(self.__buildings, f)

    @staticmethod
    def load_progress():
        file_path = r"C:\Users\Матвей\PycharmProjects\MapEditor\Progress\progress"
        if os.path.exists(file_path):
            with open(file_path, "rb") as f:
                return pickle.load(f)
        else:
            return {"Баланс": 100,
                    "Ресурсы": [100, 100],
                    "Дом лекаря": Hospital(),
                    "Кузница": Forge(),
                    "Казарма": Barrack(),
                    "Рынок": Market(),
                    "Академия": Academy(),
                    "Ремесленная мастерская": BuilderHut(),
                    "Таверна": Tavern(),
                    "Военная академия": MilitaryAcademy()
                    }

    @staticmethod
    def show_units():
        names = [unit.name for unit in User.show_coordinates().values()]
        print("\nСписок купленных наемников:")
        print(', '.join(names))

    @staticmethod
    def show_bot_units():
        names = [unit.name for unit in Bot.show_coordinates().values()]
        print("\nСписок наемников, выданных боту:")
        print(', '.join(names))
