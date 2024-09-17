from User import User
from Bot import Bot
from Field import Field
from Menu import Menu
import time
import os
import json


class GameHandler:

    def __init__(self):
        self.__menu = Menu()
        self.__map = None

    def load_maps_stage(self):
        directory = r"C:\Users\Матвей\PycharmProjects\MapEditor\Maps"
        answer = input("Хотите загрузить карту из предыдущих сражений (Yes, No): ").lower()
        print('\n')
        if answer == "yes":
            print("Номера карт, которые можно выбрать:", *(sorted(list(map(int, os.listdir(directory))))))
            map_num = input("Выберете номер карты, которую хотите загрузить: ")
            while map_num not in os.listdir(directory):
                map_num = input("Данная карта была удалена или ее не существует, выберете другую: ")
            with open(directory + f"\\{map_num}", "r") as f:
                print("Загрузка карты...")
                self.__map = Field()
                self.__map.change_map(json.load(f)[map_num])
        else:
            self.__map = Field()
            map_num = sorted(map(int, os.listdir(directory)))[-1] + 1
            with open(directory + f"\\{map_num}", "w") as f:
                json.dump({str(map_num): self.__map.field}, f)

    def build_town_stage(self):
        self.__menu.town_stage(self.__map)
        self.__menu.show_all_buildings()

    def buy_stage(self):
        self.__menu.show_description_of_units()
        self.__menu.buy_units()
        self.__menu.buy_units_for_bot()
        # self.__menu.buy_all_units()
        # self.__menu.buy_units()
        self.__map.update(User.show_coordinates())
        self.__map.update(Bot.show_coordinates())

    def bot_test(self):
        self.__menu.show_description_of_units()
        self.__menu.buy_units()
        self.__menu.buy_mega_unit_for_bot()
        self.__map.update(User.show_coordinates())
        self.__map.update(Bot.show_coordinates())

    def player_test(self):
        self.__menu.show_description_of_units()
        self.__menu.buy_mega_unit()
        self.__menu.buy_units_for_bot()
        self.__map.update(User.show_coordinates())
        self.__map.update(Bot.show_coordinates())

    def battle_stage(self):
        while Bot.show_coordinates() and User.show_coordinates():
            for unit in User.show_coordinates().values():
                action = input(
                    "Выберете действие: 1 - атака + перемещение, 2 - только атака, 3 - только перемещение, 4 - сидеть афк: ")
                print()
                if action == "1":
                    if unit.number in self.__menu.buffed_nums:
                        self.__menu.debuff()
                        self.__menu.buffed_nums = []
                        print("Все баффы юнитов в построении были утрачены")
                    unit.move(self.__map)
                    unit.attack(self.__map, Bot.show_coordinates())
                elif action == "2":
                    unit.attack(self.__map, Bot.show_coordinates())
                elif action == "3":
                    if unit.number in self.__menu.buffed_nums:
                        self.__menu.debuff()
                        self.__menu.buffed_nums = []
                        print("Все баффы юнитов в построении были утрачены")
                    unit.move(self.__map)
                elif action == "4":
                    pass

            for bot_unit in Bot.show_coordinates().values():
                bot_unit.attack(self.__map, User.show_coordinates())
        if not Bot.show_coordinates():
            return "Поздравляю, вы победили в сражении\n"
        else:
            return "К сожалению бот вас обыграл\n"

#b = GameHandler()
# b.load_maps_stage()
# b.buy_stage()
#b.build_town_stage()
# print(b.battle_stage())
