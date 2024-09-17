from User import User
from Bot import Bot
from tabulate import tabulate
from Welcome_Text import text
import random


class Menu:

    def __init__(self):
        print(text, "\n")
        self.__balance = 100
        self.__bot_balance = 100
        print(
            f"На город готовится нападение. В городской казне есть сумма:{self.__balance} для покупки наемников, защищающих город. Характеристики воинов:\n")
        self.units = [User("Мечник", 50, 8, 5, 1, 3, 10), User("Копьеносец", 35, 4, 3, 1, 6, 15),
                      User("Топорщик", 45, 3, 9, 1, 4, 20), User("Лучник с длинным луком", 30, 8, 6, 5, 2, 15),
                      User("Лучник с коротким луком", 25, 4, 3, 3, 4, 19), User("Арбалетчик", 40, 3, 7, 6, 2, 23),
                      User("Рыцарь", 30, 3, 5, 1, 6, 20), User("Кирасир", 50, 7, 2, 1, 5, 23),
                      User("Конный лучник", 25, 2, 3, 3, 5, 25)]
        User.clear()

    def show_description_of_units(self):
        table_data = []
        for unit in self.units:
            table_data.append([unit.name, unit.hp, unit.defense_points, unit.attack_points, unit.attack_range, unit.move_range, unit.price, unit.current_coordinates])

        headers = ["Type", "HP", "Defense Points", "Attack Points", "Attack Range", "Move Range", "Price",
                   "Current Coordinates"]
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
        print("Выберете юнита, которого хотите купить. Необходимо ввести полное название")
        while self.__balance >= 10:
            unit_type = input().lower()
            if self.check_unit(unit_type):
                if self.__balance >= self.check_price(unit_type):
                    self.__balance -= self.check_price(unit_type)
                    User.fill_coordinates(unit_type)
                    print(f"Вы успешно купили {unit_type}, ваш текущий баланс:{self.__balance}")
                else:
                    print(f"Недостаточно денег для покупки {unit_type}, введите другого юнита")
            else:
                print("Такого юнита не существует, введите корректное название")
        self.show_units()

    def buy_units_for_bot(self):
        lst_of_units = ["мечник", "копьеносец", "топорщик", "лучник с длинным луком", "лучник с коротким луком", "арбалетчик", "рыцарь", "кирасир", "конный лучник"]
        while self.__bot_balance >= 10:
            unit_type = random.choice(lst_of_units)
            if self.__bot_balance >= self.check_price(unit_type):
                self.__bot_balance -= self.check_price(unit_type)
                Bot.fill_coordinates(unit_type)
        self.show_bot_units()

    def buy_mega_unit(self):
        print("Выберете юнита, которого хотите купить. Необходимо ввести полное название")
        unit_type = "мега лучник"
        User.fill_coordinates(unit_type)
        self.show_units()

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


# a = Menu()
# a.show_description_of_units()
# a.buy_units_for_bot()
# a.buy_units()
