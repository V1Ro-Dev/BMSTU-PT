from collections import deque
from typing import Tuple, List
import math
import json


def calculate_fine(type_: str, obstacle: str) -> float:
    with open(r'C:\Users\Матвей\PycharmProjects\MapEditor\Obstacles\obstacles', 'r') as f:
        obstacles = json.load(f)
    if obstacle in obstacles.keys():
        if type_ == "Пеший":
            return obstacles[obstacle][0]
        elif type_ == "Лучник":
            return obstacles[obstacle][1]
        elif type_ == "Всадник":
            return obstacles[obstacle][2]
        else:
            return min(*obstacles[obstacle])


def check_destination_point(grid: List[List[str]], end: Tuple[int, ...], flag: str = "User") -> bool:
    with open(r'C:\Users\Матвей\PycharmProjects\MapEditor\Obstacles\obstacles', 'r') as f:
        obstacles = json.load(f)
    row = end[0]
    col = end[1]
    if flag == "User":
        if (row < 0 or row >= 15) or (col < 0 or col >= 15):
            print("Вы вышли за пределы поля")
            return False
        if grid[row][col] in obstacles.keys():
            print("Нельзя находиться на препятствии")
            return False
        if grid[row][col].isdigit() or grid[row][col].isalpha():
            print("Вы наступили на другого юнита")
            return False
        return True
    else:
        if (row < 0 or row >= 15) or (col < 0 or col >= 15):
            return False
        if grid[row][col] == "#" or grid[row][col] == "!" or grid[row][col] == "@":
            return False
        if grid[row][col].isdigit() or grid[row][col].isalpha() or grid[row][col] == "$":
            return False
        return True


def shortest_path_with_obstacles(grid: List[List[str]], start: Tuple[int, ...], end: Tuple[int, ...], type_: str) -> float:
    with open(r'C:\Users\Матвей\PycharmProjects\MapEditor\Obstacles\obstacles', 'r') as f:
        obstacles = json.load(f)

    def is_valid(row, col):
        return 0 <= row < 15 and 0 <= col < 15

    def calculate_distance(row1, col1, row2, col2):
        return math.sqrt((row1 - row2) ** 2 + (col1 - col2) ** 2)

    queue = deque([(start[0], start[1], 0)])  # Кортеж (row, col, weight)
    visited = set()
    visited.add(start)

    while queue:
        row, col, weight = queue.popleft()

        if (row, col) == end:
            print(weight)
            return weight

        neighbors = [(row - 1, col), (row + 1, col), (row, col - 1), (row, col + 1),
                     (row - 1, col - 1), (row - 1, col + 1), (row + 1, col - 1), (row + 1, col + 1)]

        for neighbor_row, neighbor_col in neighbors:
            if is_valid(neighbor_row, neighbor_col) and (neighbor_row, neighbor_col) not in visited:
                new_weight = weight
                cell_value = grid[neighbor_row][neighbor_col]
                if cell_value in obstacles.keys():
                    new_weight += calculate_fine(type_, cell_value)
                else:
                    new_weight += 1

                if (row != neighbor_row) and (col != neighbor_col):
                    new_weight += calculate_distance(row, col, neighbor_row, neighbor_col) - 1

                queue.append((neighbor_row, neighbor_col, new_weight))
                visited.add((neighbor_row, neighbor_col))

    return -1.0
