import os
import json
import random
from typing import List, Dict
import logging

directory = os.getcwd() + r'\Maps\\'


class MapEditor:
    obstacles: Dict[str, float] = {
        "!": [1.2, 1.0, 1.5],
        "@": [2.0, 2.2, 1.2],
        "#": [1.5, 1.8, 2.2]
    }
    map_counter: int = 0
    available_maps: List[str] = os.listdir(directory)
    current_map: List[List[str]] = []
    logger = None

    def __init__(self):
        print("Вы находитесь в редакторе карт\n")
        MapEditor.setup_log()

    @classmethod
    def setup_log(cls):
        cls.logger = logging.getLogger('MapEditor')
        cls.logger.setLevel(logging.DEBUG)
        handler = logging.FileHandler('logs.txt', 'a', 'utf-8')
        formatter = logging.Formatter("%(filename)s[LINE:%(lineno)d]# %(levelname)-8s [%(asctime)s]  %(message)s")
        handler.setFormatter(formatter)
        cls.logger.addHandler(handler)

    @classmethod
    def load_number_of_latest_map(cls) -> None:
        if len(os.listdir(directory)) == 0:
            cls.map_counter = 0
        else:
            cls.map_counter = int(sorted(os.listdir(directory))[-1])

    @classmethod
    def load_obstacles_from_file(cls) -> None:
        obstacle_directory = os.getcwd() + r'\Obstacles'
        if not os.path.isdir(obstacle_directory):
            os.mkdir(obstacle_directory)
            with open(obstacle_directory + r'\obstacles', 'w') as f:
                json.dump({
                    "!": [1.2, 1.0, 1.5],
                    "@": [2.0, 2.2, 1.2],
                    "#": [1.5, 1.8, 2.2]
                }, f)
        else:
            with open(obstacle_directory + r'\obstacles', 'r') as f:
                cls.obstacles = json.load(f)

    @classmethod
    def actions(cls) -> None:
        cls.load_number_of_latest_map()
        while True:
            action = input("Выберете действие: 1-создать пустую/рандомную карту, 2-удалить все карты/какую-то одну, "
                           "3-отредактировать карту, 4 - показать все карты, , 5 - выйти из редактора: ")
            if action == "1":
                cls.create_map()
                break
            elif action == "2":
                cls.delete_maps()
            elif action == "3":
                cls.edit_map()
            elif action == "4":
                cls.show_all_maps()
            else:
                print("Вы вышли из редактора карт")
                break

    @classmethod
    def save_to_json(cls, field: List[List[str]], map_counter: int) -> None:
        global directory
        map_file = directory + str(map_counter)
        with open(map_file, "w") as f:
            json.dump({map_counter: field}, f)
        cls.logger.info(f"Карта под номером {cls.map_counter} была успешно сохранена в файл")

    @classmethod
    def delete_maps(cls) -> None:
        global directory
        action = input("Выберете действие: 1-удалить все карты, 2-удалить конкретную карту: ")
        while action != "1" and action != "2":
            action = input("Вы ввели не ту цифру, введите - 1, чтобы удалить все карты, введите - 2, чтобы удалить "
                           "конкретную карту")
            cls.logger.error("Введена неверная цифра при выборе действия при удалении")
        if action == "1":
            os.remove(directory)
            cls.logger.info(f"Все карты были удалены")
            os.mkdir(directory)
            cls.available_maps.clear()
        else:
            num = cls.correct_num()
            if num != "-1":
                map_file = directory + num
                os.remove(map_file)
                cls.logger.info(f"Карта под номером: {num} была удалена")
                cls.available_maps.remove(num)

    @classmethod
    def edit_map(cls) -> None:
        num = cls.correct_num()
        if num != "-1":
            field = cls.edit(cls.get_field(num))
            cls.current_map = field
            cls.save_to_json(field, num)

    @classmethod
    def correct_num(cls) -> str:
        if len(cls.available_maps) == 0:
            print("Еще ни одна карта не была создана, создайте карту, а только потом редактируйте/удаляйте ее")
            cls.logger.error("Еще ни одна карта не была создана")
            return "-1"
        else:
            print("Список карт, доступных для редактирования/удаления:", *cls.available_maps, "\n")
            num = input("Выберете номер карты, которую хотите отредактировать/удалить: ")
            while num not in cls.available_maps:
                num = input("Карта под этим номером была удалена или еще не была создана, выберете другую карту:")
                cls.logger.error("Карта под этим номером была удалена или еще не была создана")
            return num

    @classmethod
    def edit(cls, field: List[List[str]]) -> List[List[str]]:
        cls.load_obstacles_from_file()
        print("Введите новые препятствия и штрафы для них")
        cls.print_field(field)
        coordinates = cls.correct_coordinates()
        while coordinates != [-1, -1]:
            row, col = coordinates
            obstacle = input("Введите желаемое препятствие: ")
            if obstacle not in cls.obstacles.keys():
                cls.add_obstacle_to_file(obstacle)
            field[row][col] = obstacle
            cls.print_field(field)
            coordinates = cls.correct_coordinates()
        return field

    @classmethod
    def add_obstacle_to_file(cls, obstacle: str) -> None:
        foot_warrior_fine = float(input("Введите штраф для пеших воинов: "))
        archer_fine = float(input("Введите штраф для лучников: "))
        horse_warrior_fine = float(input("Введите штраф для всадников: "))
        cls.obstacles.update({obstacle: [foot_warrior_fine, archer_fine, horse_warrior_fine]})
        obstacle_directory = os.getcwd() + r'\Obstacles'
        with open(obstacle_directory + r'\obstacles', 'w') as f:
            json.dump(cls.obstacles, f)
        cls.logger.warning(f"Препятствие: {obstacle} было создано, штрафы: {foot_warrior_fine}, {archer_fine}, {horse_warrior_fine}")

    @staticmethod
    def correct_coordinates() -> List[int]:
        coordinates = list(map(int, input("Введите координаты клетки, которую хотите отредактировать:").split()))
        row, col = coordinates
        while True:
            if row == -1 and col == -1:
                return [row, col]
            elif (row < 0 or row >= 15) or (col < 0 or col >= 15):
                coordinates = list(map(int, input("Вы вышли за пределы поля, выберете другую клетку: ")))
                MapEditor.logger.error("Выход за пределы поля")
                row, col = coordinates
            elif row == 0 or row == 14:
                coordinates = list(map(int, input("Нельзя создавать препятствия на линии спавна юнитов, выберите "
                                                  "другую клетку: ").split()))
                MapEditor.logger.error("Создание препятствия на линии спавна юнитов")
                row, col = coordinates
            else:
                return coordinates

    @classmethod
    def show_all_maps(cls) -> None:
        for num in cls.available_maps:
            print(num)
            cls.print_field(cls.get_field(num))

    @staticmethod
    def print_field(field: List[List[str]]) -> None:
        for i in range(15):
            print(*field[i])
        print("\n")

    @staticmethod
    def get_field(num: str) -> List[List[str]]:
        global directory
        map_file = directory + num
        with open(map_file, "r") as f:
            dic = json.load(f)
            return dic[num]

    @classmethod
    def create_map(cls) -> None:
        action = input("Выберете действие: 1 - создать пустую карту, 2 - создать рандомную карту: ")
        while action != "1" and action != "2":
            action = input("Вы ввели не ту цифру, введите: 1, чтобы создать пустую карту, введите: 2, чтобы создать "
                           "рандомную карту: ")
            cls.logger.error("Введена неверная цифра при создании карты")
        if action == "2":
            cls.create_random_map()
        else:
            cls.create_empty_map()

    @classmethod
    def create_random_map(cls) -> None:
        symbol_pool = ["*", "*", "*", "*", "*", "*", "*", "*", "*", "*", "*", "!", "@", "#"]
        field = [["*"] * 15 for _ in range(15)]
        for i in range(1, 14):
            field[i] = [random.choice(symbol_pool) for _ in range(15)]
        cls.map_counter += 1
        cls.available_maps.append(str(cls.map_counter))
        print(f"Вы создали карту под номером {cls.map_counter}")
        cls.print_field(field)
        cls.logger.info(f"Рандомная карта номер {cls.map_counter} была успешно создана")
        cls.save_to_json(field, cls.map_counter)
        cls.current_map = field

    @classmethod
    def create_empty_map(cls) -> None:
        field = [["*"] * 15 for _ in range(15)]
        cls.map_counter += 1
        cls.available_maps.append(str(cls.map_counter))
        print(f"Вы создали карту под номером {cls.map_counter}")
        cls.print_field(field)
        cls.logger.info(f"Пустая карта номер {cls.map_counter} была успешно создана")
        cls.save_to_json(field, cls.map_counter)
        cls.current_map = field


MapEditor().actions()
