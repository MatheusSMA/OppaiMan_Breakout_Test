import math
import pygame
from breakout.entities.block import Block


class ToughBlock(Block):
    """Bloco resistente: requer 4 acertos para destruir.

    Sprite muda a cada acerto: estados 0-3 em x=448,480,512,544 (32×32).
    """
    MAX_HITS = 4

    def __init__(self, x, y, w, h, powerup_type=None):
        super().__init__(x, y, w, h, powerup_type)
        self.hits_remaining = self.MAX_HITS

    def _take_hit(self):
        self.hits_remaining -= 1
        if self.hits_remaining <= 0:
            self.active = False
            return True
        return False

    def check_collision(self, ball, suppress_bounce=False):
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

        if not suppress_bounce:
            overlap_x = (ball.radius + self.rect.width  / 2) - abs(ball.x - self.rect.centerx)
            overlap_y = (ball.radius + self.rect.height / 2) - abs(ball.y - self.rect.centery)
            if overlap_x < overlap_y:
                ball.vx = -ball.vx
            else:
                ball.vy = -ball.vy

        destroyed = self._take_hit()
        if destroyed and self.powerup_type:
            return self.powerup_type(self.rect.centerx, self.rect.centery)
        return None

    def check_bullet_hit(self, bullet):
        if not self.active or not bullet.active:
            return None

        b_rect = pygame.Rect(
            bullet.x - bullet.radius, bullet.y - bullet.radius,
            bullet.radius * 2,        bullet.radius * 2
        )
        if not self.rect.colliderect(b_rect):
            return None

        bullet.active = False
        destroyed = self._take_hit()
        if destroyed and self.powerup_type:
            return self.powerup_type(self.rect.centerx, self.rect.centery)
        return None
