from collections import deque
from typing import Tuple, List
import math


def calculate_fine(name: str, obstacle: str) -> float:
    if obstacle == '@':
        if name in ["Мечник", "Копьеносец", "Топорщик"]:
            return 2.0
        elif name in ["Лучник с длинным луком", "Лучник с коротким луком", "Арбалетчик"]:
            return 2.2
        else:
            return 1.2
    elif obstacle == '#':
        if name in ["Мечник", "Копьеносец", "Топорщик"]:
            return 1.5
        elif name in ["Лучник с длинным луком", "Лучник с коротким луком", "Арбалетчик"]:
            return 1.8
        else:
            return 2.2
    elif obstacle == '!':
        if name in ["Мечник", "Копьеносец", "Топорщик"]:
            return 1.2
        elif name in ["Лучник с длинным луком", "Лучник с коротким луком", "Арбалетчик"]:
            return 1.0
        else:
            return 1.5


def check_destination_point(grid: List[List[str]], end: Tuple[int, ...], flag="User") -> bool:
    row = end[0]
    col = end[1]
    if flag == "User":
        if (row < 0 or row >= 15) or (col < 0 or col >= 15):
            print("Вы вышли за пределы поля")
            return False
        if grid[row][col] == "#" or grid[row][col] == "!" or grid[row][col] == "@":
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
        if grid[row][col].isdigit() or grid[row][col].isalpha():
            return False
        return True


def shortest_path_with_obstacles(grid: List[List[str]], start: Tuple[int, ...], end: Tuple[int, ...], name) -> float:
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
            return weight

        neighbors = [(row - 1, col), (row + 1, col), (row, col - 1), (row, col + 1),
                     (row - 1, col - 1), (row - 1, col + 1), (row + 1, col - 1), (row + 1, col + 1)]

        for neighbor_row, neighbor_col in neighbors:
            if is_valid(neighbor_row, neighbor_col) and (neighbor_row, neighbor_col) not in visited:
                new_weight = weight
                cell_value = grid[neighbor_row][neighbor_col]
                if cell_value == '@':
                    new_weight += calculate_fine(name, cell_value)
                elif cell_value == '#':
                    new_weight += calculate_fine(name, cell_value)
                elif cell_value == '!':
                    new_weight += calculate_fine(name, cell_value)
                else:
                    new_weight += 1

                if (row != neighbor_row) and (col != neighbor_col):
                    new_weight += calculate_distance(row, col, neighbor_row, neighbor_col) - 1

                queue.append((neighbor_row, neighbor_col, new_weight))
                visited.add((neighbor_row, neighbor_col))

    return -1.0
