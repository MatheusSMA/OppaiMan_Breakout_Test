from .config.constants import (
    WIDTH, HEIGHT,
    BALL_RADIUS, BALL_SPEED, BALL_LAUNCH_ANGLE,
    PADDLE_WIDTH, PADDLE_HEIGHT, PADDLE_SPEED, PADDLE_Y,
)

# re-exporta o módulo para que `from breakout import constants as C` continue funcionando
from .config import constants
