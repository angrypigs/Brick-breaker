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