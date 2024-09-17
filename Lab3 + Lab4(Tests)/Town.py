import random
from typing import List
from User import User


class BaseBuilding:
    def __init__(self):
        self.tree = 0
        self.stone = 0
        self.name = ""
        self.amount = 0

    def can_buy(self, resources: List[int]) -> bool:
        tree, stone = resources
        if tree >= self.tree and stone >= self.stone:
            if self.name == "Ремесленная мастерская" and self.amount < 4:
                return True
            elif self.amount < 1:
                return True
        return False

    def buy(self, resources: List[int]) -> List[int]:
        resources[0] -= self.tree
        resources[1] -= self.stone
        self.amount += 1
        print(f"Ваш баланс ресурсов составляет: дерево - {resources[0]}, камень - {resources[1]}\n")
        return resources


class Building(BaseBuilding):
    def __init__(self):
        self.tree = 0
        self.stone = 0
        self.lvl = 1
        self.upgrade_tree = 0
        self.upgrade_stone = 0
        self.name = ""
        self.type_of_points = ""

    def up_feature(self, dict_of_units) -> None:
        for unit in dict_of_units.values():
            if self.lvl == 1:
                if self.name == "Дом лекаря":
                    unit._hp += 1
                elif self.name == "Кузница":
                    unit._attack_points += 1
                elif self.name == "Казарма":
                    unit._defense_points += 1
                elif self.name == "Таверна":
                    unit._move_range += 0.5
            elif self.lvl == 2:
                if self.name == "Дом лекаря":
                    unit._hp += 2
                elif self.name == "Кузница":
                    unit._attack_points += 2
                elif self.name == "Казарма":
                    unit._defense_points += 2
                elif self.name == "Таверна":
                    unit._move_range += 1.0
            elif self.lvl == 3:
                if self.name == "Дом лекаря":
                    unit._hp += 3
                elif self.name == "Кузница":
                    unit._attack_points += 3
                elif self.name == "Казарма":
                    unit._defense_points += 3
                elif self.name == "Таверна":
                    unit._move_range += 1.5
        self.show_upgraded_stats()

    def show_upgraded_stats(self):
        if self.lvl == 1:
            print(f"Всем юнитам прибавилось 1 {self.type_of_points}\n")
        elif self.lvl == 2:
            print(f"Всем юнитам прибавилось 2 {self.type_of_points}\n")
        else:
            print(f"Всем юнитам прибавилось 3 {self.type_of_points}\n")

    def upgrade(self, resources: List[int]) -> List[int]:
        tree, stone = resources
        if self.can_upgrade(resources):
            self.lvl += 1
            tree -= self.upgrade_tree
            stone -= self.upgrade_stone
            if self.lvl == 2:
                print(f"Вы прокачали {self.name} до {self.lvl} уровня\n")
                self.upgrade_tree = 3
                self.upgrade_stone = 3
            if self.lvl == 3:
                print(f"Вы прокачали {self.name} до максимального {self.lvl} уровня\n")
                self.upgrade_tree = 5
                self.upgrade_stone = 5
            resources[0] = tree
            resources[1] = stone
            return [tree, stone]
        else:
            print("Вам не хватает ресурсов для апгрейда здания\n")
            return [tree, stone]

    def can_upgrade(self, resources) -> bool:
        tree, stone = resources
        if tree >= self.upgrade_tree and stone >= self.upgrade_stone and self.lvl < 3:
            return True
        else:
            return False


class Hospital(Building):
    def __init__(self):
        self.tree = 10
        self.stone = 10
        self.lvl = 1
        self.upgrade_tree = 2
        self.upgrade_stone = 2
        self.name = "Дом лекаря"
        self.type_of_points = "хп"
        self.amount = 0


class Forge(Building):
    def __init__(self):
        self.tree = 15
        self.stone = 15
        self.lvl = 1
        self.upgrade_tree = 5
        self.upgrade_stone = 5
        self.name = "Кузница"
        self.type_of_points = "поинта атаки"
        self.amount = 0


class Barrack(Building):
    def __init__(self):
        self.tree = 13
        self.stone = 13
        self.lvl = 1
        self.upgrade_tree = 5
        self.upgrade_stone = 5
        self.name = "Казарма"
        self.type_of_points = "поинта защиты"
        self.amount = 0


