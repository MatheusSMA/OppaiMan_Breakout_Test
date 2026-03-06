from breakout.entities.powerups.powerup_base import PowerUp


class Shooter(PowerUp):
    """Ativa metralhadora: ESPAÇO dispara balas dos dois lados por 12 segundos."""
    TIER     = "special"
    DURATION = 12.0

    def apply(self, paddle, balls):
        paddle.shooter_active  = True
        paddle.shots_remaining = 8
        paddle.fire_cooldown   = 0.0
