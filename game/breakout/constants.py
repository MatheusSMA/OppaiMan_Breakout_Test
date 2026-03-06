# tamanho da janela
WIDTH  = 800
HEIGHT = 600

# bola
BALL_RADIUS       = 12
BALL_SPEED        = 5    # velocidade total (px/frame a 60fps)
BALL_LAUNCH_ANGLE = 35   # graus a partir do eixo vertical (positivo = direita)

# raquete
PADDLE_WIDTH  = 100
PADDLE_HEIGHT = 20
PADDLE_SPEED  = 8
PLAY_BORDER   = 22   # margem da borda do GameBG (px do jogo)
PADDLE_Y      = HEIGHT - 40 - PLAY_BORDER

# 5 tamanhos discretos de raquete (em pixels do jogo)
PADDLE_SIZES = [50, 75, 100, 125, 150]
PADDLE_DEFAULT_SIZE_IDX = 2  # índice do tamanho padrão (100px)

# blocos
BLOCK_W        = 70
BLOCK_H        = 30
BLOCK_GAP      = 4   # espaço entre blocos
BLOCK_OFFSET_X = PLAY_BORDER + 10  # margem extra além da borda do GameBG
BLOCK_OFFSET_Y = 110  # distância do topo (espaço para a bola quicar acima)
