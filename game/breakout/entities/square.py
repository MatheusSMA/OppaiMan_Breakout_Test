import pygame
from breakout import constants as C

class Square:
    def __init__(self,size=80):
        self.size = size
        x = (C.WIDTH - size)//2
        y = (C.HEIGHT - size)//2
        self.rect = pygame.Rect(x,y,size, size)
