import pygame
from breakout.config import constants as C


class Paddle:
    def __init__(self):
        start_x = (C.WIDTH - C.PADDLE_WIDTH) // 2
        self.rect            = pygame.Rect(start_x, C.PADDLE_Y, C.PADDLE_WIDTH, C.PADDLE_HEIGHT)
        self.size_idx        = C.PADDLE_DEFAULT_SIZE_IDX
        self.shooter_active  = False
        self.shots_remaining = 0
        self.fire_cooldown   = 0.0

    def update(self, keys, delta_time):
        # multiplica por 60 pra manter a velocidade igual independente do fps
        frame_speed = C.PADDLE_SPEED * delta_time * 60

        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.rect.x -= int(frame_speed)
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.rect.x += int(frame_speed)

        # nao deixa sair da tela
        self.rect.left  = max(0, self.rect.left)
        self.rect.right = min(C.WIDTH, self.rect.right)

        if self.shooter_active and self.fire_cooldown > 0:
            self.fire_cooldown -= delta_time
