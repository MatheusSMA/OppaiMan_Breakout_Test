"""
DialogueTriggerBlock — a normal Block that fires a dialogue sequence
when destroyed for the first time.
"""

from breakout.entities.block import Block


class DialogueTriggerBlock(Block):
    """
    A breakable block that triggers a named dialogue sequence once.

    Parameters
    ----------
    x, y, w, h      : position / size (pixels)
    trigger_id       : key into the DialogueManager's sequence_registry
    dialogue_manager : DialogueManager instance (injected at build time)
    powerup_type     : optional powerup class (same as Block)
    """

    def __init__(self, x, y, w, h, trigger_id, dialogue_manager, powerup_type=None):
        super().__init__(x, y, w, h, powerup_type)
        self.trigger_id       = trigger_id
        self.consumed         = False          # fire only once
        self._dm              = dialogue_manager

    # ------------------------------------------------------------------
    # Override both destruction paths
    # ------------------------------------------------------------------

    def _on_destroyed(self):
        """Called internally the first time the block is destroyed."""
        if not self.consumed and self._dm is not None:
            self.consumed = True
            self._dm.enqueue(self.trigger_id)

    def check_collision(self, ball, suppress_bounce=False):
        spawned = super().check_collision(ball, suppress_bounce=suppress_bounce)
        if not self.active:           # just became inactive → destroyed
            self._on_destroyed()
        return spawned

    def check_bullet_hit(self, bullet):
        spawned = super().check_bullet_hit(bullet)
        if not self.active:
            self._on_destroyed()
        return spawned
