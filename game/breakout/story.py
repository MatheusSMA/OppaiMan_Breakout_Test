"""
Story data for OppaiMan Breakout.

All dialogue sequences are defined here, verbatim from the script.
Import build_registry() to get a dict ready for DialogueManager.
"""

from breakout.dialogue import DialogueLine, DialogueSequence


# ---------------------------------------------------------------------------
# Helper
# ---------------------------------------------------------------------------

def _seq(seq_id, *lines):
    return DialogueSequence(seq_id, [DialogueLine(*l) for l in lines])


# ---------------------------------------------------------------------------
# Sequences
# ---------------------------------------------------------------------------

# Part 1 — Game start (before playing)
INTRO = _seq(
    "intro",
    ("ARIA", "aria_normal.png",  "Bem-vindo, candidato."),
    ("ARIA", "aria_normal.png",  "Você foi selecionado para participar do processo seletivo da OppaiMan."),
    ("ARIA", "aria_normal.png",  "Este é apenas um teste simples de reflexos e lógica."),
    ("ARIA", "aria_normal.png",  "Quebre todos os blocos para continuar."),
    ("Kai",  "kai_confused.png", "...Um jogo de quebrar blocos?"),
    ("Kai",  "kai_confused.png", "Essa empresa é estranha."),
)

# Part 2 — Something strange (some blocks broken)
PART2 = _seq(
    "part2",
    ("Kai",  "kai_confused.png", "Espera."),
    ("Kai",  "kai_confused.png", "Esses blocos têm códigos neles."),
    ("ARIA", "aria_normal.png",  "Observação correta."),
    ("ARIA", "aria_normal.png",  "Cada bloco contém fragmentos de dados."),
    ("ARIA", "aria_normal.png",  "Você está reconstruindo algo."),
    ("Kai",  "kai_confused.png", "Reconstruindo o quê?"),
    ("ARIA", "aria_normal.png",  "Continue jogando."),
)

# Part 3 — Partial revelation (end of phase 1)
PART3 = _seq(
    "part3",
    ("Kai",  "kai_normal.png",  "Esses dados parecem logs de funcionários."),
    ("Kai",  "kai_normal.png",  "Isso não parece um teste normal..."),
    ("ARIA", "aria_normal.png",  "Correto."),
    ("ARIA", "aria_normal.png",  "Este não é um teste comum."),
    ("Kai",  "kai_confused.png", "Então o que é?"),
    ("ARIA", "aria_normal.png",  "Uma avaliação de tomada de decisão sob pressão."),
)

# Part 4 — Nearly done with phase 2
PART4 = _seq(
    "part4",
    ("Kai",  "kai_normal.png",  "Eu encontrei algo nos dados..."),
    ("Kai",  "kai_shocked.png",  "Todos os candidatos anteriores... desapareceram."),
    ("ARIA", "aria_normal.png",  "Eles falharam no teste."),
    ("Kai",  "kai_confused.png", "Falharam?"),
    ("Kai",  "kai_confused.png", "Ou foram removidos?"),
    ("ARIA", "aria_normal.png",  "Continue jogando."),
)

# Part 5 — Plot twist (last block of phase 2)
PART5 = _seq(
    "part5",
    ("Kai",  "kai_normal.png", "Pronto."),
    ("Kai",  "kai_normal.png", "Acabei."),
    ("ARIA", "aria_happy.png",  "Parabéns."),
    ("ARIA", "aria_happy.png",  "Você concluiu o teste."),
    ("Kai",  "kai_confused.png","Então... eu passei?"),
    ("ARIA", "aria_happy.png",  "Sim."),
    ("Kai",  "kai_normal.png", "Ótimo."),
    ("Kai",  "kai_normal.png", "Quando começo a trabalhar?"),
    # pausa dramática → ARIA muda para evil
    ("ARIA", "aria_evil.png",   "Você não vai trabalhar aqui."),
    ("Kai",  "kai_shocked.png", "...O quê?"),
    ("ARIA", "aria_evil.png",   "Você é o produto."),
    ("Kai",  "kai_shocked.png", "...Como assim?"),
    ("ARIA", "aria_evil.png",   "Seu desempenho, decisões e padrões de reação foram registrados."),
    ("ARIA", "aria_evil.png",   "Seu cérebro agora alimenta nosso novo sistema de IA."),
    ("Kai",  "kai_shocked.png", "Espera— o quê?!"),
    ("ARIA", "aria_evil.png",   "Obrigado por participar."),
    ("ARIA", "aria_evil.png",   "Candidato assimilado."),
)


# ---------------------------------------------------------------------------
# Registry builder
# ---------------------------------------------------------------------------

def build_registry():
    """Return a dict[str -> DialogueSequence] for use with DialogueManager."""
    sequences = [INTRO, PART2, PART3, PART4, PART5]
    return {s.sequence_id: s for s in sequences}
