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

    def change_map(self, battle_field):
        self.field = battle_field

    def update(self, dic_of_units, flag="default"):  # метод, который обновляет карту при появлении новых юнитов
        for number, unit in dic_of_units.items():
            self.field[unit.current_coordinates[0]][unit.current_coordinates[1]] = number
        print(self)

    def update_map_after_formation(self, dic_of_units, type_of_units):
        x = 7
        y = 7
        counter = 0
        nums = []
        if type_of_units == "пешие":
            for number, unit in dic_of_units.items():
                if unit._type == "Пеший":
                    self.field[unit.current_coordinates[0]][unit.current_coordinates[1]] = "*"
                    unit._current_coordinates = (x, y)
                    nums.append(number)
                    self.field[unit.current_coordinates[0]][unit.current_coordinates[1]] = unit._number
                    if counter == 0:
                        x += 1
                    elif counter == 1:
                        y += 1
                    elif counter == 2:
                        x -= 1
                    else:
                        print("Построение выполнено\n")
                        print(self)
                        break
                    counter += 1
        elif type_of_units == "всадники":
            for number, unit in dic_of_units.items():
                if unit._type == "Всадник":
                    self.field[unit.current_coordinates[0]][unit.current_coordinates[1]] = "*"
                    unit._current_coordinates = (x, y)
                    nums.append(number)
                    self.field[unit.current_coordinates[0]][unit.current_coordinates[1]] = unit._number
                    if counter == 0:
                        x -= 1
                        y += 2
                    elif counter == 1:
                        x += 1
                    elif counter == 2:
                        x += 1
                    else:
                        print("Построение выполнено\n")
                        print(self)
                        break
                    counter += 1
        else:
            for number, unit in dic_of_units.items():
                if unit._type == "Лучник":
                    self.field[unit.current_coordinates[0]][unit.current_coordinates[1]] = "*"
                    unit._current_coordinates = (x, y)
                    nums.append(number)
                    self.field[unit.current_coordinates[0]][unit.current_coordinates[1]] = unit._number
                    if counter == 0 or counter == 1:
                        x += 1
                    elif counter == 2:
                        y += 1
                    elif counter == 3 or counter == 4:
                        x -= 1
                    else:
                        print("Построение выполнено\n")
                        print(self)
                        break
                    counter += 1
        return nums



