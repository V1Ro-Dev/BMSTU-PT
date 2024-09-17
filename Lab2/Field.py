import random


class Field:

    def __init__(self):
        self.__symbol_pool = ["*", "*", "*", "*", "*", "*", "*", "*", "*", "*", "*", "!", "@", "#"]
        self.field = [["*"] * 15 for _ in range(15)]
        for i in range(1, 14):
            self.field[i] = [random.choice(self.__symbol_pool) for _ in range(15)]

    def __str__(self):  # вывод карты
        print("Поле битвы:")
        for i in range(15):
            print(*self.field[i])
        return ""

    def update(self, dic_of_units):  # метод, который обновляет карту при появлении новых юнитов
        for number, unit in dic_of_units.items():
            self.field[unit.current_coordinates[0]][unit.current_coordinates[1]] = number
        print(self)