class Market(BaseBuilding):
    def __init__(self):
        self.tree = 8
        self.stone = 8
        self.name = "Рынок"
        self.exchange_rate_tree = random.randint(1, 5)
        self.exchange_rate_stone = random.randint(1, 5)
        self.amount = 0

    def exchange(self, resources: List[int]) -> List[int]:
        self.update_exchange_rate()
        tree, stone = resources
        print(f"Курс дерева к камню на сегодняшний день: {self.exchange_rate_tree} к {self.exchange_rate_stone}\n")
        print(f"Количество ваших ресурсов в данный момент: дерево - {tree}, камень - {stone}\n")
        answer = input(f"хотите совершить обмен? (Yes/No) ").lower()
        if answer == "yes":
            resource = input("Введите ресурс, который вы хотите поменять (камень/дерево): ")
            amount = int(input("Введите количество ресурса, которое вы хотите поменять: "))
            if self.check_availability(resources, resource, amount):
                if resource == 'камень':
                    stone -= self.exchange_rate_stone * (amount // self.exchange_rate_stone)
                    tree += (amount // self.exchange_rate_stone) * self.exchange_rate_tree
                else:
                    tree -= self.exchange_rate_tree * (amount // self.exchange_rate_tree)
                    stone += (amount // self.exchange_rate_tree) * self.exchange_rate_stone
                print(f"В результате обмена количество дерева стало = {tree}, количество камня = {stone}\n")
                return [tree, stone]
            else:
                print("Вы ввели недостаточное количество ресурса, или вы уйдете в кредит по обмениваемому ресурсу\n")
                return resources
        else:
            return resources

    def check_availability(self, resources: List[int], resource: str, amount: int) -> bool:
        if resource == 'камень' and resources[
            1] >= amount >= self.exchange_rate_stone and amount // self.exchange_rate_stone * self.exchange_rate_tree <= \
                resources[0]:
            return True
        elif resources[
            0] >= amount >= self.exchange_rate_tree and amount // self.exchange_rate_tree * self.exchange_rate_stone <= \
                resources[1]:
            return True
        return False

    def update_exchange_rate(self):
        self.exchange_rate_tree = random.randint(1, 5)
        self.exchange_rate_stone = random.randint(1, 5)


class Academy(BaseBuilding):
    def __init__(self):
        self.tree = 8
        self.stone = 8
        self.name = "Академия"
        self.amount = 0
        self.pending_units = []

    def research_new_unit(self, balance):
        print(
            'Задайте характеристики своему будущему юниту. Если хотите выйти из меню создания новых юнитов, напишите "exit"\n')
        type_ = input("Введите тип вашего юнита: пеший/лучник/всадник: ")
        if type_ == "exit":
            return balance
        else:
            name = input("Введите название вашего юнита:")
            hp = int(input("Введите очки хп:"))
            defense_points = int(input("Введите очки защиты:"))
            attack_points = int(input("Введите очки атаки: "))
            attack_range = int(input("Введите радиус атаки: "))
            move_range = int(input("Введите очки перемещения: "))
            price = hp + defense_points + move_range + attack_points + attack_range
            if balance >= price:
                answer = input(f'Итоговая цена вашего юнита: {price}, хотите его исследовать? (Yes/No): ').lower()
                if answer == "yes":
                    self.pending_units.append(
                        [type_, name, hp, defense_points, attack_points, attack_range, move_range, price]
                    )
                    return balance - price
                else:
                    print("\nВы отказались от исследования юнита")
                    return balance
            else:
                print("Вам не хватает денег для исследования юнита")
                return balance


class BuilderHut(BaseBuilding):
    def __init__(self):
        self.tree = 8
        self.stone = 8
        self.name = "Ремесленная мастерская"
        self.amount = 0

    def update_balance(self, balance: int) -> int:
        earned_money = random.randint(1, 10)
        if earned_money >= 5:
            print(f"Сегодня рабочие хорошо потрудились и принесли в городскую казну {earned_money} монет\n")
        else:
            print(
                f"Сегодня часть рабочих ушла пить пиво, поэтому городская казна была пополнена всего на {earned_money} монеты\n")
        return balance + earned_money


class Tavern(Building):
    def __init__(self):
        self.tree = 13
        self.stone = 13
        self.lvl = 1
        self.upgrade_tree = 5
        self.upgrade_stone = 5
        self.name = "Таверна"
        self.amount = 0
        self.type_of_points = "очков перемещения"


class MilitaryAcademy(BaseBuilding):
    def __init__(self):
        self.tree = 10
        self.stone = 10
        self.name = "Военная академия"
        self.amount = 0


def get_list_of_affordable_buildings(dict_of_buildings, resources):
    result = []
    for building in dict_of_buildings.values():
        if isinstance(building, BaseBuilding) and building.can_buy(resources):
            result.append(building.name)
    if len(result) == 0:
        print("Вам не хватает ресурсов для покупки зданий\n")
        return result
    else:
        print("Вы можете купить здания:", ",".join(result), '\n')
        return result


def get_list_of_upgradeable_buildings(dict_of_buildings, resources):
    result = []
    for building in dict_of_buildings.values():
        if isinstance(building, Building) and building.can_upgrade(resources) and building.amount != 0:
            result.append(building.name)
    if len(result) == 0:
        print(
            "Вам не хватает ресурсов для апгрейда зданий или все возможные здания были прокачены до максимального "
            "уровня или вы еще не купили здание \n")
        return result
    else:
        print("Вы можете прокачать здания:", ",".join(result), '\n')
        return result
