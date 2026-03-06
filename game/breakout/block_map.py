from breakout import constants as C
from breakout.entities.block import Block


class BlockMap:
    def __init__(self, grid, powerup_map=None, block_class_map=None, dialogue_manager=None):
        self.blocks          = []
        self.powerups        = []
        self.dialogue_manager = dialogue_manager
        powerup_map     = powerup_map or {}
        block_class_map = block_class_map or {}

        for row_i, row in enumerate(grid):
            for col_i, cell in enumerate(row):
                if cell == 0:
                    continue
                x   = C.BLOCK_OFFSET_X + col_i * (C.BLOCK_W + C.BLOCK_GAP)
                y   = C.BLOCK_OFFSET_Y + row_i * (C.BLOCK_H + C.BLOCK_GAP)
                pt  = powerup_map.get(cell)
                cls = block_class_map.get(cell, Block)

                # DialogueTriggerBlock sentinels (legacy, not used in current maps)
                if isinstance(cls, tuple) and cls[0] == "trigger":
                    from breakout.entities.dialogue_trigger_block import DialogueTriggerBlock
                    trigger_id = cls[1]
                    self.blocks.append(
                        DialogueTriggerBlock(x, y, C.BLOCK_W, C.BLOCK_H,
                                             trigger_id, dialogue_manager, pt)
                    )
                elif cls is Block:
                    half_h = C.BLOCK_H // 2
                    self.blocks.append(cls(x, y,          C.BLOCK_W, half_h, pt))
                    self.blocks.append(cls(x, y + half_h, C.BLOCK_W, half_h, None))
                else:
                    self.blocks.append(cls(x, y, C.BLOCK_W, C.BLOCK_H, pt))

    POINTS_PER_BLOCK = 10

    def check_collisions(self, balls):
        points = 0
        for block in self.blocks:
            if not block.active:
                continue
            for ball in balls:
                spawned = block.check_collision(ball)
                if spawned:
                    self.powerups.append(spawned)
                if not block.active:
                    points += self.POINTS_PER_BLOCK
                    break
        return points

    def check_bullet_collisions(self, bullets):
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
                    points += self.POINTS_PER_BLOCK
                    break
        return points

    def update_powerups(self, dt, paddle, balls):
        for p in self.powerups:
            p.update(dt)
            if p.check_collect(paddle):
                p.apply(paddle, balls)
        self.powerups = [p for p in self.powerups if p.active]

    def draw(self, canvas, scale_x, scale_y, color):
        for block in self.blocks:
            if not block.active:
                continue
            b  = block.rect
            bx = int(b.x      * scale_x)
            by = int(b.y      * scale_y)
            bw = int(b.width  * scale_x)
            bh = int(b.height * scale_y)
            canvas.rect(color, (bx, by, bw, bh))

    def draw_powerups(self, canvas, scale_x, scale_y, color):
        for p in self.powerups:
            px = int(p.x    * scale_x)
            py = int(p.y    * scale_y)
            pr = int(p.SIZE * min(scale_x, scale_y))
            canvas.circle(color, (px, py), pr)
