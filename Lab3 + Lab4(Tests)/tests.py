import pickle
from math import sqrt
import io
from GameHandler import GameHandler
from User import User
from Bot import Bot
import pytest
from Menu import Menu
from unittest.mock import patch
from FindPath import shortest_path_with_obstacles, check_destination_point


#тест 1
def test_player_win():
    fake_inputs = [
        "No",
        "2",
        "A"
    ]

    with patch('builtins.input', side_effect=fake_inputs):
        game = GameHandler()
        game.load_maps_stage()
        game.player_test()
        result = game.battle_stage()

    assert result == 'Поздравляю, вы победили в сражении\n'


#тест 2
def test_bot_win():
    fake_inputs = [
        'No',
        "мечник",
        "4"
    ]

    with patch('builtins.input', side_effect=fake_inputs):
        game = GameHandler()
        game.load_maps_stage()
        game.bot_test()
        result = game.battle_stage()

    assert result == 'К сожалению бот вас обыграл\n'


#тест 3
def test_fine():
    fake_inputs = [
        'Yes',
        "3",
        'мечник',
        "3",
    ]
    with patch('builtins.input', side_effect=fake_inputs):
        game = GameHandler()
        game.load_maps_stage()
        game.buy_stage()
        map = game._GameHandler__map
        start = (0, 0)
        end = (5, 5)
        result = round(shortest_path_with_obstacles(map.field, start, end, "Пеший"), 2)
        assert result == round(float(sqrt(50)), 2)


#тест 4,5
def test_attack():
    fake_inputs = [
        "yes",
        "3",
        'мечник',
    ]
    fake_input = ["A"]
    with patch('builtins.input', side_effect=fake_inputs):
        game = GameHandler()
        game.load_maps_stage()
        game.buy_stage()
        map = game._GameHandler__map
        unit = User._coordinates["1"]
        with patch('sys.stdout', new=io.StringIO()) as fake_stdout:
            unit.attack(map, Bot.show_coordinates())
            output = fake_stdout.getvalue()
            print(output)
            assert 'Вы никого не можете атаковать' in output
        unit._attack_range = 100
        with patch('builtins.input', side_effect=fake_input):
            with patch('sys.stdout', new=io.StringIO()) as fake_stdout:
                unit.attack(map, Bot.show_coordinates())
                unit_1 = unit.my_dict["A"]
                output = fake_stdout.getvalue()
                assert f"Вы атаковали юнита под номером {"A"}, его характеристики: {unit_1}\n" in output


#тест 6
def test_moving():
    fake_inputs = [
        "yes",
        "4",
        'мечник',
    ]
    with patch('builtins.input', side_effect=fake_inputs):
        game = GameHandler()
        game.load_maps_stage()
        game.buy_stage()
        map = game._GameHandler__map
        end_1 = (4, 0)
        end_2 = (14, 14)
        end_3 = (20, 20)
        result_1 = check_destination_point(map.field, end_1)
        assert result_1 == False
        result_2 = check_destination_point(map.field, end_2)
        assert result_2 == False
        result_3 = check_destination_point(map.field, end_3)
        assert result_3 == False


#тест 7 и 12
def test_die():
    fake_inputs = [
        "yes",
        "4",
    ]
    fake_input = ["A"]
    with patch('builtins.input', side_effect=fake_inputs):
        game = GameHandler()
        game.load_maps_stage()
        game.player_test()
        map = game._GameHandler__map
        unit = User._coordinates["1"]
        with patch('builtins.input', side_effect=fake_input):
            result = unit.attack(map, Bot.show_coordinates())
            assert result == True


#тест 8
def test_defense():
    fake_inputs = [
        "yes",
        "4",
    ]
    fake_input = ["A"]
    with patch('builtins.input', side_effect=fake_inputs):
        game = GameHandler()
        game.load_maps_stage()
        game.player_test()
        map = game._GameHandler__map
        unit = User._coordinates["1"]
        unit._attack_points = 1
        expected = Bot.show_coordinates()["A"]._defense_points - 1
        with patch('builtins.input', side_effect=fake_input):
            print(Bot.show_coordinates()["A"])
            unit.attack(map, Bot.show_coordinates())
            assert Bot.show_coordinates()["A"]._defense_points == expected


