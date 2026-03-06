from .block import Block


class ToughBlock(Block):
    """Bloco resistente: requer 4 acertos para destruir.

    Sprite muda a cada acerto -- estados 0-3 mapeados em renderer.py.
    Herda toda a logica de colisao de Block; so override _on_hit() e damage_stage.
    """
    MAX_HITS = 4

    def __init__(self, x, y, width, height, powerup_type=None):
        super().__init__(x, y, width, height, powerup_type)
        self.hits_remaining = self.MAX_HITS

    def _on_hit(self):
        """Decrementa acertos; destroi apenas quando chegar a zero."""
        self.hits_remaining -= 1
        if self.hits_remaining <= 0:
            return super()._on_hit()
        return None

    @property
    def damage_stage(self):
        """Indice de dano atual (0 = intacto, MAX_HITS-1 = quase destruido)."""
        return self.MAX_HITS - self.hits_remaining
