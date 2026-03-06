import math
from breakout import constants as C
from breakout.entities.powerups.powerup_base import PowerUp


class SlowBall(PowerUp):
    """Desacelera todas as bolas (mín 0.5× a velocidade base) por 10 segundos."""
    TIER     = "positive"
    DURATION = 10.0

    def apply(self, paddle, balls):
        for ball in balls:
            current_speed = math.sqrt(ball.vx ** 2 + ball.vy ** 2)
            if current_speed == 0:
                continue
            new_speed        = max(current_speed * 0.6, C.BALL_SPEED * 0.5)
            ball.vx          = ball.vx / current_speed * new_speed
            ball.vy          = ball.vy / current_speed * new_speed
            ball.speed_state = "slow"
            ball.speed_timer = self.DURATION
