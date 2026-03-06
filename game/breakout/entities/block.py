import math
import pygame


class Block:
    def __init__(self, x, y, w, h, powerup_type=None):
        self.rect         = pygame.Rect(x, y, w, h)
        self.active       = True
        self.powerup_type = powerup_type  # classe do powerup (não instância)

    def check_collision(self, ball):
        """Retorna uma instância de PowerUp se o bloco foi destruído com um, senão None."""
        if not self.active:
            return None
        
        ball_rect = pygame.Rect(
            ball.x - ball.radius, ball.y - ball.radius,
            ball.radius * 2,      ball.radius * 2
        )
        if not self.rect.colliderect(ball_rect):
            return None
        
        closest_x = max(self.rect.left, min(ball.x, self.rect.right))
        closest_y = max(self.rect.top,  min(ball.y, self.rect.bottom))
        dist = math.sqrt((ball.x - closest_x) ** 2 + (ball.y - closest_y) ** 2)

        if dist >= ball.radius:
            return None

        self.active = False

        overlap_x = (ball.radius + self.rect.width  / 2) - abs(ball.x - self.rect.centerx)
        overlap_y = (ball.radius + self.rect.height / 2) - abs(ball.y - self.rect.centery)

        if overlap_x < overlap_y:
            ball.vx = -ball.vx
        else:
            ball.vy = -ball.vy

        if self.powerup_type:
            return self.powerup_type(self.rect.centerx, self.rect.centery)
        return None

    def check_bullet_hit(self, bullet):
        """Bala destrói o bloco sem ricochetear. Retorna PowerUp ou None."""
        if not self.active or not bullet.active:
            return None
        b_rect = pygame.Rect(
            bullet.x - bullet.radius, bullet.y - bullet.radius,
            bullet.radius * 2,        bullet.radius * 2
        )
        if not self.rect.colliderect(b_rect):
            return None
        self.active   = False
        bullet.active = False
        if self.powerup_type:
            return self.powerup_type(self.rect.centerx, self.rect.centery)
        return None
