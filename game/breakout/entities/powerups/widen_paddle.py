from breakout import constants as C
from breakout.entities.powerups.powerup_base import PowerUp


class WidenPaddle(PowerUp):
    """Alarga a raquete (sobe um nível de tamanho)."""
    TIER = "positive"

    def apply(self, paddle, balls):
        paddle.size_idx   = min(paddle.size_idx + 1, len(C.PADDLE_SIZES) - 1)
        paddle.rect.width = C.PADDLE_SIZES[paddle.size_idx]
        # reposiciona dentro da tela caso a expansão ultrapasse a borda
        paddle.rect.left  = max(0, paddle.rect.left)
        paddle.rect.right = min(C.WIDTH, paddle.rect.right)
