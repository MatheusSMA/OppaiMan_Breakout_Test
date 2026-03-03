default paddle_width = 100
default paddle_height = 15

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

            self.paddle.rect.width = renpy.store.paddle_width
            self.paddle.rect.height = renpy.store.paddle_height
            self.paddle.rect.right = min(C.WIDTH, self.paddle.rect.right) # evita que a raquete passe da borda direita quando aumentar de tamanho.            
            
            scale_x = width  / C.WIDTH
            scale_y = height / C.HEIGHT
            ox = 0
            oy = 0
            
            rv = renpy.Render(width, height)
            canvas = rv.canvas()
            
            canvas.rect(gui.idle_color, (ox, oy, width, height))
            
            # converte coordenadas do jogo pra coordenadas de tela
            r = self.paddle.rect
            sx = int(r.x * scale_x) + ox
            sy = int(r.y * scale_y) + oy
            sw = int(r.width  * scale_x)
            sh = int(r.height * scale_y)
            
            r2 = self.square.rect
            sx2 = int(r2.x * scale_x) + ox
            sy2 = int(r2.y * scale_y) + oy
            sw2 = int(r2.width  * scale_x)
            sh2 = int(r2.height * scale_y)
            
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


screen game_settings():
    tag menu
    use game_menu(_("Dev Settings"), scroll="viewport"):
        style_prefix "slider"
        vbox:
            label _("Paddle Size")
            label _("Width")
            bar value VariableValue("paddle_width", range=250,offset=50,step=5)
            text _("[paddle_width]px")
            label _("Height")
            bar value VariableValue("paddle_height", range=25,offset=5,step=5)
            text _("[paddle_height]px")           
            