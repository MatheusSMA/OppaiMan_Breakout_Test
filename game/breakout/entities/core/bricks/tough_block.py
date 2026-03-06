from .block import Block


class ToughBlock(Block):
    """Bloco resistente: requer 4 acertos para destruir.

    Sprite muda a cada acerto — estados 0-3 mapeados em renderer.py.
    Herda toda a lógica de colisão de Block; só override _on_hit().
    """
    MAX_HITS = 4

    def __init__(self, x, y, width, height, powerup_type=None):
        super().__init__(x, y, width, height, powerup_type)
        self.hits_remaining = self.MAX_HITS

    def _on_hit(self):
        """Decrementa acertos; destrói apenas quando chegar a zero."""
        self.hits_remaining -= 1
        if self.hits_remaining <= 0:
            return super()._on_hit()  # destrói e retorna powerup
        return None  # ainda não destruído
