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
        r         = paddle.rect
        closest_x = max(r.left, min(self.x, r.right))
        closest_y = max(r.top,  min(self.y, r.bottom))
        dist_sq   = (self.x - closest_x) ** 2 + (self.y - closest_y) ** 2
        if dist_sq <= self.SIZE ** 2:
            self.active = False
            return True
        return False

    @abstractmethod
    def apply(self, paddle, balls):
        """Efeito do powerup. balls é a lista viva de bolas do jogo."""
        ...


# --- powerups concretos ---

class WidenPaddle(PowerUp):
    """Alarga a raquete (sobe um nível de tamanho)."""
    TIER = "positive"
    def apply(self, paddle, balls):
        paddle.size_idx   = min(paddle.size_idx + 1, len(C.PADDLE_SIZES) - 1)
        paddle.rect.width = C.PADDLE_SIZES[paddle.size_idx]
        paddle.rect.left  = max(0, paddle.rect.left)
        paddle.rect.right = min(C.WIDTH, paddle.rect.right)


class ShrinkPaddle(PowerUp):
    """Encolhe a raquete (desce um nível de tamanho)."""
    TIER = "negative"
    def apply(self, paddle, balls):
        paddle.size_idx   = max(paddle.size_idx - 1, 0)
        paddle.rect.width = C.PADDLE_SIZES[paddle.size_idx]
        paddle.rect.left  = max(0, paddle.rect.left)
        paddle.rect.right = min(C.WIDTH, paddle.rect.right)


class SpeedBall(PowerUp):
    """Acelera todas as bolas (máx 3× a velocidade base) por 10 segundos."""
    TIER     = "negative"
    DURATION = 10.0

    def apply(self, paddle, balls):
        for ball in balls:
            speed = math.sqrt(ball.vx ** 2 + ball.vy ** 2)
            if speed == 0:
                continue
            new_speed        = min(speed * 1.4, C.BALL_SPEED * 3)
            ball.vx          = ball.vx / speed * new_speed
            ball.vy          = ball.vy / speed * new_speed
            ball.speed_state = "fast"
            ball.speed_timer = self.DURATION


class SlowBall(PowerUp):
    """Desacelera todas as bolas (mín 0.5× a velocidade base) por 10 segundos."""
    TIER     = "positive"
    DURATION = 10.0

    def apply(self, paddle, balls):
        for ball in balls:
            speed = math.sqrt(ball.vx ** 2 + ball.vy ** 2)
            if speed == 0:
                continue
            new_speed        = max(speed * 0.6, C.BALL_SPEED * 0.5)
            ball.vx          = ball.vx / speed * new_speed
            ball.vy          = ball.vy / speed * new_speed
            ball.speed_state = "slow"
            ball.speed_timer = self.DURATION


class Shooter(PowerUp):
    """Ativa metralhadora: ESPAÇO dispara balas dos dois lados por 12 segundos."""
    TIER     = "special"
    DURATION = 12.0

    def apply(self, paddle, balls):
        paddle.shooter_active  = True
        paddle.shots_remaining = 8
        paddle.fire_cooldown   = 0.0


class MultiBall(PowerUp):
    """Clona a primeira bola em mais 2, com ângulos deslocados."""
    TIER = "positive"
    def apply(self, paddle, balls):
        from breakout.entities.ball import Ball  # import local evita circular
        if not balls:
            return
        ref   = balls[0]
        speed = math.sqrt(ref.vx ** 2 + ref.vy ** 2)
        if speed == 0:
            return
        for offset in [-30, 30]:
            b           = Ball()
            b.x         = ref.x
            b.y         = ref.y
            b.launched  = True
            b.ball_type = "clone"
            rad        = math.radians(offset)
            b.vx       = ref.vx * math.cos(rad) - ref.vy * math.sin(rad)
            b.vy       = ref.vx * math.sin(rad) + ref.vy * math.cos(rad)
            balls.append(b)
