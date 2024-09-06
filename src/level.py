import pygame

import random

from src.utils import *
from src.brick import Brick



class Level:

    def __init__(self, screen: pygame.Surface) -> None:
        self.screen = screen
        self.bg = pygame.Surface((WIDTH, HEIGHT))
        self.bg.fill((98, 122, 174))
        pygame.draw.rect(self.bg, (46, 59, 85), (
            X_OFFSET, Y_OFFSET, 
            GRID_WIDTH * (BRICK_GAP + BRICK_SIZE) + BRICK_GAP, 
            GRID_HEIGHT * (BRICK_GAP + BRICK_SIZE) + BRICK_GAP
        ))
        self.BRICK_RANGE = 3
        self.matrix : list[list[Brick | None]] = [[Brick(self.screen, random.randint(1, self.BRICK_RANGE), (y, x))
                                                   for y in range(GRID_WIDTH)] for x in range(GRID_HEIGHT)]
        for i in self.matrix:
            print()
            for j in i:
                print(j)

    def __bool__(self) -> bool:
        return all([x is None or not x for y in self.matrix for x in y])
        
    def draw(self, cursor_pos: tuple[int, int]) -> None:
        self.screen.blit(self.bg, (0, 0))
        for j in range(GRID_WIDTH):
            for i in reversed(range(GRID_HEIGHT)):
                if self.matrix[i][j] is not None:
                    self.matrix[i][j].draw()
                else:
                    break

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
                print("lol")
                for key, c in cols_to_fall.items():
                    if c > 0:
                        for _ in range(c):
                            for i in range(GRID_HEIGHT - 1, 0, -1):
                                if self.matrix[i][key] is None and self.matrix[i - 1][key] is not None:
                                    self.matrix[i][key], self.matrix[i - 1][key] = self.matrix[i - 1][key], self.matrix[i][key]
                                    self.matrix[i][key].counter.y += 1 
                for col in range(GRID_WIDTH // 2 - 1):
                    if self.matrix[GRID_HEIGHT - 1][col + 1] is None:
                        for i in range(col, -1, -1):
                            for row in range(GRID_HEIGHT - 1, -1, -1):
                                if self.matrix[row][i] is not None:
                                    self.matrix[row][i].counter.x += 1
                                    print(row, i, 1)
                                    self.matrix[row][i], self.matrix[row][i + 1] = self.matrix[row][i + 1], self.matrix[row][i]
                                else:
                                    break
                for col in range(GRID_WIDTH // 2 - 1): 
                    if self.matrix[GRID_HEIGHT - 1][GRID_WIDTH - 2 - col] is None:
                        for i in range(GRID_WIDTH - 1 - col, GRID_WIDTH):
                            for row in range(GRID_HEIGHT - 1, -1, -1):
                                if self.matrix[row][i] is not None:
                                    print(row, i, -1)
                                    self.matrix[row][i].counter.x -= 1
                                    self.matrix[row][i], self.matrix[row][i - 1] = self.matrix[row][i - 1], self.matrix[row][i]
                                else:
                                    break
                for i in self.matrix:
                        print(i)
                        
                        

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
