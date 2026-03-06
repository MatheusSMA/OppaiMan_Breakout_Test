import math
import pygame
from breakout.config import constants as C


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

    def update(self, delta_time, paddle_rect):
        if not self.launched:
            self.x = paddle_rect.centerx
            self.y = paddle_rect.top - self.radius
            return

        self.x += self.vx * delta_time * 60
        self.y += self.vy * delta_time * 60

        # expira o efeito de velocidade temporário
        if self.speed_timer > 0:
            self.speed_timer -= delta_time
            if self.speed_timer <= 0:
                self.speed_timer = 0.0
                current_speed = math.sqrt(self.vx ** 2 + self.vy ** 2)
                if current_speed > 0:
                    self.vx = self.vx / current_speed * C.BALL_SPEED
                    self.vy = self.vy / current_speed * C.BALL_SPEED
                self.speed_state = "normal"

        # mantém a bola dentro das bordas laterais do campo
        if self.x - self.radius <= C.PLAY_BORDER:
            self.x  = C.PLAY_BORDER + self.radius
            self.vx = abs(self.vx)
        elif self.x + self.radius >= C.WIDTH - C.PLAY_BORDER:
            self.x  = C.WIDTH - C.PLAY_BORDER - self.radius
            self.vx = -abs(self.vx)

        # mantém a bola dentro do teto do campo
        if self.y - self.radius <= C.PLAY_BORDER:
            self.y  = C.PLAY_BORDER + self.radius
            self.vy = abs(self.vy)
