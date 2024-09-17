import json
import os
from MapEditor import MapEditor
from unittest.mock import patch
import pytest

directory = os.getcwd() + r'\Maps\\'


#тест 13 + 16
def test_map_creation_empty():
    input_1 = [
        '1',
        '1',
    ]
    with patch('builtins.input', side_effect=input_1):
        MapEditor.actions()
        result = MapEditor.current_map
        print(MapEditor.map_counter)
        real_map = [[]]
        with open(directory + str(MapEditor.map_counter), 'r') as f:
            real_map = json.load(f)[str(MapEditor.map_counter)]
    assert result == real_map


def test_map_creation_random():
    input_2 = [
        '1',
        '2'
    ]
    with patch('builtins.input', side_effect=input_2):
        MapEditor.actions()
        result = MapEditor.current_map
        real_map = [[]]
        with open(directory + str(MapEditor.map_counter), 'r') as f:
            real_map = json.load(f)[str(MapEditor.map_counter)]
    assert result == real_map


#тест 14
def test_obstacles():
    input_1 = [
        '3',
        '10',
        "1 1",
        "$",
        50.0,
        50.0,
        50.0,
        "-1 -1",
        '5'
    ]
    with patch('builtins.input', side_effect=input_1):
        MapEditor.actions()
        result = MapEditor.current_map
        with open(directory + "10", 'r') as f:
            real_map = json.load(f)["10"]
        print(real_map)
    assert result == real_map


#тест 15
def test_editing():
    input_1 = [
        '3',
        '9',
        "1 1",
        "#",
        "-1 -1",
        '5'
    ]
    with patch('builtins.input', side_effect=input_1):
        MapEditor.actions()
        result = MapEditor.current_map
        with open(directory + "9", 'r') as f:
            real_map = json.load(f)["9"]
        print(real_map)
    assert result == real_map


