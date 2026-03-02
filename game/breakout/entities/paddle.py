import pygame
from breakout import constants as C


class Paddle:
    def __init__(self):
        x = (C.WIDTH - C.PADDLE_WIDTH) // 2
        self.rect = pygame.Rect(x, C.PADDLE_Y, C.PADDLE_WIDTH, C.PADDLE_HEIGHT)
    
    def update(self, keys, dt):
        # multiplica por 60 pra manter a velocidade igual independente do fps
        speed = C.PADDLE_SPEED * dt * 60

        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.rect.x -= int(speed)
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.rect.x += int(speed)
        
        # não deixa sair da tela
        self.rect.left  = max(0, self.rect.left)
        self.rect.right = min(C.WIDTH, self.rect.right)

    def draw(self, surface):
        pygame.draw.rect(surface, C.WHITE, self.rect)
        pygame.draw.rect(surface, C.WHITE, self.rect, 1)
