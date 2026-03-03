default paddle_width = 100
default paddle_height = 15

init python:
    import pygame
    from breakout import constants as C
    from breakout.entities import Paddle, Ball

    class BreakoutScreen(renpy.Displayable):
        def __init__(self):
            super(BreakoutScreen, self).__init__()
            self.paddle = Paddle()            
            self.ball = Ball()
            self.last_st = None
        
        def render(self, width, height, st, at):
            dt = (st - self.last_st) if self.last_st is not None else 0.016
            dt = min(dt, 0.005)  # cap pra não explodir se o jogo travar
            self.last_st = st
            
            keys = pygame.key.get_pressed()
            self.paddle.update(keys, dt)
            self.ball.update(dt, self.paddle.rect)

            if self.ball.launched and self.paddle.rect.collidepoint(self.ball.x, self.ball.y + self.ball.radius):
                self.ball.vy = -abs(self.ball.vy)
            
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
            # p = paddle, b = ball
            r = self.paddle.rect
            px = int(r.x * scale_x) + ox
            py = int(r.y * scale_y) + oy
            pw = int(r.width  * scale_x)
            ph = int(r.height * scale_y)            
                                            
            canvas.rect(gui.accent_color, (px, py, pw, ph))

            bx = int(self.ball.x * scale_x)
            by = int(self.ball.y * scale_y)
            br = int(self.ball.radius * min(scale_x, scale_y))
            canvas.circle(C.RED, (bx, by), br)
    
            renpy.redraw(self, 0)
            return rv

        def event(self, ev, x, y, st):
            if ev.type == pygame.KEYDOWN:
                if ev.key == pygame.K_ESCAPE:
                    return True
                if ev.key == pygame.K_SPACE and not self.ball.launched:
                    self.ball.launch()
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
             
            