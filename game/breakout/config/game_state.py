"""
GameState — shared mutable state between the Displayable and the
dialogue / trigger systems.
"""


class GameState:
    def __init__(self):
        # ---- core gameplay ----
        self.paused            = False   # True while dialogue is running
        self.bricks_destroyed  = 0
        self.phase             = 1       # 1 or 2

        # ---- dialogue runtime ----
        self.current_dialogue  = None    # DialogueSequence currently shown

        # ---- story flags (prevent re-triggering) ----
        self.intro_done        = False
        self.part2_done        = False
        self.part3_done        = False   # end of phase 1
        self.part4_done        = False   # near end of phase 2
        self.part5_done        = False   # plot twist (last block phase 2)
        self.final_done        = False   # ending scene shown

    def reset(self):
        """Full reset for a new game run."""
        self.__init__()
