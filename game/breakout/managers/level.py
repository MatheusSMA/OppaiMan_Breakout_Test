import math
import pygame
from breakout import constants as C
from breakout.entities.core.bricks.block import Block
from breakout.entities.core.bricks.tough_block import ToughBlock
from breakout.entities.powerups import WidenPaddle, ShrinkPaddle, SpeedBall, SlowBall, MultiBall, Shooter


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
    [1, 1, 1, 1, 8, 8, 1, 1, 6, 1],
    [1, 2, 1, 5, 1, 1, 6, 1, 3, 1],
    [0, 1, 1, 6, 7, 1, 1, 1, 1, 0],
    [0, 0, 4, 8, 1, 1, 8, 4, 0, 0],
    [0, 0, 0, 1, 1, 1, 1, 0, 0, 0],
]

MAP_2 = [
    [8, 1, 6, 1, 8, 8, 1, 1, 1, 8],
    [1, 2, 8, 5, 1, 1, 6, 8, 3, 1],
    [0, 1, 1, 8, 7, 1, 8, 1, 1, 0],
    [0, 8, 4, 8, 1, 1, 8, 4, 8, 0],
    [0, 0, 1, 1, 1, 1, 1, 1, 0, 0],
    [0, 0, 0, 1, 8, 1, 1, 7, 0, 0],
]


POINTS_PER_BLOCK = 10


class LevelManager:
    """Responsavel por construir e gerenciar os blocos de uma fase."""

    def __init__(self, phase=1):
        self.powerups = []
        grid = MAP_1 if phase == 1 else MAP_2
        self.blocks = self._build_blocks(grid)

    def _build_blocks(self, grid):
        blocks = []
        for row_index, row in enumerate(grid):
            for col_index, cell in enumerate(row):
                if cell == 0:
                    continue
                block_x = C.BLOCK_OFFSET_X + col_index * (C.BLOCK_W + C.BLOCK_GAP)
                block_y = C.BLOCK_OFFSET_Y + row_index * (C.BLOCK_H + C.BLOCK_GAP)
                powerup_type = POWERUP_MAP.get(cell)
                block_class = BLOCK_CLASS_MAP.get(cell, Block)
                blocks.append(block_class(block_x, block_y, C.BLOCK_W, C.BLOCK_H, powerup_type))
        return blocks

    def check_collisions(self, balls):
        """Checa colisao bola-bloco. Retorna pontos e spawn de powerups."""
        points = 0
        # cada bola so muda direcao uma vez por frame
        bounced_this_frame = set()
        for block in self.blocks:
            if not block.active:
                continue
            for ball in balls:
                already_bounced = ball in bounced_this_frame
                spawned = block.check_collision(ball, suppress_bounce=already_bounced)
                if spawned:
                    self.powerups.append(spawned)
                if not block.active:
                    points += POINTS_PER_BLOCK
                    bounced_this_frame.add(ball)
                    break
        return points

    def check_bullet_collisions(self, bullets):
        """Checa colisao bala-bloco. Retorna pontos e spawn de powerups."""
        points = 0
        for block in self.blocks:
            if not block.active:
                continue
            for bullet in bullets:
                if not bullet.active:
                    continue
                spawned = block.check_bullet_hit(bullet)
                if spawned:
                    self.powerups.append(spawned)
                if not block.active:
                    points += POINTS_PER_BLOCK
                    break
        return points

    @property
    def all_destroyed(self):
        """True quando todos os blocos estao inativos."""
        return all(not b.active for b in self.blocks)

    @property
    def destruction_ratio(self):
        """Fracao de blocos destruidos (0.0 a 1.0)."""
        total = len(self.blocks)
        if total == 0:
            return 0.0
        destroyed = sum(1 for b in self.blocks if not b.active)
        return destroyed / total
