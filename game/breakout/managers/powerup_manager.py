"""
PowerupManager — gerencia powerups que estão caindo na tela.

Responsabilidade única: atualizar posição, detectar coleta e aplicar efeito.
"""


class PowerupManager:
    """Atualiza, coleta e aplica powerups em queda."""

    def update(self, powerups, delta_time, paddle, balls):
        """Atualiza todos os powerups, coleta os que tocam o paddle e limpa inativos."""
        for powerup in powerups:
            powerup.update(delta_time)
            if powerup.check_collect(paddle):
                powerup.apply(paddle, balls)
        # remove powerups que saíram da tela ou foram coletados
        powerups[:] = [p for p in powerups if p.active]
