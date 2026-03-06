import renpy
from breakout import constants as C


_SHEET                 = "images/gameplay/BreakOut Assets x2.png"
_POWERUP_SHEET         = "images/gameplay/powerUps.png"
_SPECIAL_POWERUP_SHEET = "images/gameplay/specialPowerUp.png"
_BALL_SHEET            = "images/gameplay/Ball Assets.png"

_BLOCK_ANIM_XS  = [0, 32, 64, 96, 128, 160]
_BLOCK_COLOR_YS = [0, 16, 32, 48, 64, 80]

_TOUGH_STATE_XS = [448, 512, 576, 640]
_TOUGH_SPRITE_Y = 0

_POWERUP_ANIM_XS  = [0, 32, 64, 96, 128, 160]
_POWERUP_TIER_Y   = {"positive": 0, "negative": 32}
_SPECIAL_FRAME_H  = 32

_BALL_SPRITES = {
    "normal": ( 0,  0, 16, 16),
    "fast":   ( 0, 32, 16, 16),
    "slow":   (16, 64, 16, 16),
    "clone":  (16,  0, 16, 16),
}

_PADDLE_FLAT_Y        = 400
_PADDLE_FLAT_H        = 16
_PADDLE_SHOOTER_Y     = 368
_PADDLE_SHOOTER_H     = 32
_PADDLE_SIZE_SPRITES  = [(0, 32), (40, 48), (96, 64), (168, 80), (256, 96)]


class BreakoutRenderer:

    def render_frame(self, target, canvas, game, scale_x, scale_y,
                     st, at, anim_frame=0, powerup_frame=0):
        self._draw_paddle(target, game.paddle, scale_x, scale_y, st, at)
        self._draw_blocks(target, game.level_mgr.blocks, scale_x, scale_y, st, at, anim_frame)
        self._draw_powerups(target, game.level_mgr.powerups, scale_x, scale_y, st, at, powerup_frame)
        self._draw_bullets(target, canvas, game.bullets, scale_x, scale_y)
        self._draw_balls(target, game.balls, scale_x, scale_y, st, at)

    def _draw_paddle(self, target, paddle, scale_x, scale_y, st, at):
        rect          = paddle.rect
        paddle_x      = int(rect.x      * scale_x)
        paddle_y      = int(rect.y      * scale_y)
        paddle_width  = int(rect.width  * scale_x)
        paddle_height = int(rect.height * scale_y)
        source_x, source_width = _PADDLE_SIZE_SPRITES[paddle.size_idx]
        if paddle.shooter_active:
            drawn_height = int(paddle_width * _PADDLE_SHOOTER_H / source_width)
            drawn_y      = paddle_y + paddle_height - drawn_height
            self._blit(target, source_x, _PADDLE_SHOOTER_Y, source_width, _PADDLE_SHOOTER_H,
                       paddle_x, drawn_y, paddle_width, drawn_height, st, at)
        else:
            self._blit(target, source_x, _PADDLE_FLAT_Y, source_width, _PADDLE_FLAT_H,
                       paddle_x, paddle_y, paddle_width, paddle_height, st, at)

    def _draw_blocks(self, target, blocks, scale_x, scale_y, st, at, anim_frame):
        for block in blocks:
            if not block.active:
                continue
            rect         = block.rect
            block_x      = int(rect.x      * scale_x)
            block_y      = int(rect.y      * scale_y)
            block_width  = int(rect.width  * scale_x)
            block_height = int(rect.height * scale_y)
            self._draw_single_block(target, block, block_x, block_y, block_width, block_height, st, at, anim_frame)

    def _draw_single_block(self, target, block, block_x, block_y, block_width, block_height, st, at, anim_frame):
        damage = block.damage_stage
        if damage is not None:
            source_x = _TOUGH_STATE_XS[min(damage, len(_TOUGH_STATE_XS) - 1)]
            self._blit(target, source_x, _TOUGH_SPRITE_Y, 64, 32, block_x, block_y, block_width, block_height, st, at)
        else:
            row     = int((block.rect.y - C.BLOCK_OFFSET_Y) // (C.BLOCK_H + C.BLOCK_GAP))
            frame_x = _BLOCK_ANIM_XS[anim_frame]
            color_y = _BLOCK_COLOR_YS[row % len(_BLOCK_COLOR_YS)]
            self._blit(target, frame_x, color_y, 32, 16, block_x, block_y, block_width, block_height, st, at)

    def _draw_powerups(self, target, powerups, scale_x, scale_y, st, at, powerup_frame):
        for powerup in powerups:
            powerup_x    = int(powerup.x    * scale_x)
            powerup_y    = int(powerup.y    * scale_y)
            display_size = int(powerup.SIZE * 4 * min(scale_x, scale_y))
            tier         = getattr(powerup, "TIER", "positive")
            half         = display_size // 2
            if tier == "special":
                frame_y = (powerup_frame % 2) * _SPECIAL_FRAME_H
                self._blit(target, 0, frame_y, 32, _SPECIAL_FRAME_H,
                           powerup_x - half, powerup_y - half, display_size, display_size,
                           st, at, sheet=_SPECIAL_POWERUP_SHEET)
            else:
                frame_x  = _POWERUP_ANIM_XS[powerup_frame]
                source_y = _POWERUP_TIER_Y.get(tier, 0)
                self._blit(target, frame_x, source_y, 32, 32,
                           powerup_x - half, powerup_y - half, display_size, display_size,
                           st, at, sheet=_POWERUP_SHEET)

    def _draw_bullets(self, target, canvas, bullets, scale_x, scale_y):
        accent = renpy.store.gui.accent_color
        for bullet in bullets:
            bullet_x      = int(bullet.x      * scale_x)
            bullet_y      = int(bullet.y      * scale_y)
            bullet_radius = max(int(bullet.radius * min(scale_x, scale_y)), 2)
            canvas.circle(accent, (bullet_x, bullet_y), bullet_radius)

    def _draw_balls(self, target, balls, scale_x, scale_y, st, at):
        for ball in balls:
            ball_x      = int(ball.x      * scale_x)
            ball_y      = int(ball.y      * scale_y)
            ball_radius = int(ball.radius * min(scale_x, scale_y))
            sprite_key  = self._ball_sprite_key(ball)
            source_x, source_y, source_width, source_height = _BALL_SPRITES.get(sprite_key, _BALL_SPRITES["normal"])
            self._blit(target, source_x, source_y, source_width, source_height,
                       ball_x - ball_radius, ball_y - ball_radius, ball_radius * 2, ball_radius * 2,
                       st, at, sheet=_BALL_SHEET)

    def _ball_sprite_key(self, ball):
        if getattr(ball, "ball_type", "normal") == "clone":
            return "clone"
        return getattr(ball, "speed_state", "normal")

    def _blit(self, target, source_x, source_y, source_width, source_height,
              dest_x, dest_y, dest_width, dest_height, st, at, sheet=None):
        Transform   = renpy.store.Transform
        displayable = Transform(sheet or _SHEET,
                                crop=(source_x, source_y, source_width, source_height),
                                xysize=(dest_width, dest_height))
        rendered = renpy.display.render.render(displayable, dest_width, dest_height, st, at)
        target.blit(rendered, (dest_x, dest_y))
