import pygame

import random

from src.utils import *
from src.brick import Brick



class Level:

    def __init__(self, screen: pygame.Surface, lvl: int) -> None:
        self.screen = screen
        self.bg = pygame.Surface((WIDTH, HEIGHT))
        self.LIMIT = 120 + 10 * (lvl % 5) if lvl < len(COLORS) * 5 else 160
        self.lvl = lvl
        self._blocks_destroyed = 0
        self.matrix : list[list[Brick | None]] = [[Brick(self.screen, random.randint(1, min(lvl // 5 + 3, len(COLORS) - 1)), (y, x))
                                                   for y in range(GRID_WIDTH)] for x in range(GRID_HEIGHT)]
        self.fonts = {36: pygame.font.Font(None, 36), 48: pygame.font.Font(None, 48), 72: pygame.font.Font(None, 72)}
        self.texts = {"points": self.fonts[48].render(f"0 / {self.LIMIT}", 1, FONT_COLOR)}
        self.text_positions = {"points": (Y_OFFSET + 180 - self.texts["points"].get_rect().width // 2,
                                          Y_OFFSET + 80 - self.texts["points"].get_rect().height // 2)}
        self.__draw_bg()

    def __bool__(self) -> bool:
        return all([x is None or x for y in self.matrix for x in y])
        
    def draw(self, cursor_pos: tuple[int, int]) -> None:
        self.screen.blit(self.bg, (0, 0))
        self.screen.blit(self.texts["points"], self.text_positions["points"])
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
                self._blocks_destroyed += len(blob)
                self.texts["points"] = self.fonts[48].render(f"{self._blocks_destroyed} / {self.LIMIT}", 1, FONT_COLOR)
                self.text_positions["points"] = (Y_OFFSET + 180 - self.texts["points"].get_rect().width // 2,
                                                Y_OFFSET + 80 - self.texts["points"].get_rect().height // 2)
                if self._blocks_destroyed >= self.LIMIT:
                    return 1
        return 0
                
                        

    def dfs_board(self, row: int, col: int, visited: list[list[bool]], 
                  target: int) -> list[tuple[int, int]]:
        """
        Recursive function to collect all coords of a 'blob' of color from a given cell
        """
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
    
    def __draw_bg(self) -> None:
        """
        Draws all necessary graphics on self.bg
        """
        self.bg.fill((30, 54, 102))

        # main rectangles

        pygame.draw.rect(self.bg, (18, 36, 72), (X_OFFSET, Y_OFFSET, 
            GRID_WIDTH * (BRICK_GAP + BRICK_SIZE) + BRICK_GAP, 
            GRID_HEIGHT * (BRICK_GAP + BRICK_SIZE) + BRICK_GAP
        ), border_radius=5)
        pygame.draw.rect(self.bg, (18, 36, 72), (
            Y_OFFSET, Y_OFFSET, 360, GRID_HEIGHT * (BRICK_GAP + BRICK_SIZE) + BRICK_GAP
        ), border_radius=5)

        # menu sectors

        pygame.draw.rect(self.bg, (14, 27, 54), (
            Y_OFFSET + 30, Y_OFFSET + 30, 300, 300
        ), border_radius=5)
        pygame.draw.rect(self.bg, (14, 27, 54), (
            Y_OFFSET + 30, Y_OFFSET + 360, 300, 290
        ), border_radius=5)
        pygame.draw.rect(self.bg, (14, 27, 54), (
            Y_OFFSET + 30, Y_OFFSET + 680, 300, 200
        ), border_radius=5)


