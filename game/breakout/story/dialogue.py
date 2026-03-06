"""
Dialogue system for OppaiMan Breakout.
DialogueLine      -- one line of dialogue (speaker, sprite, text)
DialogueSequence  -- ordered list of DialogueLines with an id
DialogueQueue     -- FIFO queue of sequences
DialogueManager   -- pauses gameplay and signals the Ren'Py label to run
"""


class DialogueLine:
    """A single line spoken by a character."""

    def __init__(self, speaker, sprite, text):
        # speaker: "Kai" | "ARIA"
        self.speaker = speaker
        # sprite:  filename, e.g. "kai_neutral.png"
        self.sprite  = sprite
        self.text    = text

    def __repr__(self):
        return f"<DialogueLine {self.speaker!r}: {self.text[:30]!r}>"


class DialogueSequence:
    """An ordered collection of DialogueLines identified by a string id."""

    def __init__(self, sequence_id, lines):
        self.sequence_id = sequence_id
        self.lines       = list(lines)

    def __repr__(self):
        return f"<DialogueSequence {self.sequence_id!r} ({len(self.lines)} lines)>"


class DialogueQueue:
    """FIFO queue for DialogueSequence objects."""

    def __init__(self):
        self._queue = []

    def enqueue(self, sequence):
        self._queue.append(sequence)

    def dequeue(self):
        if self._queue:
            return self._queue.pop(0)
        return None

    def is_empty(self):
        return len(self._queue) == 0

    def __len__(self):
        return len(self._queue)


class DialogueManager:
    """Central dialogue controller."""

    def __init__(self, game_state, sequence_registry):
        self.game_state        = game_state
        self.sequence_registry = sequence_registry
        self.queue             = DialogueQueue()
        self.is_playing        = False

    def enqueue(self, sequence_id):
        """Enqueue a dialogue by id. Safe to call even while one plays."""
        seq = self.sequence_registry.get(sequence_id)
        if seq is None:
            return
        self.queue.enqueue(seq)

    def tick(self):
        if self.is_playing:
            return False
        if self.queue.is_empty():
            return False
        return self._play_next()

    def on_sequence_finished(self):
        """Called after the player advances through all lines."""
        self.is_playing = False

    def _play_next(self):
        seq = self.queue.dequeue()
        if seq is None:
            return False
        self.is_playing                  = True
        self.game_state.paused           = True
        self.game_state.current_dialogue = seq
        return True
