import json
import os
from typing import List


# ================================================================
# 1. Game Manager
# ================================================================
class GameManager:
    def __init__(self,
                 stage=0,
                 attack_amount=-1,
                 platform_amount=-1,
                 wait_time=0,
                 gravity_direction=0,
                 display_pos_x1=0,
                 display_pos_y1=0,
                 display_pos_x2=0,
                 display_pos_y2=0,
                 free_unused=0):

        self.stage = stage
        self.attack_amount = attack_amount
        self.platform_amount = platform_amount
        self.wait_time = wait_time
        self.gravity_direction = gravity_direction
        self.display_pos_x1 = display_pos_x1
        self.display_pos_y1 = display_pos_y1
        self.display_pos_x2 = display_pos_x2
        self.display_pos_y2 = display_pos_y2
        self.free_unused = free_unused

    def to_dict(self):
        return {
            "stage": self.stage,
            "attack_amount": self.attack_amount,
            "platform_amount": self.platform_amount,
            "wait_time": self.wait_time,
            "gravity_direction": self.gravity_direction,
            "display_pos_x1": self.display_pos_x1,
            "display_pos_y1": self.display_pos_y1,
            "display_pos_x2": self.display_pos_x2,
            "display_pos_y2": self.display_pos_y2,
            "free(unused)": self.free_unused
        }


# ================================================================
# 2. Attack Object
# ================================================================
class AttackObject:
    def __init__(self,
                 type=0,
                 colider_type=0,
                 movement_direction=0,
                 speed=0,
                 pos_x=0,
                 pos_y=0,
                 w=0,
                 h=0,
                 wait_time=0,
                 destroy_time=0,
                 destroy_trigger=0,
                 free_unused=0):

        self.type = type
        self.colider_type = colider_type
        self.movement_direction = movement_direction
        self.speed = speed
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.w = w
        self.h = h
        self.wait_time = wait_time
        self.destroy_time = destroy_time
        self.destroy_trigger = destroy_trigger
        self.free_unused = free_unused

    def to_dict(self):
        return {
            "type": self.type,
            "colider_type": self.colider_type,
            "movement_direction": self.movement_direction,
            "speed": self.speed,
            "pos_x": self.pos_x,
            "pos_y": self.pos_y,
            "w": self.w,
            "h": self.h,
            "wait_time": self.wait_time,
            "destroy_time": self.destroy_time,
            "destroy_trigger": self.destroy_trigger,
            "free(unused)": self.free_unused
        }


# ================================================================
# 3. Platform Object
# ================================================================
class PlatformObject:
    def __init__(self,
                 movement_direction=0,
                 speed=0,
                 pos_x=0,
                 pos_y=0,
                 w=0,
                 h=0,
                 wait_time=0,
                 destroy_time=0,
                 destroy_trigger=0,
                 free_unused=0):

        self.movement_direction = movement_direction
        self.speed = speed
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.w = w
        self.h = h
        self.wait_time = wait_time
        self.destroy_time = destroy_time
        self.destroy_trigger = destroy_trigger
        self.free_unused = free_unused

    def to_dict(self):
        return {
            "movement_direction": self.movement_direction,
            "speed": self.speed,
            "pos_x": self.pos_x,
            "pos_y": self.pos_y,
            "w": self.w,
            "h": self.h,
            "wait_time": self.wait_time,
            "destroy_time": self.destroy_time,
            "destroy_trigger": self.destroy_trigger,
            "free(unused)": self.free_unused
        }


# ================================================================
# 4. Game Stage (One stage = GM + objects)
# ================================================================
class GameStage:
    def __init__(self, game_manager=None):
        self.game_manager = game_manager or GameManager()
        self.attack_objects: List[AttackObject] = []
        self.platform_objects: List[PlatformObject] = []

    def to_dict(self):
        self.game_manager.attack_amount = len(self.attack_objects)
        self.game_manager.platform_amount = len(self.platform_objects)

        return {
            "game_manger": self.game_manager.to_dict(),
            "attack_object": [obj.to_dict() for obj in self.attack_objects],
            "platform_object": [obj.to_dict() for obj in self.platform_objects]
        }

    def get_total_time(self):
        total_time = 0
        total_time += self.game_manager.wait_time

        for obj in self.attack_objects:
            total_time += obj.wait_time

        return total_time
    

# ================================================================
# 5. Entire Game (multiple stages)
# ================================================================
class EntireGame:
    def __init__(self):
        self.stages = []

    def add_stage(self, stage: GameStage):
        self.stages.append(stage)

    # ---- EXPORT to many stageXX.json ----
    def export(self, export_folder):
        # Create directory if missing
        os.makedirs(export_folder, exist_ok=True)

        # Export each stage
        for i, stage in enumerate(self.stages):
            output_path = os.path.join(export_folder, f"stage{i:02}.json")
            with open(output_path, "w") as f:
                json.dump(stage.to_dict(), f, indent=4)
            print(f"stage_{i:02}: {stage.get_total_time():.2f}")

        print(f"Exported {len(self.stages)} stages → {export_folder}/")



