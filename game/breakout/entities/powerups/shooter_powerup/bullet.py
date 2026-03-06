from breakout.config import constants as C


class Bullet:
    RADIUS = 5
    SPEED  = 12

    def __init__(self, x, y):
        self.x        = float(x)
        self.y        = float(y)
        self.radius   = self.RADIUS
        self.vx       = 0.0
        self.vy       = -self.SPEED
        self.active   = True
        self.launched = True   # para compatibilidade com checagem de saída de tela

    def update(self, delta_time):
        self.y += self.vy * delta_time * 60
        if self.y + self.radius < 0:
            self.active = False
