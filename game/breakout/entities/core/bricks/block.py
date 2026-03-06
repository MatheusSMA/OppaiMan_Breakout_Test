import pygame


class Block:
    def __init__(self, x, y, width, height, powerup_type=None):
        self.rect         = pygame.Rect(x, y, width, height)
        self.active       = True
        self.powerup_type = powerup_type  # classe do powerup, instanciada ao ser coletado

    # ------------------------------------------------------------------
    # Interface pública — usada pelo LevelManager
    # ------------------------------------------------------------------

    def check_collision(self, ball, suppress_bounce=False):
        """Verifica colisão bola-bloco. Retorna PowerUp instanciado ou None."""
        if not self.active or not self._overlaps_ball(ball):
            return None
        if not suppress_bounce:
            self._bounce_ball(ball)
        return self._on_hit()

    def check_bullet_hit(self, bullet):
        """Bala destrói o bloco sem ricochete. Retorna PowerUp ou None."""
        if not self.active or not bullet.active:
            return None
        bullet_rect = pygame.Rect(
            bullet.x - bullet.radius, bullet.y - bullet.radius,
            bullet.radius * 2,        bullet.radius * 2,
        )
        if not self.rect.colliderect(bullet_rect):
            return None
        bullet.active = False
        return self._on_hit()

    # ------------------------------------------------------------------
    # Helpers — subclasses podem sobrescrever apenas _on_hit()
    # ------------------------------------------------------------------

    def _overlaps_ball(self, ball):
        """AABB grosseira + distância exata ao centro do bloco."""
        ball_rect = pygame.Rect(
            ball.x - ball.radius, ball.y - ball.radius,
            ball.radius * 2,      ball.radius * 2,
        )
        if not self.rect.colliderect(ball_rect):
            return False
        closest_x   = max(self.rect.left, min(ball.x, self.rect.right))
        closest_y   = max(self.rect.top,  min(ball.y, self.rect.bottom))
        distance_sq = (ball.x - closest_x) ** 2 + (ball.y - closest_y) ** 2
        return distance_sq < ball.radius ** 2

    def _bounce_ball(self, ball):
        """Reflete a bola no eixo com menor sobreposição (lateral vs topo)."""
        overlap_x = (ball.radius + self.rect.width  / 2) - abs(ball.x - self.rect.centerx)
        overlap_y = (ball.radius + self.rect.height / 2) - abs(ball.y - self.rect.centery)
        if overlap_x < overlap_y:
            ball.vx = -ball.vx
        else:
            ball.vy = -ball.vy

    def _on_hit(self):
        """Destrói o bloco e retorna powerup se houver. Sobrescreva em subclasses."""
        self.active = False
        if self.powerup_type:
            return self.powerup_type(self.rect.centerx, self.rect.centery)
        return None
