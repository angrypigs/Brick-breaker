import pygame

from src.utils import *



class Brick:

    def __init__(self, screen: pygame.Surface,
                 index: int,
                 pos: tuple[int, int]) -> None:
        self.screen = screen
        self.index = index
        self.counter = pygame.math.Vector2(0, 0)
        self.limit = pygame.math.Vector2(0, 0)
        self.velocity = pygame.math.Vector2(0, 0)
        
        self.coords = pygame.math.Vector2(
            X_OFFSET + BRICK_GAP * (pos[0] + 1) + BRICK_SIZE * pos[0],
            Y_OFFSET + BRICK_GAP * (pos[1] + 1) + BRICK_SIZE * pos[1],
        )
        self._anim = False

    def __bool__(self) -> bool:
        return self._anim
    
    def __str__(self) -> str:
        return f"Brick | coords: {self.coords[0]} {self.coords[1]} | index: {self.index}"

    def __repr__(self) -> str:
        return f"_{self.index}__"
    
    def draw(self) -> None:
        pygame.draw.rect(self.screen, COLORS[self.index], (self.coords, (BRICK_SIZE, BRICK_SIZE)), border_radius=5)
        if (self.counter.x != 0 or self.counter.y > 0) and not self._anim:
            self.__start_falling()
        if self._anim:
            if self.limit.y - self.coords.y < 8:
                self.coords.y = self.limit.y
                self.counter.y = 0
                self.velocity.y = 0
            else:
                self.coords.y += self.velocity.y
                self.velocity.y += 0.981 * 3
            if self.counter.y == 0:
                if abs(self.limit.x - self.coords.x) < 8:
                    self.coords.x = self.limit.x
                    self.counter.x = 0
                    self.velocity.x = 0
                    self._anim = False
                else:
                    self.coords.x += self.velocity.x
                    self.velocity.x += 0.981 * 3 * (-1 if self.counter.x < 0 else 1)

    
    def __start_falling(self) -> None:
        print(self.counter)
        self._anim = True
        self.limit.y = self.coords.y + (BRICK_GAP + BRICK_SIZE) * self.counter.y
        self.limit.x = self.coords.x + (BRICK_GAP + BRICK_SIZE) * self.counter.x

