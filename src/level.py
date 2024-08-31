import pygame

from src.utils import *



class Level:

    def __init__(self, screen: pygame.Surface) -> None:
        self.screen = screen
        self.bg = pygame.Surface((WIDTH, HEIGHT))
        self.bg.fill((98, 122, 174))

    def draw(self, cursor_pos: tuple[int, int]) -> None:
        pass