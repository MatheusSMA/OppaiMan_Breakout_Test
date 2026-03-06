from breakout import constants as C
from breakout.entities.powerups.powerup_base import PowerUp


class ShrinkPaddle(PowerUp):
    """Encolhe a raquete (desce um nível de tamanho)."""
    TIER = "negative"

    def apply(self, paddle, balls):
        paddle.size_idx   = max(paddle.size_idx - 1, 0)
        paddle.rect.width = C.PADDLE_SIZES[paddle.size_idx]
        paddle.rect.left  = max(0, paddle.rect.left)
        paddle.rect.right = min(C.WIDTH, paddle.rect.right)
