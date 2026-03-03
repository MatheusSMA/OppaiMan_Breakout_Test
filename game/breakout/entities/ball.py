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
        self.vx       = C.BALL_VEL_X
        self.vy       = C.BALL_VEL_Y
        self.launched = True

    def update(self, dt, paddle_rect):
        if not self.launched:
            # segue o centro do paddle
            self.x = paddle_rect.centerx
            self.y = paddle_rect.top - self.radius
            return

        self.vy += dt
        self.x  += self.vx * dt * 60
        self.y  += self.vy * dt * 60

        # paredes laterais
        if self.x - self.radius <= 0:
            self.x  = self.radius
            self.vx = abs(self.vx)
        elif self.x + self.radius >= C.WIDTH:
            self.x  = C.WIDTH - self.radius
            self.vx = -abs(self.vx)

        # teto
        if self.y - self.radius <= 0:
            self.y  = self.radius
            self.vy = abs(self.vy)
