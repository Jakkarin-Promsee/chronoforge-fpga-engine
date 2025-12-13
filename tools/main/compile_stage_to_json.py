import importlib
import glob
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from interpret_langauge.game_class import EntireGame


game = EntireGame()

STAGE_DIR = "stage"
STAGE_PATTERN = "stage_*.py"

stage_files = sorted(
    glob.glob(os.path.join(os.path.dirname(__file__), STAGE_DIR, STAGE_PATTERN))
)

print(stage_files)

for path in stage_files:
    module_name = os.path.splitext(os.path.basename(path))[0]
    module = importlib.import_module(f"{STAGE_DIR}.{module_name}")

    # Expect each file to define stage()
    game.add_stage(module.stage())

# Base path for this file
tools_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Final output folder
export_folder = os.path.join(tools_path, "json_stage_source")
    
# Export
game.export(export_folder)