# ================================================================
# 6. Game UI Object (UI ROM Entry)
# ================================================================
class GameUI:
    def __init__(self,
                 show_healt_text=0,
                 reset_character=0,
                 character_amount=0,

                 healt_current=0,
                 healt_max=0,

                 transparent_out_screen_display=0,
                 reset_when_dead=0,

                 healt_bar_pos_x=0,
                 healt_bar_pos_y=0,
                 healt_bar_w=0,
                 healt_bar_h=0,

                 healt_bar_sensitivity=0.0,   # seconds (0.01–1.23)
                 wait_time=0,                  # seconds
                 free_unused=0):

        self.show_healt_text = show_healt_text
        self.reset_character = reset_character
        self.character_amount = character_amount

        self.healt_current = healt_current
        self.healt_max = healt_max

        self.transparent_out_screen_display = transparent_out_screen_display
        self.reset_when_dead = reset_when_dead

        self.healt_bar_pos_x = healt_bar_pos_x
        self.healt_bar_pos_y = healt_bar_pos_y
        self.healt_bar_w = healt_bar_w
        self.healt_bar_h = healt_bar_h

        self.healt_bar_sensitivity = healt_bar_sensitivity
        self.wait_time = wait_time

        self.free_unused = free_unused

    def to_dict(self):
        return {
            "free(unused)": self.free_unused,

            "show_healt_text": self.show_healt_text,
            "reset_character": self.reset_character,
            "character_amount": self.character_amount,

            "healt_current": self.healt_current,
            "healt_max": self.healt_max,

            "transparent_out_screen_display": self.transparent_out_screen_display,
            "reset_when_dead": self.reset_when_dead,

            "healt_bar_pos_x": self.healt_bar_pos_x,
            "healt_bar_pos_y": self.healt_bar_pos_y,
            "healt_bar_w": self.healt_bar_w,
            "healt_bar_h": self.healt_bar_h,

            "healt_bar_sensitivity": self.healt_bar_sensitivity,
            "wait_time": self.wait_time
        }

# ================================================================
# 7. Character Object (Character ROM Entry)
# ================================================================
class CharacterObject:
    def __init__(self,
                 character_pos_x=0,
                 character_pos_y=0,
                 character_index="A"):

        self.character_pos_x = character_pos_x
        self.character_pos_y = character_pos_y

        # ---- normalize input ----
        if not isinstance(character_index, str) or len(character_index) != 1:
            raise ValueError("character_index must be a single character")

        ch = character_index.upper()

        # ---- A–X : 0–23 ----
        if "A" <= ch <= "X":
            self.character_index = ord(ch) - ord("A")

        # ---- 0–9 : 26–35 ----
        elif "0" <= ch <= "9":
            self.character_index = 26 + ord(ch) - ord("0")

        # ---- Special characters ----
        else:
            special_map = {
                "/": 36,
                # ":": 37,
                # ".": 38,
                # "-": 39,
                # " ": 40
            }

            if ch in special_map:
                self.character_index = special_map[ch]
            else:
                # fallback: blank / unknown glyph
                self.character_index = 255


    def to_dict(self):
        return {
            "character_pos_x": self.character_pos_x,
            "character_pos_y": self.character_pos_y,
            "character_index": self.character_index
        }

# ================================================================
# UI Stage (One UI step = UI config + characters)
# ================================================================
class GameUIStage:
    def __init__(self, game_ui=None):
        self.game_ui = game_ui or GameUI()
        self.character_objects: List[CharacterObject] = []

    def to_dict(self):
        # auto-fill character_amount for encoder correctness
        self.game_ui.character_amount = len(self.character_objects)

        return {
            "game_ui": self.game_ui.to_dict(),
            "character_object": [
                ch.to_dict() for ch in self.character_objects
            ]
        }

    def get_total_time(self):
        total_time = 0
        total_time += self.game_ui.wait_time

        return total_time

# ================================================================
# Entire Game UI (Multiple UI stages)
# ================================================================
class EntireGameUI:
    def __init__(self):
        self.ui_stages = []

    def add_stage(self, stage: GameUIStage):
        self.ui_stages.append(stage)

    # ---- EXPORT to stage_ui_XX.json ----
    def export(self, export_folder):
        os.makedirs(export_folder, exist_ok=True)

        for i, stage in enumerate(self.ui_stages):
            output_path = os.path.join(export_folder, f"stage_ui_{i:02}.json")
            with open(output_path, "w") as f:
                json.dump(stage.to_dict(), f, indent=4)
            print(f"stage_ui_{i:02}: {stage.get_total_time():.2f}")

        print(f"Exported {len(self.ui_stages)} UI stages → {export_folder}/")
