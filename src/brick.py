import pygame

from src.utils import *



class Brick:

    def __init__(self, screen: pygame.Surface,
                 index: int,
                 pos: tuple[int, int]) -> None:
        self.screen = screen
        self.index = index
        self.texture = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        pygame.draw.rect(self.texture, COLORS[index], (0, 0, BRICK_SIZE, BRICK_SIZE), border_radius=5)
        self.coords = pygame.math.Vector2(
            X_OFFSET + BRICK_GAP * (pos[0] + 1) + BRICK_SIZE * pos[0],
            Y_OFFSET + BRICK_GAP * (pos[1] + 1) + BRICK_SIZE * pos[1],
        )
        self._anim = False

    def __bool__(self) -> bool:
        return self._anim
    
    def __str__(self) -> str:
        return f"Brick | coords: {self.coords[0]} {self.coords[1]} | index: {self.index}"
    
    def draw(self) -> None:
        self.screen.blit(self.texture, self.coords)
