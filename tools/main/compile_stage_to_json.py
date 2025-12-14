import importlib
import glob
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from interpret_langauge.game_class import EntireGame, EntireGameUI


game = EntireGame()

STAGE_UI_DIR = "stage"
STAGE_UI_PATTERN = "stage_*.py"

stage_files = sorted(
    glob.glob(os.path.join(os.path.dirname(__file__), STAGE_UI_DIR, STAGE_UI_PATTERN))
)

for path in stage_files:
    module_name = os.path.splitext(os.path.basename(path))[0]
    module = importlib.import_module(f"{STAGE_UI_DIR}.{module_name}")

    # Expect each file to define stage()
    game.add_stage(module.stage())

# Base path for this file
tools_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Final output folder
export_folder = os.path.join(tools_path, "json_stage_source")
    
# Export
game.export(export_folder)

################################

game_ui = EntireGameUI()

STAGE_UI_DIR = "stage_ui"
STAGE_UI_PATTERN = "stage_ui_*.py"

stage_ui_files = sorted(
    glob.glob(os.path.join(os.path.dirname(__file__), STAGE_UI_DIR, STAGE_UI_PATTERN))
)

for path in stage_ui_files:
    module_name = os.path.splitext(os.path.basename(path))[0]
    module = importlib.import_module(f"{STAGE_UI_DIR}.{module_name}")

    # Expect each file to define stage()
    game_ui.add_stage(module.stage())

# Base path for this file
tools_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Final output folder
export_folder = os.path.join(tools_path, "json_stage_ui_source")
    
# Export
game_ui.export(export_folder)
