init python:
    def leaderboard_save(name, score):
        if not hasattr(persistent, 'leaderboard') or persistent.leaderboard is None:
            persistent.leaderboard = []
        persistent.leaderboard.append({'name': name.strip() or "Anon", 'score': score})
        persistent.leaderboard.sort(key=lambda e: e['score'], reverse=True)
        persistent.leaderboard = persistent.leaderboard[:10]

    def leaderboard_entries():
        if not hasattr(persistent, 'leaderboard') or not persistent.leaderboard:
            return []
        return persistent.leaderboard


screen leaderboard():
    tag menu
    use game_menu(_("Leaderboard"), scroll="viewport"):
        vbox:
            spacing 12
            if leaderboard_entries():
                for i, entry in enumerate(leaderboard_entries()):
                    hbox:
                        spacing 20
                        text "[i+1]."    min_width 40
                        text "[entry['name']]" min_width 200
                        text "[entry['score']] pts"
            else:
                text _("Nenhuma pontuação ainda.")
