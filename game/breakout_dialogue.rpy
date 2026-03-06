################################################################################
# breakout_dialogue.rpy
# Usa o sistema NATIVO de diálogo do Ren'Py (Character + say screen).
################################################################################

# ---------------------------------------------------------------------------
# Personagens
# ---------------------------------------------------------------------------
define kai  = Character("Kai",  color="#88ccff")
define aria = Character("ARIA", color="#ff88cc")

# ---------------------------------------------------------------------------
# Imagens dos sprites (declaradas para o sistema show/hide do Ren'Py)
# ---------------------------------------------------------------------------
image kai  normal   = "images/kai_normal.png"
image kai  confused = "images/kai_confused.png"
image kai  shocked  = "images/kai_shocked.png"
image aria normal   = "images/aria_normal.png"
image aria happy    = "images/aria_happy.png"
image aria evil     = "images/aria_evil.png"

# ---------------------------------------------------------------------------
# Label principal — recebe a sequência de _game_state.current_dialogue
# e usa o say nativo do Ren'Py para cada linha.
# ---------------------------------------------------------------------------
label breakout_dialogue_show:
    python:
        _seq = _game_state.current_dialogue

    if _seq is None:
        $ _game_state.paused = False
        return

    python:
        _dlg_lines = list(_seq.lines)
        _dlg_idx   = 0
        # Mapeia sprite filename → tag Ren'Py
        _sprite_map = {
            "kai_normal.png":    ("kai",  "normal"),
            "kai_confused.png":  ("kai",  "confused"),
            "kai_shocked.png":   ("kai",  "shocked"),
            "aria_normal.png":   ("aria", "normal"),
            "aria_happy.png":    ("aria", "happy"),
            "aria_evil.png":     ("aria", "evil"),
        }
        _last_kai_sprite  = None
        _last_aria_sprite = None

    label .line_loop:
        if _dlg_idx >= len(_dlg_lines):
            jump .done

        python:
            _line = _dlg_lines[_dlg_idx]
            _tag, _expr = _sprite_map.get(_line.sprite, (None, None))

        # Mostra só o personagem que está falando, esconde o outro
        if _tag == "kai":
            hide aria
            show expression ("kai " + _expr) as kai at left with dissolve
        elif _tag == "aria":
            hide kai
            show expression ("aria " + _expr) as aria at right with dissolve

        # Fala com o sistema nativo (say screen, caixa de texto, histórico)
        if _line.speaker == "Kai":
            kai "[_line.text]"
        elif _line.speaker == "ARIA":
            aria "[_line.text]"

        $ _dlg_idx += 1
        jump .line_loop
    
    label .done:
        hide kai  with dissolve
        hide aria with dissolve

        python:
            _game_state.current_dialogue = None
            # NOTE: paused=False is set by the game_loop label after a brief
            # post-dialogue freeze, not here.
            if _breakout_dm is not None:
                _breakout_dm.on_sequence_finished()
        return


# ---------------------------------------------------------------------------
# Store defaults
# ---------------------------------------------------------------------------
default _breakout_dm = None


# ---------------------------------------------------------------------------
# Cena final — OPPAIMAN SYSTEMS
# ---------------------------------------------------------------------------
label breakout_final_scene:
    scene expression Transform("images/FinalBG.png", xysize=(config.screen_width, config.screen_height)) with dissolve
    pause 1.5

    show text "{color=#00ff00}OPPAIMAN SYSTEMS{/color}" with dissolve
    pause 2.0
    hide text

    show text "{color=#00ff00}Novo núcleo de IA instalado.{/color}" with dissolve
    pause 1.8
    hide text

    show text "{color=#00ff00}Origem: Candidato #1042{/color}" with dissolve
    pause 2.0
    hide text

    $ _final_name = renpy.input("Candidato, insira seu nome:", default="", length=15)
    $ leaderboard_save(_final_name, breakout_score)

    show text "{color=#00ff00}Registro completo.{/color}" with dissolve
    pause 1.5
    hide text

    show text "{color=#00ff00}Preparando próximo candidato...{/color}" with dissolve
    pause 2.0
    hide text

    pause 0.8
    scene black with dissolve
    pause 1.0
    
    $ renpy.full_restart()
