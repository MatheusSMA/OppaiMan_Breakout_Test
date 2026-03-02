init python:
    import pygame
    from breakout import constants as C
    from breakout.entities import Paddle, Square

    class BreakoutScreen(renpy.Displayable):
        def __init__(self):
            super(BreakoutScreen, self).__init__()
            self.paddle = Paddle()
            self.square = Square()
            self.last_st = None

        def render(self, width, height, st, at):
            dt = (st - self.last_st) if self.last_st is not None else 0.016
            dt = min(dt, 0.05)  # cap pra não explodir se o jogo travar
            self.last_st = st

            keys = pygame.key.get_pressed()
            self.paddle.update(keys, dt)
            
            # escala proporcional pra caber na tela sem distorcer
            scale = min(width / C.WIDTH, height / C.HEIGHT)
            gw = int(C.WIDTH  * scale)
            gh = int(C.HEIGHT * scale)
            ox = (width  - gw) // 2   # centraliza horizontal
            oy = (height - gh) // 2   # centraliza vertical

            rv = renpy.Render(width, height)
            canvas = rv.canvas()

            canvas.rect(gui.idle_color, (0, 0, width, height))
            canvas.rect(gui.idle_color, (ox, oy, gw, gh))
            
            # converte coordenadas do jogo pra coordenadas de tela
            r = self.paddle.rect
            sx = int(r.x      * scale) + ox
            sy = int(r.y      * scale) + oy
            sw = int(r.width  * scale)
            sh = int(r.height * scale)
            
            r2 = self.square.rect
            sx2 = int(r2.x      * scale) + ox
            sy2 = int(r2.y      * scale) + oy
            sw2 = int(r2.width  * scale)
            sh2 = int(r2.height * scale)
            
            canvas.rect(C.RED, (sx2, sy2, sw2, sh2))            
            canvas.rect(gui.accent_color, (sx, sy, sw, sh))
            
            renpy.redraw(self, 0)
            return rv

        def event(self, ev, x, y, st):
            if ev.type == pygame.KEYDOWN and ev.key == pygame.K_ESCAPE:
                return True
            raise renpy.IgnoreEvent()


screen breakout():
    add BreakoutScreen()


label breakout_game:
    call screen breakout
    return
