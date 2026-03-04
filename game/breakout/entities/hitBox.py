import pygame
from breakout import constants as C

class HitBox:
    def __init__(self):
        self.rect = pygame.Rect(0, 0, 50, 50)
        x = C.WIDTH // 2
        y = C.HEIGHT // 2
        self.rect.center = (x, y)

       
       