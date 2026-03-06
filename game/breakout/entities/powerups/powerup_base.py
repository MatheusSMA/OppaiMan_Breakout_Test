from abc import ABC, abstractmethod
from breakout.config import constants as C


class PowerUp(ABC):
    """Base de todos os powerups: cai da tela e é coletado pela raquete."""
    SIZE = 12  # raio do círculo que cai

    def __init__(self, x, y):
        self.x      = float(x)
        self.y      = float(y)
        self.vy     = 3       # velocidade de queda (px/frame a 60fps)
        self.active = True

    def update(self, delta_time):
        self.y += self.vy * delta_time * 60
        if self.y - self.SIZE > C.HEIGHT:
            self.active = False

    def check_collect(self, paddle):
        if not self.active:
            return False
        paddle_rect = paddle.rect
        closest_x   = max(paddle_rect.left, min(self.x, paddle_rect.right))
        closest_y   = max(paddle_rect.top,  min(self.y, paddle_rect.bottom))
        distance_sq = (self.x - closest_x) ** 2 + (self.y - closest_y) ** 2
        if distance_sq <= self.SIZE ** 2:
            self.active = False
            return True
        return False

    @abstractmethod
    def apply(self, paddle, balls):
        """Efeito do powerup ao ser coletado."""
        ...
