import math
from breakout.entities.powerups.powerup_base import PowerUp


class MultiBall(PowerUp):
    """Clona a primeira bola em mais 2, com ângulos deslocados."""
    TIER = "positive"

    def apply(self, paddle, balls):
        from breakout.entities.core.ball import Ball  # import local evita circular
        if not balls:
            return
        source_ball  = balls[0]
        source_speed = math.sqrt(source_ball.vx ** 2 + source_ball.vy ** 2)
        if source_speed == 0:
            return
        for angle_offset in [-30, 30]:
            clone           = Ball()
            clone.x         = source_ball.x
            clone.y         = source_ball.y
            clone.launched  = True
            clone.ball_type = "clone"
            radians         = math.radians(angle_offset)
            clone.vx        = source_ball.vx * math.cos(radians) - source_ball.vy * math.sin(radians)
            clone.vy        = source_ball.vx * math.sin(radians) + source_ball.vy * math.cos(radians)
            balls.append(clone)
