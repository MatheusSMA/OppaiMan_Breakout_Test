import math
import pygame
from breakout import constants as C

class Ball:
    def __init__(self):
        self.radius   = C.BALL_RADIUS
        self.x        = C.WIDTH // 2
        self.y        = 0
        self.vx       = 0
        self.vy       = 0
        self.launched = False

    def launch(self):
        angle     = math.radians(C.BALL_LAUNCH_ANGLE)
        self.vx   =  C.BALL_SPEED * math.sin(angle)
        self.vy   = -C.BALL_SPEED * math.cos(angle)  # negativo = subindo
        self.launched = True

    def bounce_paddle(self, paddle):
        hit_pos = (self.x - paddle.rect.centerx) / (paddle.rect.width / 2)
        hit_pos = max(-1.0, min(1.0, hit_pos))

        speed = math.sqrt(self.vx ** 2 + self.vy ** 2)
        angle = hit_pos * 60  # -60° a +60°

        self.vx = speed * math.sin(math.radians(angle))
        self.vy = -speed * math.cos(math.radians(angle))  # sempre sobe

    def update(self, dt, paddle_rect):
        if not self.launched:
            self.x = paddle_rect.centerx
            self.y = paddle_rect.top - self.radius
            return

        self.x += self.vx * dt * 60
        self.y += self.vy * dt * 60

        # colisão paredes laterais
        if self.x - self.radius <= 0:
            self.x  = self.radius
            self.vx = abs(self.vx)
        elif self.x + self.radius >= C.WIDTH:
            self.x  = C.WIDTH - self.radius
            self.vx = -abs(self.vx)

        # colisão teto
        if self.y - self.radius <= 0:
            self.y  = self.radius
            self.vy = abs(self.vy)
