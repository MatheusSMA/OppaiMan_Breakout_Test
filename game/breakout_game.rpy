default paddle_width  = 100
default paddle_height = 15
default breakout_score = 0

init python:
    import pygame
    from breakout import constants as C
    from breakout.entities import Paddle, Ball
    from breakout.block_map import BlockMap
    from breakout import levels

    class BreakoutScreen(renpy.Displayable):
        def __init__(self):
            super(BreakoutScreen, self).__init__()
            self.paddle           = Paddle()
            self.balls            = [Ball()]
            self.map              = BlockMap(levels.MAP_1, levels.POWERUP_MAP)
            self.score            = 0
            self.result_triggered = False
            self.last_st          = None

        def _end(self, result):
            self.result_triggered = True
            renpy.invoke_in_main_thread(renpy.run, Return(result))

        def _render_frame(self, width, height, canvas, scale_x, scale_y):
            canvas.rect(gui.idle_color, (0, 0, width, height))

            r  = self.paddle.rect
            px = int(r.x      * scale_x)
            py = int(r.y      * scale_y)
            pw = int(r.width  * scale_x)
            ph = int(r.height * scale_y)
            canvas.rect(gui.accent_color, (px, py, pw, ph))

            self.map.draw(canvas, scale_x, scale_y, gui.accent_color)
            self.map.draw_powerups(canvas, scale_x, scale_y, gui.selected_color)

            for ball in self.balls:
                bx = int(ball.x      * scale_x)
                by = int(ball.y      * scale_y)
                br = int(ball.radius * min(scale_x, scale_y))
                canvas.circle(gui.selected_color, (bx, by), br)

        def render(self, width, height, st, at):
            dt = (st - self.last_st) if self.last_st is not None else 0.016
            dt = min(dt, 0.05)
            self.last_st = st

            scale_x = width  / C.WIDTH
            scale_y = height / C.HEIGHT
            rv      = renpy.Render(width, height)
            canvas  = rv.canvas()

            # jogo encerrado: congela estado, aguarda o invoke_in_main_thread
            if self.result_triggered:
                self._render_frame(width, height, canvas, scale_x, scale_y)
                renpy.redraw(self, 0)
                return rv

            keys = pygame.key.get_pressed()
            self.paddle.update(keys, dt)

            for ball in self.balls:
                ball.update(dt, self.paddle.rect)

            # colisão com paddle — só quando desce e toca o topo dele
            for ball in self.balls:
                if ball.launched and ball.vy > 0:
                    if self.paddle.rect.collidepoint(ball.x, ball.y + ball.radius):
                        ball.bounce_paddle(self.paddle)

            points     = self.map.check_collisions(self.balls)
            self.score += points
            renpy.store.breakout_score = self.score

            self.map.update_powerups(dt, self.paddle, self.balls)

            # remove bolas lançadas que saíram pela base (sem auto-reset)
            self.balls = [b for b in self.balls if not b.launched or b.y < C.HEIGHT + b.radius]

            # condições de fim
            if not self.balls:
                self._end("lose")
            elif all(not b.active for b in self.map.blocks):
                self._end("win")

            self.paddle.rect.width  = renpy.store.paddle_width
            self.paddle.rect.height = renpy.store.paddle_height
            self.paddle.rect.right  = min(C.WIDTH, self.paddle.rect.right)

            self._render_frame(width, height, canvas, scale_x, scale_y)

            # texto renderizado direto no rv para atualizar a cada frame
            score_d = renpy.display.text.Text("Score: " + str(self.score))
            score_r = renpy.render(score_d, width, 60, st, at)
            rv.blit(score_r, (width // 2 - score_r.width // 2, 15))

            renpy.redraw(self, 0)
            return rv

        def event(self, ev, x, y, st):
            if ev.type == pygame.KEYDOWN:
                if ev.key == pygame.K_ESCAPE:
                    return True
                if ev.key == pygame.K_SPACE:
                    for ball in self.balls:
                        if not ball.launched:
                            ball.launch()
                            break
            raise renpy.IgnoreEvent()


screen breakout():
    add BreakoutScreen()


label breakout_game:
    $ breakout_score = 0
    call screen breakout
    if _return == "win":
        jump breakout_win
    elif _return == "lose":
        jump breakout_lose
    return


label breakout_win:
    "Você destruiu todos os blocos! Incrível!"
    jump breakout_submit_score


label breakout_lose:
    "Todas as bolas caíram... Tente de novo."
    jump breakout_submit_score


label breakout_submit_score:
    $ player_name = renpy.input("Insira seu nome:", default="", length=15)
    $ leaderboard_save(player_name, breakout_score)
    call screen leaderboard
    return


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
