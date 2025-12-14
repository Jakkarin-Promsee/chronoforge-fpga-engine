import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from interpret_langauge.game_class import GameUIStage, GameUI, CharacterObject

def stage():
    stage = GameUIStage()

    stage.game_ui = GameUI(
        show_healt_text=1,
        healt_current=100,
        healt_max=100,
        healt_bar_pos_x=20,
        healt_bar_pos_y=10,
        healt_bar_w=120,
        healt_bar_h=8,
        healt_bar_sensitivity=0.2,
        wait_time=1.0
    )

    CHARACTER_W = 17
    GAP = 1

    stage.character_objects.extend([

        CharacterObject(60 + (CHARACTER_W + GAP) * i, 40, ch)
        for i, ch in enumerate("THIS IS CHRONO FORGE")
        if ch != " "
        
    ])

    return stage