"""
BreakoutGame — orquestra toda a lógica do jogo.

Responsabilidades: física, colisões, milestones, win/lose.
NÃO conhece nada de Ren'Py ou rendering — puro Python.
"""
import pygame
from breakout import constants as C
from breakout.entities.core.paddle import Paddle
from breakout.entities.core.ball import Ball
from breakout.entities.powerups.shooter_powerup.bullet import Bullet
from breakout.managers.level import LevelManager


# Thresholds para dialogues de milestone
_PART2_THRESHOLD = 0.40   # 40% da fase 1 destruída → part2
_PART4_THRESHOLD = 0.50   # 50% da fase 2 destruída → part4


class BreakoutGame:
    """Orquestra o estado e a lógica do jogo.

    Recebe todos os managers via DI. Retorna sinais para BreakoutScreen
    sem depender de nenhuma API do Ren'Py.
    """

    def __init__(self, game_state, dialogue_manager, registry,
                 collision_mgr, level_mgr, powerup_mgr):
        self.game_state       = game_state
        self.dialogue_manager = dialogue_manager
        self.registry         = registry

        self.collision_mgr = collision_mgr
        self.level_mgr     = level_mgr
        self.powerup_mgr   = powerup_mgr

        self.paddle  = Paddle()
        self.balls   = [Ball()]
        self.bullets = []
        self.score   = 0

        # True enquanto aguarda Ren'Py processar o sinal de resultado
        self.result_triggered = False
        self.result_signal    = None

        self.dialogue_manager.enqueue("intro")

    # ------------------------------------------------------------------
    # Loop principal
    # ------------------------------------------------------------------

    def update(self, delta_time, keys):
        """Atualiza um frame do jogo. Retorna sinal ou None.

        Sinais possíveis:
          "dialogue"        — diálogo foi disparado este frame
          "lose"            — todas as bolas caíram
          "phase1_complete" — fase 1 zerada
          "phase2_complete" — fase 2 zerada
        """
        if self.result_triggered:
            return None

        # Dispara próxima sequência de diálogo se houver
        if not self.game_state.paused:
            if self.dialogue_manager.tick():
                return "dialogue"

        if self.game_state.paused:
            return None

        self._update_entities(delta_time, keys)
        self._resolve_collisions(delta_time)
        self._check_milestones()
        self._cleanup_inactive()
        self._clamp_paddle()

        return self._evaluate_win_lose()

    # ------------------------------------------------------------------
    # Física e colisões
    # ------------------------------------------------------------------

    def _update_entities(self, delta_time, keys):
        self.paddle.update(keys, delta_time)
        self._handle_shooter(keys)
        for ball in self.balls:
            ball.update(delta_time, self.paddle.rect)
        for bullet in self.bullets:
            bullet.update(delta_time)

    def _handle_shooter(self, keys):
        if not (self.paddle.shooter_active
                and self.paddle.fire_cooldown <= 0
                and self.paddle.shots_remaining > 0):
            return
        if keys[pygame.K_SPACE]:
            self._fire_bullets()

    def _fire_bullets(self):
        paddle_rect = self.paddle.rect
        self.bullets.append(Bullet(paddle_rect.left  + 4, paddle_rect.y))
        self.bullets.append(Bullet(paddle_rect.right - 4, paddle_rect.y))
        self.paddle.fire_cooldown   = 1.0
        self.paddle.shots_remaining -= 1
        if self.paddle.shots_remaining <= 0:
            self.paddle.shooter_active = False

    def _resolve_collisions(self, delta_time):
        self.collision_mgr.check_ball_paddle(self.balls, self.paddle)
        points  = self.level_mgr.check_collisions(self.balls)
        points += self.level_mgr.check_bullet_collisions(self.bullets)
        self.score += points
        self.game_state.bricks_destroyed = sum(
            1 for b in self.level_mgr.blocks if not b.active
        )
        self.powerup_mgr.update(
            self.level_mgr.powerups, delta_time, self.paddle, self.balls
        )

    def _cleanup_inactive(self):
        # powerup_mgr já limpou powerups; aqui limpa bolas e balas
        self.balls   = [ball   for ball   in self.balls   if not ball.launched or ball.y < C.HEIGHT + ball.radius]
        self.bullets = [bullet for bullet in self.bullets if bullet.active]

    def _clamp_paddle(self):
        self.paddle.rect.width = C.PADDLE_SIZES[self.paddle.size_idx]
        self.paddle.rect.left  = max(C.PLAY_BORDER, self.paddle.rect.left)
        self.paddle.rect.right = min(C.WIDTH - C.PLAY_BORDER, self.paddle.rect.right)

    # ------------------------------------------------------------------
    # Milestones e condições de fim
    # ------------------------------------------------------------------

    def _check_milestones(self):
        game_state        = self.game_state
        destruction_ratio = self.level_mgr.destruction_ratio
        if game_state.phase == 1:
            if not game_state.part2_done and destruction_ratio >= _PART2_THRESHOLD:
                game_state.part2_done = True
                self.dialogue_manager.enqueue("part2")
        else:
            if not game_state.part4_done and destruction_ratio >= _PART4_THRESHOLD:
                game_state.part4_done = True
                self.dialogue_manager.enqueue("part4")

    def _evaluate_win_lose(self):
        if not self.balls:
            return self._trigger("lose")
        if self.level_mgr.all_destroyed:
            return self._phase_complete_signal()
        return None

    def _phase_complete_signal(self):
        """Retorna sinal só quando não há diálogos pendentes."""
        if self.dialogue_manager.is_playing or not self.dialogue_manager.queue.is_empty():
            return None
        signal = "phase1_complete" if self.game_state.phase == 1 else "phase2_complete"
        return self._trigger(signal)

    def _trigger(self, signal):
        self.result_triggered = True
        self.result_signal    = signal
        return signal

    # ------------------------------------------------------------------
    # Transição de fase
    # ------------------------------------------------------------------

    def advance_to_phase2(self):
        """Reseta estado para fase 2. Chamado pelo game_loop após part3."""
        self.game_state.phase = 2
        self.level_mgr        = LevelManager(phase=2)
        self.balls            = [Ball()]
        self.bullets          = []
        self.result_triggered = False
        self.result_signal    = None
