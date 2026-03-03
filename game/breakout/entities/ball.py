import pygame
from breakout import constants as C

class Ball:
    def __init__(self):
        self.radius = C.BALL_RADIUS
        self.x = C.WIDTH // 2
        self.y = C.HEIGHT // 2
        self.vx = C.BALL_VEL_X
        self.vy = C.BALL_VEL_Y
    
    def update(self, dt, g):
        self.vy += g * dt  # acelera pra baixo com o tempo
        self.x  += self.vx * dt * 60  # mantém consistência com o paddle
        self.y  += self.vy * dt * 60
