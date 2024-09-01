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
                self.matrix[i][j].draw()

    def pressed(self, pos: tuple[int, int]) -> int:
        row = (pos[1] - Y_OFFSET - BRICK_GAP) // (BRICK_SIZE + BRICK_GAP)
        col = (pos[0] - X_OFFSET - BRICK_GAP) // (BRICK_SIZE + BRICK_GAP)
        if (row >= 0 and row < GRID_HEIGHT and
            col >= 0 and col < GRID_WIDTH and
            self.matrix[row][col] is not None):
            visited = [[False for x in range(GRID_WIDTH)] for y in range(GRID_HEIGHT)]
            blob = self.dfs_board(row, col, visited, self.matrix[row][col].index)
            print(blob)

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