#тест 9
def test_buy():
    fake_inputs = [
        "yes",
        "4",
        'мечник',
    ]
    with patch('builtins.input', side_effect=fake_inputs):
        game = GameHandler()
        game.load_maps_stage()
        game.buy_stage()
        unit = User._coordinates["1"]
        assert "Мечник" == unit.name


#тест 10
def test_bot_actions():
    fake_inputs = [
        "yes",
        "4",
        'мечник',
    ]
    with patch('builtins.input', side_effect=fake_inputs):
        game = GameHandler()
        game.load_maps_stage()
        game.buy_stage()
        unit = User._coordinates["1"]
        bot = Bot._bot_coordinates["A"]
        map = game._GameHandler__map
        bot.attack(map, User.show_coordinates())
        assert bot._current_coordinates == (13, 14)
        unit._current_coordinates = (13, 13)
        bot.attack(map, User.show_coordinates())
        assert bot._current_coordinates == (13, 14)


#тест 11
def test_field():
    fake_inputs = [
        "yes",
        "4",
        'мечник',
    ]
    with patch('builtins.input', side_effect=fake_inputs):
        game = GameHandler()
        game.load_maps_stage()
        game.buy_stage()
        map = game._GameHandler__map
        assert map.field[0][0] == "1"


# тест 16
def test():
    fake_inputs = [
        "yes",
        "4",
        'мечник',
        '2',
        'Дом лекаря'
    ]
    with patch('builtins.input', side_effect=fake_inputs):
        game = GameHandler()
        game.load_maps_stage()
        game.buy_stage()
        game.build_town_stage()
        menu = game._GameHandler__menu
        buildings = menu._Menu__buildings
        assert buildings["Дом лекаря"].lvl == 2


# тест 17
def test_academy():
    fake_inputs = [
        '3',
        '2',
        'пеший',
        'llll',
        '1',
        '1',
        '1',
        '1',
        '1',
        'yes',
        'no'
    ]
    with patch('builtins.input', side_effect=fake_inputs):
        game = GameHandler()
        game.build_town_stage()
        menu = game._GameHandler__menu
        with open(r'C:\Users\Матвей\PycharmProjects\MapEditor\Progress\progress', 'rb') as f:
            buildings = pickle.load(f)
        print(buildings["Академия"].pending_units)
        assert ['пеший', 'llll', 1, 1, 1, 1, 1, 5] in buildings["Академия"].pending_units
        assert menu._Menu__balance == buildings["Баланс"]


def test_builders_hut():
    fake_inputs = [
        '4',
        'no'
    ]
    with patch('builtins.input', side_effect=fake_inputs):
        game = GameHandler()
        game.build_town_stage()
        menu = game._GameHandler__menu
        with open(r'C:\Users\Матвей\PycharmProjects\MapEditor\Progress\progress', 'rb') as f:
            buildings = pickle.load(f)
        assert menu._Menu__balance == buildings["Баланс"]


def test_market():
    fake_inputs = [
        '3',
        '1',
        'yes',
        'камень',
        '5',
        'no'
    ]
    with patch('builtins.input', side_effect=fake_inputs):
        game = GameHandler()
        game.build_town_stage()
        menu = game._GameHandler__menu
        with open(r'C:\Users\Матвей\PycharmProjects\MapEditor\Progress\progress', 'rb') as f:
            buildings = pickle.load(f)
        assert menu._Menu__resources == buildings["Ресурсы"]

def test_progress():
    fake_inputs = [
        '2',
        'Дом лекаря'
    ]
    with patch('builtins.input', side_effect=fake_inputs):
        game = GameHandler()
        game.build_town_stage()
        with open(r'C:\Users\Матвей\PycharmProjects\MapEditor\Progress\progress', 'rb') as f:
            buildings = pickle.load(f)
        assert buildings["Дом лекаря"].lvl == 3


