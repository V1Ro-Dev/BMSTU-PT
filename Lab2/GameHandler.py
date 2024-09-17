from User import User
from Bot import Bot
from Field import Field
from Menu import Menu
import time


class GameHandler:
    def __init__(self):
        self.__menu = Menu()
        self.__map = Field()

    def buy_stage(self):
        self.__menu.show_description_of_units()
        self.__menu.buy_mega_unit()
        self.__menu.buy_units_for_bot()
        self.__map.update(User.show_coordinates())
        self.__map.update(Bot.show_coordinates())

    def battle_stage(self):
        while Bot.show_coordinates() and User.show_coordinates():
            for unit in User.show_coordinates().values():
                action = input("Выберете действие: 1 - атака + перемещение, 2 - только атака, 3 - только перемещение, 4 - сидеть афк: ")
                if action == "1":
                    unit.move(self.__map)
                    unit.attack(self.__map, Bot.show_coordinates())
                elif action == "2":
                    unit.attack(self.__map, Bot.show_coordinates())
                elif action == "3":
                    unit.move(self.__map)
                elif action == "4":
                    pass

            for bot_unit in Bot.show_coordinates().values():
                bot_unit.attack(self.__map, User.show_coordinates())
                time.sleep(2)
        if not Bot.show_coordinates():
            print("Поздравляю, вы победили в сражении\n")
        else:
            print("К сожалению бот вас обыграл\n")


b = GameHandler()
b.buy_stage()
b.battle_stage()