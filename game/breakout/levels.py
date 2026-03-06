from breakout.entities.powerup    import WidenPaddle, ShrinkPaddle, SpeedBall, SlowBall, MultiBall, Shooter
from breakout.entities.tough_block import ToughBlock

# 0  = vazio
# 1  = bloco normal
# 2  = WidenPaddle  (alarga a barra)
# 3  = SlowBall     (desacelera as bolas)
# 4  = ShrinkPaddle (encolhe a barra)
# 5  = SpeedBall    (acelera as bolas)
# 6  = MultiBall    (clona a bola em +2)
# 7  = Shooter      (metralhadora)
# 8  = ToughBlock   (resistente, 4 acertos)
POWERUP_MAP = {
    2: WidenPaddle,
    3: SlowBall,
    4: ShrinkPaddle,
    5: SpeedBall,
    6: MultiBall,
    7: Shooter,
}

BLOCK_CLASS_MAP = {
    8: ToughBlock,
}

MAP_1 = [
    [1, 1, 1, 1, 8, 8, 1, 1, 1, 1],
    [1, 2, 1, 5, 1, 1, 6, 1, 3, 1],
    [0, 1, 1, 1, 7, 1, 1, 1, 1, 0],
    [0, 0, 4, 8, 1, 1, 8, 4, 0, 0],
    [0, 0, 0, 1, 1, 1, 1, 7, 7, 7],
]

# Phase 2 — harder layout
MAP_2 = [
    [8, 1, 1, 1, 8, 8, 1, 1, 1, 8],
    [1, 2, 8, 5, 1, 1, 6, 8, 3, 1],
    [0, 1, 1, 8, 7, 1, 8, 1, 1, 0],
    [0, 8, 4, 8, 1, 1, 8, 4, 8, 0],
    [0, 0, 1, 1, 1, 1, 1, 1, 0, 0],
    [0, 0, 0, 1, 8, 1, 1, 7, 0, 0],
]
