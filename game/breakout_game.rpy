default paddle_width  = 100
default paddle_height = 15
default breakout_score = 0

init python:
    import pygame
    from breakout.config.game_state      import GameState
    from breakout.story.dialogue         import DialogueManager
    from breakout.story.sequences        import build_registry
    from breakout.core.game              import BreakoutGame
    from breakout.core.renderer          import BreakoutRenderer
    from breakout.managers.collision     import CollisionManager
    from breakout.managers.level         import LevelManager
    from breakout.managers.powerup_manager import PowerupManager
    from breakout import constants as C

    _BLOCK_ANIM_FPS  = 6
    _BLOCK_ANIM_LEN  = 6

    _game_state      = GameState()
    _breakout_screen = None

    def _get_breakout_screen():
        global _breakout_screen
        if _breakout_screen is None:
            _breakout_screen = BreakoutScreen()
        return _breakout_screen

    def _reset_breakout_screen():
        global _breakout_screen
        _breakout_screen = None

    class BreakoutScreen(renpy.Displayable):
        def __init__(self):
            super(BreakoutScreen, self).__init__()
            registry = build_registry()
            dm       = DialogueManager(_game_state, registry)
            self._game     = BreakoutGame(
                _game_state, dm, registry,
                collision_mgr=CollisionManager(),
                level_mgr=LevelManager(phase=1),
                powerup_mgr=PowerupManager(),
            )
            self._renderer = BreakoutRenderer()
            self._registry = registry

            self.last_st        = None
            self.pending_signal = None
            self.anim_timer     = 0.0
            self.anim_frame     = 0
            self.powerup_frame  = 0

            renpy.store._breakout_dm = dm

        def _advance_to_phase2(self):
            self._game.advance_to_phase2()
            self.last_st = None

        def render(self, width, height, st, at):
            delta_time = max(0.0, min(
                (st - self.last_st) if self.last_st is not None else 0.016,
                0.05
            ))
            self.last_st = st

            scale_x       = width  / C.WIDTH
            scale_y       = height / C.HEIGHT
            render_target = renpy.Render(width, height)
            bg            = Transform("images/ui/GameBG.png", xysize=(width, height))
            render_target.blit(renpy.render(bg, width, height, st, at), (0, 0))
            canvas = render_target.canvas()

            if self._game.result_triggered:
                self._renderer.render_frame(render_target, canvas, self._game, scale_x, scale_y,
                                            st, at, self.anim_frame, self.powerup_frame)
                renpy.redraw(self, 0)
                return render_target

            if not _game_state.paused:
                signal = self._game.update(delta_time, pygame.key.get_pressed())
                if signal:
                    self.pending_signal = signal
                    self.last_st = None
                    pygame.event.post(pygame.event.Event(pygame.USEREVENT))

                self.anim_timer += delta_time
                if self.anim_timer >= 1.0 / _BLOCK_ANIM_FPS:
                    self.anim_timer    = 0.0
                    self.anim_frame    = (self.anim_frame    + 1) % _BLOCK_ANIM_LEN
                    self.powerup_frame = (self.powerup_frame + 1) % _BLOCK_ANIM_LEN

            self._renderer.render_frame(render_target, canvas, self._game, scale_x, scale_y,
                                        st, at, self.anim_frame, self.powerup_frame)
            self._draw_score(render_target, width, st, at)

            renpy.redraw(self, 0.1 if _game_state.paused else 0)
            return render_target

        def _draw_score(self, render_target, width, st, at):
            score_text   = Text("Score: " + str(self._game.score))
            score_render = renpy.render(score_text, width, 60, st, at)
            render_target.blit(score_render, (width // 2 - score_render.width // 2, 15))
            renpy.store.breakout_score = self._game.score

        def event(self, ev, x, y, st):
            if self.pending_signal:
                signal = self.pending_signal
                self.pending_signal = None
                return signal

            if _game_state.paused:
                raise renpy.IgnoreEvent()

            if ev.type == pygame.KEYDOWN:
                if ev.key == pygame.K_ESCAPE:
                    return "pause"
                if ev.key == pygame.K_SPACE:
                    if not self._game.paddle.shooter_active:
                        for ball in self._game.balls:
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
            textbutton "Opcoes"         action ShowMenu("preferences") xalign 0.5
            textbutton "Menu Principal" action MainMenu() xalign 0.5
            textbutton "Sair"           action Quit(confirm=False) xalign 0.5


label breakout_game:
    $ breakout_score = 0
    $ _game_state.reset()
    $ _reset_breakout_screen()

    label .game_loop:
        call screen breakout

        if _return == "dialogue":
            show expression _get_breakout_screen() as breakout_frozen
            call breakout_dialogue_show
            hide breakout_frozen
            $ _game_state.paused = False
            $ _get_breakout_screen().last_st = None
            jump .game_loop
        elif _return == "phase1_complete":
            $ _game_state.part3_done = True
            $ _game_state.current_dialogue = _get_breakout_screen()._registry.get("part3")
            $ _game_state.paused = True
            show expression _get_breakout_screen() as breakout_frozen
            call breakout_dialogue_show
            hide breakout_frozen
            $ _game_state.paused = False
            $ _get_breakout_screen()._advance_to_phase2()
            jump .game_loop
        elif _return == "phase2_complete":
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
    "Todas as bolas cairam... Tente de novo."
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
