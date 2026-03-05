import math
from abc import ABC, abstractmethod
from breakout import constants as C


class PowerUp(ABC):
    SIZE = 12  # raio do círculo que cai

    def __init__(self, x, y):
        self.x      = float(x)
        self.y      = float(y)
        self.vy     = 3       # velocidade de queda (px/frame a 60fps)
        self.active = True

    def update(self, dt):
        self.y += self.vy * dt * 60
        if self.y - self.SIZE > C.HEIGHT:
            self.active = False

    def check_collect(self, paddle):
        if not self.active:
            return False
        if paddle.rect.collidepoint(self.x, self.y + self.SIZE):
            self.active = False
            return True
        return False

    @abstractmethod
    def apply(self, paddle, balls):
        """Efeito do powerup. balls é a lista viva de bolas do jogo."""
        ...


# --- powerups concretos ---

class WidenPaddle(PowerUp):
    """Alarga a raquete."""
    def apply(self, paddle, balls):
        paddle.rect.width = min(paddle.rect.width + 40, 250)
        paddle.rect.left  = max(0, paddle.rect.left)
        paddle.rect.right = min(C.WIDTH, paddle.rect.right)


class ShrinkPaddle(PowerUp):
    """Encolhe a raquete."""
    def apply(self, paddle, balls):
        paddle.rect.width = max(paddle.rect.width - 40, 50)
        paddle.rect.left  = max(0, paddle.rect.left)
        paddle.rect.right = min(C.WIDTH, paddle.rect.right)


class SpeedBall(PowerUp):
    """Acelera todas as bolas (máx 3× a velocidade base)."""
    def apply(self, paddle, balls):
        for ball in balls:
            speed = math.sqrt(ball.vx ** 2 + ball.vy ** 2)
            if speed == 0:
                continue
            new_speed = min(speed * 1.4, C.BALL_SPEED * 3)
            ball.vx   = ball.vx / speed * new_speed
            ball.vy   = ball.vy / speed * new_speed


class SlowBall(PowerUp):
    """Desacelera todas as bolas (mín 0.5× a velocidade base)."""
    def apply(self, paddle, balls):
        for ball in balls:
            speed = math.sqrt(ball.vx ** 2 + ball.vy ** 2)
            if speed == 0:
                continue
            new_speed = max(speed * 0.6, C.BALL_SPEED * 0.5)
            ball.vx   = ball.vx / speed * new_speed
            ball.vy   = ball.vy / speed * new_speed


class MultiBall(PowerUp):
    """Clona a primeira bola em mais 2, com ângulos deslocados."""
    def apply(self, paddle, balls):
        from breakout.entities.ball import Ball  # import local evita circular
        if not balls:
            return
        ref   = balls[0]
        speed = math.sqrt(ref.vx ** 2 + ref.vy ** 2)
        if speed == 0:
            return
        for offset in [-30, 30]:
            b          = Ball()
            b.x        = ref.x
            b.y        = ref.y
            b.launched = True
            rad        = math.radians(offset)
            b.vx       = ref.vx * math.cos(rad) - ref.vy * math.sin(rad)
            b.vy       = ref.vx * math.sin(rad) + ref.vy * math.cos(rad)
            balls.append(b)
