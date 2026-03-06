"""
CollisionManager — detecta e resolve colisões bola-paddle.

A colisão bola-bloco e bala-bloco fica em LevelManager,
que já é bem isolada. Aqui trata só a interação com o paddle.
"""


class CollisionManager:
    """Resolve colisões entre bolas e o paddle."""

    def check_ball_paddle(self, balls, paddle):
        """Resolve bounce de todas as bolas contra o paddle.

        Detecta se bateu de lado (reflete vx) ou de cima (bounce_paddle).
        """
        for ball in balls:
            if not ball.launched:
                continue
            self._resolve_single(ball, paddle)

    def _resolve_single(self, ball, paddle):
        paddle_rect = paddle.rect
        closest_x   = max(paddle_rect.left,  min(ball.x, paddle_rect.right))
        closest_y   = max(paddle_rect.top,   min(ball.y, paddle_rect.bottom))
        distance_sq = (ball.x - closest_x) ** 2 + (ball.y - closest_y) ** 2

        if distance_sq >= ball.radius ** 2:
            return  # sem colisão

        overlap_x = paddle_rect.width  / 2 + ball.radius - abs(ball.x - paddle_rect.centerx)
        overlap_y = paddle_rect.height / 2 + ball.radius - abs(ball.y - paddle_rect.centery)

        if overlap_x < overlap_y:
            # bateu de lado — empurra e reflete horizontal
            if ball.x < paddle_rect.centerx:
                ball.x  = paddle_rect.left - ball.radius
                ball.vx = -abs(ball.vx)
            else:
                ball.x  = paddle_rect.right + ball.radius
                ball.vx =  abs(ball.vx)
        elif ball.vy > 0:
            # bateu de cima — ângulo baseado em onde na raquete bateu
            ball.bounce_paddle(paddle)
