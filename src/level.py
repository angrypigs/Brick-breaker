import pygame

import random

from src.utils import *
from src.brick import Brick



class Level:

    def __init__(self, screen: pygame.Surface) -> None:
        self.screen = screen
        self.bg = pygame.Surface((WIDTH, HEIGHT))
        self.bg.fill((98, 122, 174))
        self.BRICK_RANGE = 4
        self.matrix : list[list[Brick | None]] = [[Brick(self.screen, random.randint(1, self.BRICK_RANGE), (y, x))
                                                   for y in range(GRID_WIDTH)] for x in range(GRID_HEIGHT)]
        for i in self.matrix:
            print()
            for j in i:
                print(j)
        
    def draw(self, cursor_pos: tuple[int, int]) -> None:
        self.screen.blit(self.bg, (0, 0))
        for i in range(GRID_HEIGHT):
            for j in range(GRID_WIDTH):
                if self.matrix[i][j] is not None:
                    self.matrix[i][j].draw()

    def pressed(self, pos: tuple[int, int]) -> int:
        row = (pos[1] - Y_OFFSET - BRICK_GAP) // (BRICK_SIZE + BRICK_GAP)
        col = (pos[0] - X_OFFSET - BRICK_GAP) // (BRICK_SIZE + BRICK_GAP)
        if (row >= 0 and row < GRID_HEIGHT and
            col >= 0 and col < GRID_WIDTH and
            self.matrix[row][col] is not None):
            visited = [[False for x in range(GRID_WIDTH)] for y in range(GRID_HEIGHT)]
            blob = self.dfs_board(row, col, visited, self.matrix[row][col].index)
            if len(blob) > 2:
                blob.sort(key=lambda x: (x[0], x[1]))
                cols_to_fall = {i: 0 for i in range(GRID_WIDTH)}
                for c in blob:
                    self.matrix[c[0]][c[1]] = None
                    cols_to_fall[c[1]] += 1
                for key, c in cols_to_fall.items():
                    if c > 0:
                        for _ in range(c):
                            for i in range(GRID_HEIGHT - 1, 0, -1):
                                if self.matrix[i][key] is None and self.matrix[i - 1][key] is not None:
                                    self.matrix[i][key], self.matrix[i - 1][key] = self.matrix[i - 1][key], self.matrix[i][key]
                                    self.matrix[i][key].fall_counter += 1               

    def dfs_board(self, row: int, col: int, visited: list[list[bool]], 
                  target: int) -> list[tuple[int, int]]:
        if (row < 0 or row >= GRID_HEIGHT or 
            col < 0 or col >= GRID_WIDTH or
            self.matrix[row][col] is None or 
            visited[row][col] or
            self.matrix[row][col].index != target):
            return []
        
        visited[row][col] = True
        blob = [(row, col)]
        blob += self.dfs_board(row + 1, col, visited, target)
        blob += self.dfs_board(row - 1, col, visited, target)
        blob += self.dfs_board(row, col + 1, visited, target)
        blob += self.dfs_board(row, col - 1, visited, target)
        return blob
