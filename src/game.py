import pygame

import sys

from src.utils import *
from src.level import Level



class Game:

    def __init__(self) -> None:
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.font.init()
        pygame.display.set_caption('Brick breaker')
        self.clock = pygame.time.Clock()
        self.menu = Level(self.screen, 10)
        self.game_mode = 1
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    match self.game_mode:
                        case 1:
                            if self.menu:
                                res = self.menu.pressed(event.pos)
                                if res == 1:
                                    print('new game')
                                    self.menu = Level(self.screen, self.menu.lvl + 1)
            self.menu.draw(pygame.mouse.get_pos())
            pygame.display.flip()
            self.clock.tick(FPS)