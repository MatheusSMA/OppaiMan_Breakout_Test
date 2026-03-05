from breakout.entities.powerup import WidenPaddle, ShrinkPaddle, SpeedBall, SlowBall, MultiBall

# 0 = vazio
# 1 = bloco normal
# 2 = WidenPaddle  (alarga a barra)
# 3 = SlowBall     (desacelera as bolas)
# 4 = ShrinkPaddle (encolhe a barra)
# 5 = SpeedBall    (acelera as bolas)
# 6 = MultiBall    (clona a bola em +2)
POWERUP_MAP = {
    2: WidenPaddle,
    3: SlowBall,
    4: ShrinkPaddle,
    5: SpeedBall,
    6: MultiBall,
}

MAP_1 = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 2, 1, 5, 1, 1, 6, 1, 3, 1],
    [0, 1, 1, 1, 1, 1, 1, 1, 1, 0],
    [0, 0, 4, 1, 1, 1, 1, 4, 0, 0],
    [0, 0, 0, 1, 1, 1, 1, 0, 0, 0],
]
