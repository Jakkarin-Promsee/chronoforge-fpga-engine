import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from interpret_langauge.game_class import GameUIStage, GameUI, CharacterObject

from main.stage_ui import center_data

def stage():
    stage = GameUIStage()

    stage.game_ui = GameUI(
        show_healt_text=1,
        reset_character=0,
        transparent_out_screen_display=0,
        healt_current=0,
        healt_max=96,
        healt_bar_pos_x=190,
        healt_bar_pos_y=400,
        healt_bar_w=120,
        healt_bar_h=20,
        healt_bar_sensitivity=0.04,
        wait_time=12.9
    )

    stage.character_objects.extend([
        CharacterObject(140 + (center_data.CHARACTER_W + center_data.GAP) * (i + 5), 160, ch)
        for i, ch in enumerate("IS ")
        if ch != " "
    ])

    return stage