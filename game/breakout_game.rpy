default paddle_width  = 100
default paddle_height = 15
default breakout_score = 0

init python:
    import pygame
    from breakout import constants as C
    from breakout.entities import Paddle, Ball, Bullet
    from breakout.entities.tough_block import ToughBlock
    from breakout.entities.dialogue_trigger_block import DialogueTriggerBlock
    from breakout.block_map import BlockMap
    from breakout import levels
    from breakout.game_state import GameState
    from breakout.dialogue   import DialogueManager
    from breakout.story      import build_registry

    _SHEET                = "images/BreakOut Assets x2.png"
    _POWERUP_SHEET        = "images/powerUps.png"
    _SPECIAL_POWERUP_SHEET = "images/specialPowerUp.png"

    # Blocos normais — 6 frames de animação, brick 32×16 px
    _BLOCK_ANIM_XS   = [0, 32, 64, 96, 128, 160]
    _BLOCK_COLOR_YS  = [0, 16, 32, 48, 64, 80]
    _BLOCK_ANIM_FPS  = 6

    # ToughBlock — 4 estados de dano
    _TOUGH_STATE_XS  = [448, 512, 576, 640]
    _TOUGH_SPRITE_Y  = 0

    # Powerup — 6 frames animados, 2 linhas: y=0 positivo, y=32 negativo
    _POWERUP_ANIM_XS     = [0, 32, 64, 96, 128, 160]
    _POWERUP_TIER_Y      = {"positive": 0, "negative": 32}
    _POWERUP_ANIM_FPS    = 6
    # Special (Shooter) — 2 frames empilhados verticalmente em specialPowerUp.png
    _SPECIAL_FRAME_H     = 32

    # ball 16×16 — Ball Assets.png: [1,1]=normal, [3,1]=fast, [5,2]=slow, [1,2]=clone
    _BALL_SHEET   = "images/Ball Assets.png"
    _BALL_SPRITES = {
        "normal": ( 0,  0, 16, 16),
        "fast":   ( 0, 32, 16, 16),
        "slow":   (16, 64, 16, 16),
        "clone":  (16,  0, 16, 16),
    }

    # 5 tamanhos de paddle
    _PADDLE_FLAT_Y     = 400
    _PADDLE_FLAT_H     = 16
    _PADDLE_SHOOTER_Y  = 368
    _PADDLE_SHOOTER_H  = 32
    _PADDLE_SIZE_SPRITES = [
        (  0, 32),
        ( 40, 48),
        ( 96, 64),
        (168, 80),
        (256, 96),
    ]

    # ---------------------------------------------------------------
    # Thresholds for milestone dialogues (fraction of blocks destroyed)
    # ---------------------------------------------------------------
    _PART2_THRESHOLD = 0.40   # 40% of phase 1 broken  → part2
    _PART4_THRESHOLD = 0.50   # 50% of phase 2 broken  → part4
    _PART5_THRESHOLD = 0.90   # 90% of phase 2 broken  → part5 (plot twist)

    # ---------------------------------------------------------------
    # Shared game state — single instance shared by the Displayable
    # and the dialogue system.
    # ---------------------------------------------------------------
    _game_state    = GameState()
    _breakout_screen = None   # singleton — preserved across dialogue calls

    def _get_breakout_screen():
        """Return (or create) the singleton BreakoutScreen instance."""
        global _breakout_screen
        if _breakout_screen is None:
            _breakout_screen = BreakoutScreen()
        return _breakout_screen

    def _reset_breakout_screen():
        """Destroy and recreate the singleton for a fresh game."""
        global _breakout_screen
        _breakout_screen = None

    class BreakoutScreen(renpy.Displayable):
        def __init__(self):
            super(BreakoutScreen, self).__init__()

            # Dialogue system
            self._registry = build_registry()
            self._dm       = DialogueManager(_game_state, self._registry)

            self.paddle           = Paddle()
            self.balls            = [Ball()]
            self.bullets          = []

            # Phase 1
            self.map = BlockMap(
                levels.MAP_1,
                levels.POWERUP_MAP,
                levels.BLOCK_CLASS_MAP,
                dialogue_manager=self._dm,
            )

            self.score            = 0
            self.result_triggered = False
            self._end_result      = None
            self._dialogue_requested = False
            self.last_st          = None
            self.anim_timer       = 0.0
            self.anim_frame       = 0
            self.powerup_frame    = 0

            # Enqueue intro — will be picked up on the first render frame
            self._dm.enqueue("intro")

            # Expose the manager to the Ren'Py store so breakout_dialogue_show
            # can call on_sequence_finished() when a sequence ends.
            renpy.store._breakout_dm = self._dm

        # ----------------------------------------------------------
        def _end(self, result):
            if not self.result_triggered:
                self.result_triggered = True
                self._end_result      = result
                pygame.event.post(pygame.event.Event(pygame.USEREVENT))

        def _blit_sprite(self, rv, sx, sy, sw, sh, tx, ty, tw, th, st, at, sheet=None):
            d = Transform(sheet or _SHEET, crop=(sx, sy, sw, sh), xysize=(tw, th))
            r = renpy.render(d, tw, th, st, at)
            rv.blit(r, (tx, ty))

        def _fire_bullets(self):
            r  = self.paddle.rect
            ly = r.y
            self.bullets.append(Bullet(r.left  + 4, ly))
            self.bullets.append(Bullet(r.right - 4, ly))
            self.paddle.fire_cooldown   = 1.0
            self.paddle.shots_remaining -= 1
            if self.paddle.shots_remaining <= 0:
                self.paddle.shooter_active = False

        def _advance_to_phase2(self):
            """Switch to MAP_2 and reset gameplay entities for phase 2."""
            _game_state.phase = 2
            self.map = BlockMap(
                levels.MAP_2,
                levels.POWERUP_MAP,
                levels.BLOCK_CLASS_MAP,
                dialogue_manager=self._dm,
            )
            self.balls              = [Ball()]
            self.bullets            = []
            self.last_st            = None   # reset timer — st reinicia na nova screen call
            self._dialogue_requested = False  # limpa flags residuais da fase anterior
            self.result_triggered   = False
            self._end_result        = None

        def _check_milestones(self):
            """Fire story milestones based on percentage of blocks destroyed."""
            gs           = _game_state
            total        = len(self.map.blocks)
            if total == 0:
                return
            destroyed    = sum(1 for b in self.map.blocks if not b.active)
            pct          = destroyed / total

            if gs.phase == 1:
                if not gs.part2_done and pct >= _PART2_THRESHOLD:
                    gs.part2_done = True
                    self._dm.enqueue("part2")
            else:  # phase 2
                if not gs.part4_done and pct >= _PART4_THRESHOLD:
                    gs.part4_done = True
                    self._dm.enqueue("part4")

        # ----------------------------------------------------------
        def _render_frame(self, width, height, rv, canvas, scale_x, scale_y, st, at):
            # paddle
            p       = self.paddle.rect
            px      = int(p.x      * scale_x)
            py      = int(p.y      * scale_y)
            pw      = int(p.width  * scale_x)
            ph      = int(p.height * scale_y)
            ssx, ssw = _PADDLE_SIZE_SPRITES[self.paddle.size_idx]
            if self.paddle.shooter_active:
                sh_sprite = int(pw * _PADDLE_SHOOTER_H / ssw)
                sy_sprite = py + ph - sh_sprite
                self._blit_sprite(rv, ssx, _PADDLE_SHOOTER_Y, ssw, _PADDLE_SHOOTER_H, px, sy_sprite, pw, sh_sprite, st, at)
            else:
                self._blit_sprite(rv, ssx, _PADDLE_FLAT_Y, ssw, _PADDLE_FLAT_H, px, py, pw, ph, st, at)

            # blocos
            for block in self.map.blocks:
                if not block.active:
                    continue
                b   = block.rect
                bx  = int(b.x      * scale_x)
                by  = int(b.y      * scale_y)
                bw  = int(b.width  * scale_x)
                bh  = int(b.height * scale_y)
                if isinstance(block, ToughBlock):
                    dmg = ToughBlock.MAX_HITS - block.hits_remaining
                    sx  = _TOUGH_STATE_XS[min(dmg, len(_TOUGH_STATE_XS) - 1)]
                    self._blit_sprite(rv, sx, _TOUGH_SPRITE_Y, 64, 32, bx, by, bw, bh, st, at)
                elif isinstance(block, DialogueTriggerBlock):
                    # render as a visually distinct block (color row 5)
                    row = int((b.y - C.BLOCK_OFFSET_Y) // (C.BLOCK_H + C.BLOCK_GAP))
                    sx  = _BLOCK_ANIM_XS[self.anim_frame]
                    sy  = _BLOCK_COLOR_YS[5]   # last color = special
                    self._blit_sprite(rv, sx, sy, 32, 16, bx, by, bw, bh, st, at)
                else:
                    row = int((b.y - C.BLOCK_OFFSET_Y) // (C.BLOCK_H + C.BLOCK_GAP))
                    sx  = _BLOCK_ANIM_XS[self.anim_frame]
                    sy  = _BLOCK_COLOR_YS[row % len(_BLOCK_COLOR_YS)]
                    self._blit_sprite(rv, sx, sy, 32, 16, bx, by, bw, bh, st, at)

            # powerups
            for p in self.map.powerups:
                px   = int(p.x    * scale_x)
                py   = int(p.y    * scale_y)
                psz  = int(p.SIZE * 4 * min(scale_x, scale_y))
                tier = getattr(p, "TIER", "positive")
                if tier == "special":
                    # 2 frames empilhados verticalmente em specialPowerUp.png
                    sfy = (self.powerup_frame % 2) * _SPECIAL_FRAME_H
                    self._blit_sprite(rv, 0, sfy, 32, _SPECIAL_FRAME_H, px - psz // 2, py - psz // 2, psz, psz, st, at, sheet=_SPECIAL_POWERUP_SHEET)
                else:
                    sx  = _POWERUP_ANIM_XS[self.powerup_frame]
                    spy = _POWERUP_TIER_Y.get(tier, 0)
                    self._blit_sprite(rv, sx, spy, 32, 32, px - psz // 2, py - psz // 2, psz, psz, st, at, sheet=_POWERUP_SHEET)

            # balas
            for bullet in self.bullets:
                bx = int(bullet.x      * scale_x)
                by = int(bullet.y      * scale_y)
                br = int(bullet.radius * min(scale_x, scale_y))
                canvas.circle(gui.accent_color, (bx, by), max(br, 2))

            # bolas
            for ball in self.balls:
                bx = int(ball.x      * scale_x)
                by = int(ball.y      * scale_y)
                br = int(ball.radius * min(scale_x, scale_y))
                if getattr(ball, "ball_type", "normal") == "clone":
                    sprite_key = "clone"
                else:
                    sprite_key = getattr(ball, "speed_state", "normal")
                sx, sy, sw, sh = _BALL_SPRITES.get(sprite_key, _BALL_SPRITES["normal"])
                self._blit_sprite(rv, sx, sy, sw, sh, bx - br, by - br, br * 2, br * 2, st, at, sheet=_BALL_SHEET)

        # ----------------------------------------------------------
        def render(self, width, height, st, at):
            dt = (st - self.last_st) if self.last_st is not None else 0.016
            dt = max(0.0, min(dt, 0.05))   # clipa negativos E valores grandes
            self.last_st = st

            scale_x = width  / C.WIDTH
            scale_y = height / C.HEIGHT
            rv      = renpy.Render(width, height)
            bg = Transform("images/GameBG.png", xysize=(width, height))
            rv.blit(renpy.render(bg, width, height, st, at), (0, 0))
            canvas  = rv.canvas()

            # Frozen after a result — keep rendering, event() will return the value
            if self.result_triggered:
                self._render_frame(width, height, rv, canvas, scale_x, scale_y, st, at)
                renpy.redraw(self, 0)
                return rv

            # ---- Tick dialogue queue — may set paused=True ----
            if not _game_state.paused:
                triggered = self._dm.tick()
                if triggered:
                    self._dialogue_requested = True
                    # Reset timer so dt is safe on the first frame after resume
                    self.last_st = None
                    pygame.event.post(pygame.event.Event(pygame.USEREVENT))

            # ---- PAUSED: freeze the frame (sem redraw contínuo) ----
            if _game_state.paused:
                self._render_frame(width, height, rv, canvas, scale_x, scale_y, st, at)
                score_d = Text("Score: " + str(self.score))
                score_r = renpy.render(score_d, width, 60, st, at)
                rv.blit(score_r, (width // 2 - score_r.width // 2, 15))
                renpy.redraw(self, 0.1)
                return rv

            # First frame after unpause — skip physics tick to avoid huge dt
            if self.last_st is None:
                self.last_st = st
                self._render_frame(width, height, rv, canvas, scale_x, scale_y, st, at)
                renpy.redraw(self, 0)
                return rv

            # animation
            self.anim_timer += dt
            if self.anim_timer >= 1.0 / _BLOCK_ANIM_FPS:
                self.anim_timer    = 0.0
                self.anim_frame    = (self.anim_frame    + 1) % len(_BLOCK_ANIM_XS)
                self.powerup_frame = (self.powerup_frame + 1) % len(_POWERUP_ANIM_XS)

            keys = pygame.key.get_pressed()
            self.paddle.update(keys, dt)

            if self.paddle.shooter_active and self.paddle.fire_cooldown <= 0 and self.paddle.shots_remaining > 0:
                if keys[pygame.K_SPACE]:
                    self._fire_bullets()

            for ball in self.balls:
                ball.update(dt, self.paddle.rect)

            for bullet in self.bullets:
                bullet.update(dt)

            # collisions paddle
            for ball in self.balls:
                if not ball.launched:
                    continue
                r         = self.paddle.rect
                bx, by, br = ball.x, ball.y, ball.radius
                closest_x = max(r.left,  min(bx, r.right))
                closest_y = max(r.top,   min(by, r.bottom))
                if (bx - closest_x) ** 2 + (by - closest_y) ** 2 < br * br:
                    # resolve por menor sobreposição: lateral ou topo
                    overlap_x = r.width  / 2 + br - abs(bx - r.centerx)
                    overlap_y = r.height / 2 + br - abs(by - r.centery)
                    if overlap_x < overlap_y:
                        # bateu de lado — empurra e reflete vx
                        if bx < r.centerx:
                            ball.x  = r.left - br
                            ball.vx = -abs(ball.vx)
                        else:
                            ball.x  = r.right + br
                            ball.vx =  abs(ball.vx)
                    elif ball.vy > 0:
                        # bateu de cima — bounce normal
                        ball.bounce_paddle(self.paddle)

            prev_destroyed = _game_state.bricks_destroyed
            points      = self.map.check_collisions(self.balls)
            points     += self.map.check_bullet_collisions(self.bullets)
            new_destroyed = sum(1 for b in self.map.blocks if not b.active)
            _game_state.bricks_destroyed = new_destroyed

            self.score += points
            renpy.store.breakout_score = self.score

            self.map.update_powerups(dt, self.paddle, self.balls)

            # Check story milestones
            self._check_milestones()

            self.balls   = [b for b in self.balls   if not b.launched or b.y < C.HEIGHT + b.radius]
            self.bullets = [b for b in self.bullets if b.active]

            if not self.balls:
                self._end("lose")
            elif all(not b.active for b in self.map.blocks):
                if _game_state.phase == 1:
                    # Aguarda diálogos pendentes (ex: part2 enfileirada no mesmo frame)
                    if not self._dm.is_playing and self._dm.queue.is_empty():
                        self._end("phase1_complete")
                else:
                    # Aguarda diálogos pendentes (ex: part4 enfileirada no mesmo frame)
                    if not self._dm.is_playing and self._dm.queue.is_empty():
                        self._end("phase2_complete")

            self.paddle.rect.width  = C.PADDLE_SIZES[self.paddle.size_idx]
            self.paddle.rect.left   = max(C.PLAY_BORDER, self.paddle.rect.left)
            self.paddle.rect.right  = min(C.WIDTH - C.PLAY_BORDER, self.paddle.rect.right)

            self._render_frame(width, height, rv, canvas, scale_x, scale_y, st, at)

            score_d = Text("Score: " + str(self.score))
            score_r = renpy.render(score_d, width, 60, st, at)
            rv.blit(score_r, (width // 2 - score_r.width // 2, 15))

            renpy.redraw(self, 0)
            return rv

        # ----------------------------------------------------------
        def event(self, ev, x, y, st):
            # Sinais internos — devem passar mesmo durante a pausa
            if self._dialogue_requested:
                self._dialogue_requested = False
                return "dialogue"
            if self.result_triggered and self._end_result is not None:
                result = self._end_result
                self._end_result = None
                return result

            # Pausado (tela congelada atrás do diálogo) — ignora input do jogo
            if _game_state.paused:
                raise renpy.IgnoreEvent()

            if ev.type == pygame.KEYDOWN:
                if ev.key == pygame.K_ESCAPE:
                    return "pause"
                if ev.key == pygame.K_SPACE:
                    if not self.paddle.shooter_active:
                        for ball in self.balls:
                            if not ball.launched:
                                ball.launch()
                                break
            raise renpy.IgnoreEvent()


screen breakout():
    add _get_breakout_screen()


screen breakout_pause_menu():
    modal True
    key "game_menu" action Return("resume")
    frame:
        xalign 0.5
        yalign 0.5
        padding (60, 40)
        vbox:
            spacing 18
            xalign 0.5
            text "PAUSA" xalign 0.5 size 40
            null height 10
            textbutton "Retomar"        action Return("resume") xalign 0.5
            textbutton "Opções"         action ShowMenu("preferences") xalign 0.5
            textbutton "Menu Principal" action MainMenu() xalign 0.5
            textbutton "Sair"           action Quit(confirm=False) xalign 0.5


label breakout_game:
    $ breakout_score = 0
    $ _game_state.reset()
    $ _reset_breakout_screen()   # fresh instance for new game

    label .game_loop:
        call screen breakout

        if _return == "dialogue":
            # Jogo congelado no master layer — sem redraw contínuo, física não roda
            show expression _get_breakout_screen() as breakout_frozen
            call breakout_dialogue_show
            hide breakout_frozen
            $ _game_state.paused = False
            $ _get_breakout_screen().last_st = None
            jump .game_loop
        elif _return == "phase1_complete":
            # Fase 1 zerada — dispara part3 diretamente e avança para fase 2
            $ _game_state.part3_done = True
            $ _game_state.current_dialogue = _get_breakout_screen()._registry.get("part3")
            $ _game_state.paused = True
            show expression _get_breakout_screen() as breakout_frozen
            call breakout_dialogue_show
            hide breakout_frozen
            $ _game_state.paused = False
            $ _get_breakout_screen()._advance_to_phase2()   # já reseta last_st internamente
            jump .game_loop
        elif _return == "phase2_complete":
            # Todos os blocos da fase 2 destruídos — dispara o plot twist diretamente
            $ _game_state.part5_done = True
            $ _game_state.current_dialogue = _get_breakout_screen()._registry.get("part5")
            $ _game_state.paused = True
            show expression _get_breakout_screen() as breakout_frozen
            call breakout_dialogue_show
            hide breakout_frozen
            $ _game_state.paused = False
            jump breakout_win
        elif _return == "pause":
            $ _game_state.paused = True
            show expression _get_breakout_screen() as breakout_frozen
            call screen breakout_pause_menu
            hide breakout_frozen
            $ _game_state.paused = False
            $ _get_breakout_screen().last_st = None
            jump .game_loop
        elif _return == "win":
            jump breakout_win
        elif _return == "lose":
            jump breakout_lose

        return


label breakout_win:
    jump breakout_final_scene


label breakout_lose:
    "Todas as bolas caíram... Tente de novo."
    jump breakout_submit_score


label breakout_submit_score:
    $ player_name = renpy.input("Insira seu nome:", default="", length=15)
    $ leaderboard_save(player_name, breakout_score)
    $ renpy.full_restart()


screen game_settings():
    tag menu
    use game_menu(_("Dev Settings"), scroll="viewport"):
        style_prefix "slider"
        vbox:
            label _("Paddle Size")
            label _("Width")
            bar value VariableValue("paddle_width", range=250, offset=50, step=5)
            text _("[paddle_width]px")
            label _("Height")
            bar value VariableValue("paddle_height", range=25, offset=5, step=5)
            text _("[paddle_height]px")
