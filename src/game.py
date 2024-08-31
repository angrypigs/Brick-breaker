import pygame

import sys

from src.utils import *
from src.level import Level



class Game:

    def __init__(self) -> None:
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption('Brick breaker')
        self.clock = pygame.time.Clock()
        self.menu = Level(self.screen)
        self.game_mode = 1
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            self.menu.draw(pygame.mouse.get_pos())
            pygame.display.flip()
            self.clock.tick(FPS)