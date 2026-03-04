import math
import pygame
from breakout import constants as C

class HitBox:
    def __init__(self):
        self.rect   = pygame.Rect(0, 0, 50, 50)
        self.rect.center = (C.WIDTH // 2, C.HEIGHT // 2)
        self.active = True
    
    def check_collision(self, ball):
        if not self.active:
            return
        
        # ponto mais próximo do rect ao centro da bola
        closest_x = max(self.rect.left, min(ball.x, self.rect.right))
        closest_y = max(self.rect.top,  min(ball.y, self.rect.bottom))
        dist = math.sqrt((ball.x - closest_x) ** 2 + (ball.y - closest_y) ** 2)

        if dist >= ball.radius:
            return

        self.active = False

        # descobre qual lado foi atingido pelo menor overlap
        overlap_x = (ball.radius + self.rect.width  / 2) - abs(ball.x - self.rect.centerx)
        overlap_y = (ball.radius + self.rect.height / 2) - abs(ball.y - self.rect.centery)

        if overlap_x < overlap_y:
            ball.vx = -ball.vx
        else:
            ball.vy = -ball.vy
