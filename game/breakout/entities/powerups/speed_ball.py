import math
from breakout import constants as C
from breakout.entities.powerups.powerup_base import PowerUp


class SpeedBall(PowerUp):
    """Acelera todas as bolas (máx 3× a velocidade base) por 10 segundos."""
    TIER     = "negative"
    DURATION = 10.0

    def apply(self, paddle, balls):
        for ball in balls:
            current_speed = math.sqrt(ball.vx ** 2 + ball.vy ** 2)
            if current_speed == 0:
                continue
            new_speed        = min(current_speed * 1.4, C.BALL_SPEED * 3)
            ball.vx          = ball.vx / current_speed * new_speed
            ball.vy          = ball.vy / current_speed * new_speed
            ball.speed_state = "fast"
            ball.speed_timer = self.DURATION
