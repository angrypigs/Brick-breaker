import pygame

import random

from src.utils import *
from src.brick import Brick



class Level:

    def __init__(self, 
                 screen: pygame.Surface,
                 lvl: int) -> None:
        self.screen = screen
        self.bg = pygame.Surface((WIDTH, HEIGHT))
        self.bg.fill((44, 77, 144))
        self.LIMIT = 120 + 10 * (lvl % 5) if lvl < len(COLORS) * 5 else 160
        self.lvl = lvl
        self._blocks_destroyed = 0
        pygame.draw.rect(self.bg, (18, 36, 72), (
            X_OFFSET, Y_OFFSET, 
            GRID_WIDTH * (BRICK_GAP + BRICK_SIZE) + BRICK_GAP, 
            GRID_HEIGHT * (BRICK_GAP + BRICK_SIZE) + BRICK_GAP
        ))
        pygame.draw.rect(self.bg, (18, 36, 72), (
            Y_OFFSET, Y_OFFSET, 360, GRID_HEIGHT * (BRICK_GAP + BRICK_SIZE) + BRICK_GAP
        ))
        self.BRICK_RANGE = 3
        self.matrix : list[list[Brick | None]] = [[Brick(self.screen, random.randint(1, min(lvl // 5 + 3, len(COLORS) - 1)), (y, x))
                                                   for y in range(GRID_WIDTH)] for x in range(GRID_HEIGHT)]

    def __bool__(self) -> bool:
        return all([x is None or x for y in self.matrix for x in y])
        
    def draw(self, cursor_pos: tuple[int, int]) -> None:
        self.screen.blit(self.bg, (0, 0))
        flag = all([x is None or not all(x.anim) for y in self.matrix for x in y])
        for j in range(GRID_WIDTH):
            for i in reversed(range(GRID_HEIGHT)):
                if self.matrix[i][j] is not None:
                    if flag and self.matrix[i][j].anim[1] and not self.matrix[i][j].anim_flag:
                        self.matrix[i][j].anim_flag = True
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
                                    self.matrix[row][i], self.matrix[row][i + 1] = self.matrix[row][i + 1], self.matrix[row][i]
                                else:
                                    break
                for col in range(GRID_WIDTH // 2 - 1): 
                    if self.matrix[GRID_HEIGHT - 1][GRID_WIDTH - 2 - col] is None:
                        for i in range(GRID_WIDTH - 1 - col, GRID_WIDTH):
                            for row in range(GRID_HEIGHT - 1, -1, -1):
                                if self.matrix[row][i] is not None:
                                    self.matrix[row][i].counter.x -= 1
                                    self.matrix[row][i], self.matrix[row][i - 1] = self.matrix[row][i - 1], self.matrix[row][i]
                                else:
                                    break
                for i in self.matrix:
                    print(i)
                self._blocks_destroyed -= len(blob)
                if self._blocks_destroyed >= self.LIMIT:
                    return 1
        return 0
                
                        

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
