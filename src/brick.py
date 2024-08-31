import pygame

from src.utils import *



class Brick:

    def __init__(self, screen: pygame.Surface,
                 index: int,
                 pos: tuple[int, int]) -> None:
        self.screen = screen
        self.texture = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        pygame.draw.rect(self.texture, COLORS[index], width=3, border_radius=5)
        self.coords = pygame.math.Vector2(
            X_OFFSET + BRICK_GAP * (pos[0] + 1) + BRICK_SIZE * pos[0],
            Y_OFFSET + BRICK_GAP * (pos[1] + 1) + BRICK_SIZE * pos[1],
        )
        self._anim = False

    def __bool__(self) -> bool:
        return self._anim
    
    def draw(self) -> None:
        self.screen.blit(self.texture, self.coords)
        