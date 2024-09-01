import pygame

from src.utils import *



class Brick:

    def __init__(self, screen: pygame.Surface,
                 index: int,
                 pos: tuple[int, int]) -> None:
        self.screen = screen
        self.index = index
        self.texture = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        self.fall_counter = 0
        self.limit = 0
        self.velocity = 0
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
        if self.fall_counter > 0 and not self._anim:
            self.__start_falling()
        if self._anim:
            if self.limit - self.coords.y < 8:
                self.coords.y = self.limit
                self.fall_counter = 0
                self._anim = False
                self.velocity = 0
            else:
                self.coords.y += self.velocity
                self.velocity += 0.981 * 3
    
    def __start_falling(self) -> None:
        self._anim = True
        self.limit = self.coords.y + (BRICK_GAP + BRICK_SIZE) * self.fall_counter

