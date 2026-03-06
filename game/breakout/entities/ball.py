import math
import pygame
from breakout import constants as C

class Ball:
    def __init__(self):
        self.radius      = C.BALL_RADIUS
        self.x           = C.WIDTH // 2
        self.y           = 0
        self.vx          = 0
        self.vy          = 0
        self.launched    = False
        self.speed_state = "normal"   # "normal" | "fast" | "slow"
        self.speed_timer = 0.0        # segundos restantes do efeito
        self.ball_type   = "normal"   # "normal" | "clone"

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

        # timer de efeito de velocidade
        if self.speed_timer > 0:
            self.speed_timer -= dt
            if self.speed_timer <= 0:
                self.speed_timer = 0.0
                speed = math.sqrt(self.vx ** 2 + self.vy ** 2)
                if speed > 0:
                    self.vx = self.vx / speed * C.BALL_SPEED
                    self.vy = self.vy / speed * C.BALL_SPEED
                self.speed_state = "normal"

        # colisão paredes laterais (respeita borda do GameBG)
        if self.x - self.radius <= C.PLAY_BORDER:
            self.x  = C.PLAY_BORDER + self.radius
            self.vx = abs(self.vx)
        elif self.x + self.radius >= C.WIDTH - C.PLAY_BORDER:
            self.x  = C.WIDTH - C.PLAY_BORDER - self.radius
            self.vx = -abs(self.vx)

        # colisão teto (respeita borda do GameBG)
        if self.y - self.radius <= C.PLAY_BORDER:
            self.y  = C.PLAY_BORDER + self.radius
            self.vy = abs(self.vy)
